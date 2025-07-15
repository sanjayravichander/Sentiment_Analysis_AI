from fastapi import FastAPI
from pydantic import BaseModel
from .model import load_sentiment_pipeline


app = FastAPI()

# Load the pipeline
sentiment_pipeline = load_sentiment_pipeline()

# ✅ Add this root route just below app initialization
@app.get("/")
def root():
    return {"message": "Sentiment Analysis API is running. Visit /docs for Swagger UI."}

# Define request schema
class TextRequest(BaseModel):
    text: str

# Define prediction endpoint
@app.post("/predict")
def predict_sentiment(request: TextRequest):
    result = sentiment_pipeline(request.text)[0]
    return {
        "label": result["label"].lower(),
        "score": round(result["score"], 4)
    }
