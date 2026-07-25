# 🛡️ PII Redaction Tool

A full-stack application that automatically detects and redacts Personally Identifiable Information (PII) from Microsoft Word (.docx) documents.

The application can redact sensitive text, detect sensitive information inside images using OCR, and automatically remove QR codes from embedded images.

---


## Update

The frontend is deployed on Vercel. The backend has been thoroughly tested and functions correctly in a local environment. The application relies on Tesseract OCR, OpenCV, and image processing for document redaction, which can exceed the memory limits of free cloud hosting services during OCR-intensive workloads. The submitted output document was generated using the same codebase running locally. To run the project locally, start the Flask backend (`python app.py`) and configure the frontend API endpoint to `http://127.0.0.1:10000/redact`. Smaller documents will work just fine on the render backend.


---

## 📸 Application Preview

![PII Redaction Tool](https://github.com/Avnish666/PII-Redaction/blob/3fdc9e4b364987c666e5ebfd52d211d69107b625/Screenshot%202026-07-24%20232145.png)

---

## Features

- 📄 Upload DOCX documents
- 🔍 Detect and redact:
  - Person Names
  - Email Addresses
  - Phone Numbers
  - Credit Card Numbers
  - SSNs
  - IP Addresses
  - Dates of Birth
- 🖼 OCR-based image redaction using Tesseract OCR
- 📱 QR Code detection and redaction
- ⚡ Flask REST API
- 💻 React frontend
- 📥 Automatically downloads the redacted document

---

## Tech Stack

### Backend

- Python
- Flask
- python-docx
- spaCy
- pytesseract
- OpenCV
- Pillow
- Regex

### Frontend

- React
- Vite
- Axios
- CSS

---

## Project Structure

```
PIR_Redaction/
│
├── app.py
├── main.py
├── detector.py
├── replacer.py
├── reader.py
├── image_redactor.py
├── extract_images.py
├── replace_images.py
│
├── frontend/
│
├── uploads/
├── output/
├── images/
└── input/
```

---

## Installation

### Backend

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Backend runs on:

```
https://pii-redaction-rt46.onrender.com
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on:

```
https://pii-redaction-9vznkd7xu-avnish666s-projects.vercel.app/
```

---

## Workflow

```
DOCX Upload
      │
      ▼
Extract Images
      │
      ▼
QR Detection
      │
      ▼
OCR using Tesseract
      │
      ▼
PII Detection
      │
      ▼
Redaction
      │
      ▼
Reinsert Images
      │
      ▼
Download Redacted DOCX
```

---
