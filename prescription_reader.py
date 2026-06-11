# =====================================================
# ADVANCED MEDICAL PRESCRIPTION READER (with folder support)
# =====================================================
import pandas as pd
import pytesseract
import cv2
import json
from PIL import Image
import re
import os
import numpy as np
from datetime import datetime
import sys
import tkinter as tk
from tkinter import filedialog

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
# -----------------------------------------------------
# 1️⃣ Setup Paths
# -----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Create output directory if missing
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tesseract OCR path (adjust if installed elsewhere)
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------------------------------
# 2️⃣ Load medicine database
# -----------------------------------------------------
MEDICINE_DB_PATH = "medicine_data.json"

if not os.path.exists(MEDICINE_DB_PATH):
    print("Medicine database not found!")
    exit()

with open(MEDICINE_DB_PATH, "r", encoding="utf-8") as file:
    MEDICINES = json.load(file)
# -----------------------------------------------------
# 3️⃣ Helper Functions
# -----------------------------------------------------
def preprocess_image(image_path):
    """
    Preprocess the image for better OCR:
    - Convert to grayscale
    - Resize for better readability
    - Apply adaptive thresholding
    - Denoise and sharpen
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize to make text clearer
    scale_percent = 200  # increase size 2x
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation=cv2.INTER_LINEAR)

    # Adaptive thresholding (better for uneven lighting)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 11
    )

    # Denoising
    denoised = cv2.medianBlur(thresh, 3)

    # Sharpen the image
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    return sharpened

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Prescription Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    return file_path

def extract_text_from_image(image):
    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(
    image,
    config=custom_config,
    lang='eng'
)

    return text

from difflib import SequenceMatcher

def find_medicines(extracted_text):
    found = []

    extracted_text = extracted_text.lower()

    for medicine_name, details in MEDICINES.items():
        if medicine_name.lower() in extracted_text:
            found.append((medicine_name, details))

    return found

def check_interactions(found_meds):
    interactions = []
    for i in range(len(found_meds)):
        med1, info1 = found_meds[i]
        for j in range(i + 1, len(found_meds)):
            med2, info2 = found_meds[j]
            if med2 in info1.get("interactions", []):
                interactions.append(f" Interaction: {med1} ↔ {med2}")
    return interactions

def check_contraindications(found_meds, patient_conditions=None):
    if patient_conditions is None:
        patient_conditions = []
    contraindications = []
    for med, info in found_meds:
        for cond in info.get("contraindications", []):
            if cond.lower() in [c.lower() for c in patient_conditions]:
                contraindications.append(f"{med} contraindicated for {cond}")
    return contraindications

def calculate_confidence(found_meds):
    if len(found_meds) == 0:
        return 0

    return min(95, 60 + (len(found_meds) * 10))

def format_prescription_report(found_meds, interactions, contraindications, extracted_text, confidence_score):
    report = []
    report.append("="*60)
    report.append("MEDICAL PRESCRIPTION REPORT")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*60)
    report.append("\n Extracted Text:\n")
    report.append(extracted_text)
    report.append("\n" + "-"*60)

    if found_meds:
        report.append("\n Medicines Identified:\n")
        for med, info in found_meds:
            report.append(f" Name: {med}")
            report.append(f"   Dosage: {info['dosage']}")
            report.append(f"   Instructions: {info['instructions']}")
            report.append(f"   Warning: {info['warning']}\n")
    else:
        report.append(" No known medicines detected.\n")

    if interactions:
        report.append("\n Drug Interactions Detected:")
        for i in interactions:
            report.append(i)

    if contraindications:
        report.append("\n Contraindications Detected:")
        for c in contraindications:
            report.append(c)

    report.append(f"\n Confidence Score: {confidence_score:.1f}%")
    report.append("\n Please verify all extracted data manually for safety before use.")
    report.append("="*60)
    return "\n".join(report)

def save_report(report, filename="prescription_report.txt"):
    report_path = os.path.join(OUTPUT_DIR, filename)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n Report saved to {report_path}")

# -----------------------------------------------------
# 4️⃣ Main Function
# -----------------------------------------------------
def main():
    image_path = select_image()
    print(f" Selected image: {image_path}")

    try:
        processed_img = preprocess_image(image_path)
    except FileNotFoundError as e:
        print(e)
        return

    extracted_text = extract_text_from_image(processed_img)
    print("\n Extracted Text:\n")
    print(extracted_text)

    found_meds = find_medicines(extracted_text)
    interactions = check_interactions(found_meds)

    patient_conditions = ["Liver disease", "Allergy to Ibuprofen"]
    contraindications = check_contraindications(found_meds, patient_conditions)

    confidence_score = calculate_confidence(found_meds)

    report = format_prescription_report(found_meds, interactions, contraindications, extracted_text, confidence_score)
    print("\n" + report)
    save_report(report)

# -----------------------------------------------------
# 5️⃣ Run Program
# -----------------------------------------------------
if __name__ == "__main__":
    main()