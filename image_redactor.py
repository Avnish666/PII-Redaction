import os
import re
import gc
import shutil
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw

windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(windows_path):
    pytesseract.pytesseract.tesseract_cmd = windows_path
elif shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")
else:
    raise RuntimeError("Tesseract OCR not found.")

AADHAAR_NUMBER = r"\b\d{4}\s\d{4}\s\d{4}\b"

PAN_KEYWORDS = [
    "income tax department",
    "permanent account",
    "permanent account number",
]

MAX_WIDTH = 900


def redact_images():
    folder = "images"

    detector = cv2.QRCodeDetector()

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if not os.path.isfile(path):
            continue

        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        print(f"\n========== {file} ==========")

        try:

            img = Image.open(path)

            if img.mode != "RGB":
                img = img.convert("RGB")

            # Resize large images
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                img = img.resize(
                    (
                        MAX_WIDTH,
                        int(img.height * ratio),
                    ),
                    Image.Resampling.BILINEAR,
                )

            draw = ImageDraw.Draw(img)

            qr_detected = False

            # ---------- QR Detection ----------
            img_np = np.asarray(img)

            cv_img = cv2.cvtColor(
                img_np,
                cv2.COLOR_RGB2BGR,
            )

            del img_np

            success, decoded_info, points, _ = detector.detectAndDecodeMulti(
                cv_img
            )

            del cv_img

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

            # ---------- OCR ----------
            text = ""

            if not qr_detected:

                try:
                    text = pytesseract.image_to_string(
                        img,
                        config="--oem 3 --psm 6",
                    ).lower()

                except Exception as e:
                    print("OCR Error:", e)

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
                draw.rectangle(
                    [(0, 0), img.size],
                    fill="black",
                )

            if is_sensitive or qr_detected:
                img.save(path, optimize=True, quality=80)

            img.close()

            del draw
            del img

            gc.collect()

        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue