from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os

MODEL_PATH = "C:\\Users\\DELL\\OneDrive\\Desktop\\Sentiment_Analysis_AI\\finetune\\files\\backend\\model"
DEFAULT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

def load_sentiment_pipeline():
    if os.path.exists(MODEL_PATH) and os.listdir(MODEL_PATH):
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    else:
        model = AutoModelForSequenceClassification.from_pretrained(DEFAULT_MODEL)
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
