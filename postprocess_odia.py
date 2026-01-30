def odia_to_paragraph(ocr_output):
    """
    Input: OCR output list from IndicPhotoOCR
    Output: Clean Odia paragraph string
    """

    words = []

    for line in ocr_output:
        for word in line:
            # Remove non-Odia junk
            if any('\u0B00' <= ch <= '\u0B7F' for ch in word):
                words.append(word.strip())

    paragraph = " ".join(words)

    # Fix common OCR spacing issues
    paragraph = paragraph.replace("  ", " ")

    return paragraph.strip()
