import os
import json
import argparse
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    set_seed
)
from preprocess import clean_text

# Label mapping for 3-class sentiment
label2id = {"negative": 0, "neutral": 1, "positive": 2}
id2label = {0: "negative", 1: "neutral", 2: "positive"}

# Base model and output directory
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SAVE_DIR = "C:\\Users\\DELL\\Sentiment_Analysis_AI\\backend\\model"

# Load JSONL file
def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f]

# Tokenize input text
def tokenize(example, tokenizer):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=64  # reduced for CPU speed
    )

def main(args):
    set_seed(42)

    # Load and clean dataset
    raw_data = read_jsonl(args.data)

    # Filter out entries with unknown labels
    valid_labels = set(label2id)
    raw_data = [item for item in raw_data if item["label"] in valid_labels]

    # Clean text
    for item in raw_data:
        item["text"] = clean_text(item["text"])

    # Convert to Hugging Face Dataset
    dataset = Dataset.from_list(raw_data)

    # Map labels to integers
    dataset = dataset.map(lambda x: {"label": label2id[x["label"]]})

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True
    )

    # Tokenize dataset
    tokenized = dataset.map(lambda x: tokenize(x, tokenizer), batched=True)
    tokenized.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    # Training setup
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=4,       # reduced batch size for CPU
        num_train_epochs=args.epochs,        # passed from CLI
        learning_rate=args.lr,
        logging_dir="./logs",
        logging_steps=10,
        save_strategy="no",                  # avoid slow checkpointing
        disable_tqdm=False,                  # show progress bar
        report_to="none"                     # no WandB/Hub logging
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized
    )

    # Train and save model
    trainer.train()
    os.makedirs(SAVE_DIR, exist_ok=True)
    model.save_pretrained(SAVE_DIR)
    tokenizer.save_pretrained(SAVE_DIR)

    print(f"Fine-tuned model saved to: {SAVE_DIR}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to training data (.jsonl)")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--lr", type=float, default=3e-5)
    args = parser.parse_args()

    main(args)
