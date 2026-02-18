# Digitalization of Old Odia Scriptures

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

📥 Step-by-Step Installation Guide
For Absolute Beginners (No Technical Knowledge)
### Step 1: Install Python
```
Go to python.org

Download Python 3.10 (scroll down to find Python 3.10)

IMPORTANT: Check ✅ "Add Python to PATH" during installation

Click "Install Now"

Wait for installation to complete
 ```

### Step 2: Download the Project
```
Go to the GitHub repository

Click the green "Code" button

Select "Download ZIP"

Extract the ZIP file to your Desktop

Rename the folder to IndicPhotoOCR (if needed)
```
### Step 3: Open Command Prompt
```
Windows:

Press Windows Key + R

Type cmd and press Enter

Type: cd Desktop\IndicPhotoOCR and press Enter

Mac:

Press Command + Space

Type terminal and press Enter

Type: cd Desktop/IndicPhotoOCR and press Enter
```
### Step 4: Create Virtual Environment (Recommended)
```
Copy and paste this command:

bash
py -3.10 -m venv indicphotoocr_env
Then activate it:
Windows:

bash
indicphotoocr_env\Scripts\activate
Mac/Linux:

bash
source indicphotoocr_env/bin/activate
You should see (indicphotoocr_env) at the beginning of your command line.
```
### Step 5: Install Required Packages
```
Copy and paste this command:

bash
python -m pip install streamlit Pillow IndicPhotoOCR
Wait for all packages to install (this may take 5-10 minutes).

Step 6: Run the App
Copy and paste this command:

bash
streamlit run app_streamlit.py
Your browser will automatically open with the app! 🎉
```

### 🎮 How to Use the App
Main Screen
When you open the app, you'll see two tabs:

✍️ Digitize Manuscript (for uploading new manuscripts)

📚 Manuscript Archive (for browsing saved manuscripts)
📤 Uploading a Manuscript
Go to "Digitize Manuscript" tab

Fill in manuscript details:

📖 Title: Name of the manuscript (e.g., "Odia Bible Verse")

👤 Author: Author name (or "Unknown")

📅 Year: Year of creation (e.g., "1455")

Upload an image:

Click "Browse files" or drag and drop

Select an image of Odia text (JPG, PNG, JPEG)

Maximum file size: 200MB

Preview your image - it will appear on screen

Click "✨ Extract & Archive Manuscript"

Wait while the OCR processes the image

Green success message appears when done

🎈 Balloons animation confirms success!

View extracted text - The Odia text appears below

📚 Browsing the Archive
Go to "Manuscript Archive" tab

View all manuscripts in elegant cards

Search using the search bar:

Search by title, author, or text content

Results update in real-time

Each manuscript card shows:

📸 Manuscript image

📖 Title with decorative underline

👤 Author name

📅 Year

🔤 Extracted text

📊 Word and character count


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
