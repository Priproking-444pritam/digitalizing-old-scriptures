from IndicPhotoOCR.ocr import OCR

from postprocess_odia import odia_to_paragraph


ocr = OCR(device="cpu", identifier_lang="auto")

result = ocr.ocr(r"C:\Users\KIIT0001\Desktop\AD lab\uploads\odia.jpg")

clean_text = odia_to_paragraph(result)

print("\nFINAL ODIA PARAGRAPH:\n")
print(clean_text)


