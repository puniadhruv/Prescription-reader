Medical Prescription Reader

This project reads a handwritten or printed medical prescription image,
extracts text using Tesseract OCR, detects known medicine names from a
small database, and displays dosage and safety warnings.

Steps to Run:
1. Install dependencies:
   pip install -r requirements.txt

2. Ensure Tesseract OCR is installed and added to PATH.
   Example path: C:\Program Files\Tesseract-OCR\tesseract.exe

3. Run the script:
   python prescription_reader.py

4. The program will display extracted text, found medicines, dosage info,
   warnings, and a confidence score.

Developed by: Dhruv
For class assignment submission ✅
