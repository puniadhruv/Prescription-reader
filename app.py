from flask import Flask, render_template, request
from prescription_reader import (
    preprocess_image,
    extract_text_from_image,
    find_medicines,
    calculate_confidence
)

import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    image = preprocess_image(filepath)

    extracted_text = extract_text_from_image(image)

    medicines = find_medicines(extracted_text)

    confidence = round(
        calculate_confidence(medicines),
        1
    )

    return render_template(
        "result.html",
        text=extracted_text,
        medicines=medicines,
        confidence=confidence
    )


if __name__ == "__main__":
    app.run(debug=True)