# 🩺 Medical Prescription Reader

A Flask-based Medical Prescription Reader that uses Optical Character Recognition (OCR) to extract text from prescription images and identify medicines from a medicine database.

## 📌 Project Overview

Medical prescriptions are often handwritten and difficult to understand. This project helps digitize prescriptions by extracting text from images and identifying medicines along with their dosage, instructions, and warnings.

The system uses:

* Python
* Flask
* Tesseract OCR
* OpenCV
* JSON-based medicine database

---

## 🚀 Features

### ✅ OCR-Based Prescription Reading

* Extracts text from prescription images using Tesseract OCR.

### ✅ Medicine Recognition

* Detects medicines from the extracted text.
* Matches medicines with a predefined medicine database.

### ✅ Dosage & Instructions Display

* Shows dosage information.
* Displays medicine usage instructions.

### ✅ Warning Detection

* Displays medicine warnings and precautions.

### ✅ Confidence Score

* Generates a confidence score based on detected medicines.

### ✅ Prescription Report Generation

* Generates a formatted prescription report.

### ✅ Web-Based Interface

* Upload prescription images through a Flask web application.

---

## 🛠️ Technologies Used

* Python 3
* Flask
* OpenCV
* Pytesseract
* JSON
* HTML/CSS

---

## 📂 Project Structure

```text
prescription_reader/
│
├── app.py
├── prescription_reader.py
├── medicine_data.json
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── uploads/
│
├── output/
│
└── static/
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/puniadhruv/Prescription-reader.git
cd Prescription-reader
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

Download and install Tesseract OCR for Windows:

https://github.com/UB-Mannheim/tesseract/wiki

Update the path in:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## ▶️ Running the Application

Start Flask server:

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

Upload a prescription image and click **Analyze Prescription**.

---

## 📋 Sample Medicines Supported

* Paracetamol
* Cefixime
* Azithromycin
* Ibuprofen
* Razo DSR
* Pan DSR
* Cetirizine
* Levocetirizine
* Pantoprazole
* Omeprazole
* Metformin
* Amlodipine
* Losartan
* Telmisartan
* Atorvastatin
* Rosuvastatin
* Diclofenac
* Aceclofenac
* Vitamin D3
* Calcium

---

## 📸 Sample Workflow

1. Upload Prescription Image
2. OCR Extracts Text
3. Medicine Recognition
4. Dosage & Warning Display
5. Confidence Score Generation
6. Report Generation

---

## 🔮 Future Improvements

* Handwritten prescription recognition using AI models
* Drug interaction analysis
* Allergy checking
* PDF report generation
* Medicine recommendation engine
* Cloud deployment

---

## 👨‍💻 Developer

**Dhruv Punia**

* GitHub: https://github.com/puniadhruv
* LinkedIn: https://www.linkedin.com/in/dhruv-punia-b15a54352

---

## 📄 License

This project is developed for educational purposes.
