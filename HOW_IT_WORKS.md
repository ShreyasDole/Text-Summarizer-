# 📖 How It Works - Text Summarizer AI Tool

Welcome to **SummarizeAI**! This guide explains how the application works, breaking down its core functionalities, how it processes files, and how you can integrate **Google's Generative AI API** for text summarization. 🚀

---

## 🛠 Workflow Overview

1️⃣ **User Uploads a File**
   - The application supports **PDF** and **CSV** files.
   - Users can also enter text manually for summarization.

2️⃣ **Extracting Text from Files**
   - For **PDFs**, the app uses `PyPDF2` to extract text.
   - For **CSVs**, `pandas` reads and processes the file contents.

3️⃣ **Summarization using Google Generative AI API**
   - The extracted text is sent to the **Google AI API**, which processes and returns a concise summary.

4️⃣ **Displaying the Summary**
   - The summarized text is shown in the UI.
   - Users can copy or download the summary.

5️⃣ **Interactive UI**
   - The Flask app provides an easy-to-use web interface.
   - Supports drag-and-drop uploads and instant summarization. ⚡

---

## 🧩 Key Code Breakdown

### **1️⃣ Extracting Text from PDF**
```python
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text
```
✔️ **Explanation**: This function reads a PDF file, extracts text from each page, and combines it into a single string.

### **2️⃣ Processing CSV Files**
```python
import pandas as pd

def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return " ".join(df.astype(str).values.flatten())
```
✔️ **Explanation**: Converts all CSV data into a text format for summarization.

### **3️⃣ Sending Data to Google AI API**
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

def summarize_text(text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(text)
    return response.text
```
✔️ **Explanation**: This function sends the extracted text to **Google Generative AI (Gemini)** and returns a summarized version.

---

## 🔑 Getting the Google Generative AI API Key

🔹 Follow these steps to get your API key:

1️⃣ **Go to** [Google AI Studio](https://ai.google.dev/)
2️⃣ **Sign in** with your Google account.
3️⃣ **Generate an API Key** under the **API Keys** section.
4️⃣ Copy the key and replace `YOUR_API_KEY` in the code.

🔹 **Enable the API** in your Google Cloud Console if necessary.

---

## 🚀 Running the App

```bash
python app.py
```
🔹 Open `http://127.0.0.1:5000/` in your browser and start summarizing text instantly!

---

🔥 **Now you're all set! Enjoy using the AI-powered text summarizer!** 🚀

