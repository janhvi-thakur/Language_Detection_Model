import pytesseract
from PIL import Image
import langid
from collections import Counter

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

LANGS = "hin+mar+guj+pan+tam+tel+kan+mal+ben+ori+san+eng"

code_to_lang = {
    "hi": "Hindi",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "or": "Odia",
    "sa": "Sanskrit",
    "en": "English"
}

INDIAN_LANGUAGES = [
    "Hindi", "Marathi", "Gujarati", "Punjabi", "Tamil",
    "Telugu", "Kannada", "Malayalam", "Bengali", "Odia",
    "Sanskrit", "English"
]

def detect_languages(image_path):

    text = pytesseract.image_to_string(Image.open(image_path), lang=LANGS)

    if not text.strip():
        return {"error": "No text detected in image"}

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    lang_counts = Counter()

    for line in lines:
        lang, _ = langid.classify(line)

        
        if line.isascii():
            lang = "en"

        lang_counts[lang] += len(line)

    total_chars = sum(lang_counts.values())

    percentages = {
        code_to_lang.get(lang, lang): round((count / total_chars) * 100, 2)
        for lang, count in lang_counts.items()
    }

    filtered_percentages = {
        lang: pct for lang, pct in percentages.items()
        if lang in INDIAN_LANGUAGES
    }

    if filtered_percentages:
        percentages = filtered_percentages

    dominant_language = max(percentages, key=percentages.get)
    dominant_percentage = percentages[dominant_language]

    return {
        "extracted_text": text,
        "percentages": percentages,
        "dominant_language": dominant_language,
        "dominant_percentage": dominant_percentage
    }
