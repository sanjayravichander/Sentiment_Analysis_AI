import streamlit as st
import requests

st.set_page_config(
    page_title="AI Sentiment Analyzer",
    layout="centered",
    page_icon="🔍"
)

st.markdown(
    """
    <style>
    .flip-box {
        background-color: transparent;
        width: 300px;
        height: 100px;
        perspective: 1000px;
        margin: auto;
    }
    .flip-box-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }
    .flip-box:hover .flip-box-inner {
        transform: rotateY(180deg);
    }
    .flip-box-front, .flip-box-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 28px;
        font-weight: bold;
        border-radius: 10px;
    }
    .flip-box-front {
        background-color: #f2f2f2;
    }
    .flip-box-back {
        transform: rotateY(180deg);
    }

    .bar-container {
        width: 100%;
        background-color: #eee;
        border-radius: 5px;
        overflow: hidden;
        margin-top: 15px;
    }
    .bar {
        height: 25px;
        transition: width 0.8s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>🔮 Real-Time Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Type your thoughts below and watch AI react instantly...</p>", unsafe_allow_html=True)

# Input box
text = st.text_area("📝 Your message:", height=150, placeholder="e.g., I love this product!")

if text.strip():
    try:
        #res = requests.post("http://localhost:8000/predict", json={"text": text})
        res = requests.post("http://backend:8000/predict", json={"text": text})
        result = res.json()
        label = result["label"].lower()
        score = round(result["score"], 4)

        emoji_map = {
            "positive": "😄",
            "negative": "😠",
            "neutral": "😐",
            "uncertain": "🤔"
        }
        color_map = {
            "positive": "#2ecc71",  # green
            "negative": "#e74c3c",  # red
            "neutral": "#f1c40f",   # yellow
            "uncertain": "#95a5a6"
        }

        emoji = emoji_map.get(label, "🤔")
        color = color_map.get(label, "#bdc3c7")
        bar_width = int(score * 100)

        # Flip animation block
        st.markdown(f"""
        <div class="flip-box">
            <div class="flip-box-inner">
                <div class="flip-box-front">
                    {emoji} {label.capitalize()}
                </div>
                <div class="flip-box-back" style="background-color:{color}; color: white;">
                    Confidence: {score}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Confidence bar
        st.markdown(f"""
        <div class="bar-container">
            <div class="bar" style="width: {bar_width}%; background-color: {color};"></div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error("❌ Error contacting backend.")
        st.exception(e)
else:
    st.info("Start typing in the box above to get sentiment predictions.")
