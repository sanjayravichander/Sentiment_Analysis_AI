import re

def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)

    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#', '', text)

    # Keep digits only if:
    # - They're part of currency (e.g. $199)
    # - Percentages (e.g. 90%)
    # - Decimal ratings (e.g. 4.5 stars)
    # So we remove all other standalone numbers

    # Remove numbers NOT next to %, $, or decimals
    text = re.sub(r'(?<![\d$%])\b\d+\b(?![%\.])', '', text)

    # Remove special characters except basic punctuation
    text = re.sub(r"[^a-zA-Z0-9.,!?'\"]+", ' ', text)

    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text
