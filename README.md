# 🤖 Sentiment Analysis AI App

A complete end-to-end sentiment analysis system powered by a fine-tuned Transformer model. This app analyzes English text and classifies it as **positive**, **negative**, or **neutral** using a real-time web interface. It includes:

* HuggingFace Transformer fine-tuning
* FastAPI backend for inference
* Streamlit frontend with animated UI
* Dockerized deployment


## Features

* Fine-tuned `cardiffnlp/twitter-roberta-base-sentiment-latest` on 3-label data
* Real-time predictions via FastAPI (`/predict`)
* Streamlit UI with:

  * Emoji-based label
  * Confidence bar animation
  * Flip-in effect on sentiment change
* Fully containerized with Docker Compose

---

## Project Structure

```
Sentiment_Analysis_AI/
├── backend/
│   ├── app.py                # FastAPI app
│   ├── model.py              # Model loading logic
│   ├── model/                # Fine-tuned model saved here
│   └── __init__.py
├── ui.py                    # Streamlit frontend
├── finetune.py              # Fine-tuning script
├── run_all.py               # Local launcher script
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Requirements

* Python 3.10+
* Docker & Docker Compose (if containerized)

---

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Backend

```bash
uvicorn backend.app:app --reload --port 8000
```

### 3. Run Frontend (separate terminal)

```bash
streamlit run ui.py
```

Then go to [http://localhost:8501](http://localhost:8501).

---

## Dockerized Deployment

### 1. Build and Run All

```bash
docker-compose up --build
```

### 2. Open in Browser

* UI: [http://localhost:8501](http://localhost:8501)
* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Fine-tuning

Train a custom sentiment classifier:

```bash
python finetune.py \
  --data data/files/train_converted.jsonl \
  --epochs 3 \
  --lr 3e-5
```

Outputs saved in `backend/model/`

---

## Example API Call

```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "This product is awesome!"}'
```

**Response:**

```json
{
  "label": "positive",
  "score": 0.9823
}
```

---

## Troubleshooting

| Issue                 | Fix                                                      |
| --------------------- | -------------------------------------------------------- |
| ConnectionError in UI | Use `http://backend:8000` inside Docker, not `localhost` |
| Docker timeout        | Use `--default-timeout=300` in `Dockerfile`              |
| CORS/XSRF warning     | Safe to ignore unless deploying cross-domain             |

---

## Author

**Sanjay Ravichander**
Junior Machine Learning & Deep Learning Engineer

---

## License

MIT

---

