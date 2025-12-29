import re
from bs4 import BeautifulSoup

def clean_html(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ")

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_description(html_text: str) -> str:
    text = clean_html(html_text)
    return normalize_text(text)

