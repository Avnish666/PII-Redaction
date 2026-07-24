from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from main import process_document

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return {
        "message": "PII Redaction API is running"
    }


@app.route("/redact", methods=["POST"])
def redact():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)

    input_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "redacted_" + filename
    )

    file.save(input_path)

    process_document(
        input_path,
        output_path
    )

    return send_file(
        output_path,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)