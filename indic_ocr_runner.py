import sys
import os
import contextlib
from IndicPhotoOCR.ocr import OCR

image_path = sys.argv[1]

# Silence model logs
with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    ocr = OCR(device="cpu", identifier_lang="auto")
    result = ocr.ocr(image_path)

# ---- Extract ONLY Odia text ----
words = []

for line in result:
    if isinstance(line, list):
        for item in line:
            if isinstance(item, dict) and "text" in item:
                text = item["text"]
                # Odia Unicode range
                if any('\u0B00' <= ch <= '\u0B7F' for ch in text):
                    words.append(text)

final_text = " ".join(words)
final_text = " ".join(final_text.split())  # normalize spaces

print(final_text)
