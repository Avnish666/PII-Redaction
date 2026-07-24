import os
import re

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

AADHAAR_NUMBER = r"\b\d{4}\s\d{4}\s\d{4}\b"

PAN_KEYWORDS = [
    "income tax department",
    "permanent account",
    "permanent account number",
]


def redact_images():
    folder = "images"

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if not os.path.isfile(path):
            continue

        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        img = Image.open(path).convert("RGB")
        draw = ImageDraw.Draw(img)


        qr_detected = False

        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        detector = cv2.QRCodeDetector()

        success, decoded_info, points, _ = detector.detectAndDecodeMulti(cv_img)

        if success and points is not None:

            print(">> QR Code Detected")

            qr_detected = True

            for qr in points:

                x_min = int(np.min(qr[:, 0]))
                y_min = int(np.min(qr[:, 1]))
                x_max = int(np.max(qr[:, 0]))
                y_max = int(np.max(qr[:, 1]))

                draw.rectangle(
                    [(x_min, y_min), (x_max, y_max)],
                    fill="black",
                )

        text = pytesseract.image_to_string(img).lower()

        print(f"\n========== {file} ==========")
        print(text)

        is_sensitive = False

        if (
            re.search(AADHAAR_NUMBER, text)
            and ("male" in text or "female" in text)
        ):
            print(">> Aadhaar Card Detected")
            is_sensitive = True

        elif any(keyword in text for keyword in PAN_KEYWORDS):
            print(">> PAN Card Detected")
            is_sensitive = True

        else:
            print(">> Normal Image")


        if is_sensitive:
            draw.rectangle([(0, 0), img.size], fill="black")

        if is_sensitive or qr_detected:
            img.save(path)