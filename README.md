# 🛡️ PII Redaction Tool

A full-stack application that automatically detects and redacts Personally Identifiable Information (PII) from Microsoft Word (.docx) documents.

The application can redact sensitive text, detect sensitive information inside images using OCR, and automatically remove QR codes from embedded images.

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
http://127.0.0.1:5000
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
http://localhost:5173
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
