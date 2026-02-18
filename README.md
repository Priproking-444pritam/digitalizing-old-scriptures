# IndicPhotoOCR – Odia Scene Text Recognition

A lightweight implementation of IndicPhotoOCR focused on **Odia Scene Text Detection and Recognition**.

This project performs:

- Text Detection
- Script Identification
- Text Recognition (Odia)

---

## Language Supported

- Odia (Oriya)

---

## Installation

### 1. Create Virtual Environment (Recommended Python 3.9)

```bash
conda create -n indicphotoocr python=3.9 -y
conda activate indicphotoocr
```

OR using venv (Python 3.10):

```bash
py -3.10 -m venv indicphotoocr_env
indicphotoocr_env\Scripts\activate
```

---

### 2. Clone Repository

```bash
git clone https://github.com/Bhashini-IITJ/IndicPhotoOCR.git
cd IndicPhotoOCR
```

---

### 3. Install (CPU Version)

```bash
python setup.py sdist bdist_wheel
pip install dist/indicphotoocr-1.3.1-py3-none-any.whl[cpu]
```

---

## How to Use (Odia Only)

### Detection

```python
from IndicPhotoOCR.ocr import OCR

ocr_system = OCR(verbose=True, device="cpu")
detections = ocr_system.detect("test_images/image_141.jpg")
ocr_system.visualize_detection("test_images/image_141.jpg", detections)
```

---

### Odia Recognition

```python
from IndicPhotoOCR.ocr import OCR

ocr_system = OCR(verbose=True)
text = ocr_system.recognise("test_images/cropped_image/image_141_0.jpg", "odia")
print(text)
```

---

### End-to-End Odia OCR

```python
from IndicPhotoOCR.ocr import OCR

ocr_system = OCR(verbose=True, identifier_lang="auto")
result = ocr_system.ocr("test_images/image_141.jpg")
print(result)
```

---

## Dataset Reference

Bharat Scene Text Dataset (BSTD)  
https://github.com/Bhashini-IITJ/BharatSceneTextDataset

---

## Citation

```
@misc{ipo,
  author = {Anik De et al.},
  title = {IndicPhotoOCR: A comprehensive toolkit for Indian language scene text understanding},
  year = 2024
}
```

---

## Project Focus

This version is customized specifically for:

- Odia Scene Text Recognition
- Academic / Research Usage
- CPU-based inference

---

## Maintainer

Pritam Acharya
