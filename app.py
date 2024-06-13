import os
import pandas as pd
from PyPDF2 import PdfReader
from flask import Flask, render_template, request
import google.generativeai as genai

# Configure the API key for the Google Generative AI service
genai.configure(api_key='Enter your own API KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def read_pdf(file_path, chunk_size=50):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        total_pages = len(reader.pages)
        for start_page in range(0, total_pages, chunk_size):
            end_page = min(start_page + chunk_size, total_pages)
            chunk_text = ""
            for page_num in range(start_page, end_page):
                chunk_text += reader.pages[page_num].extract_text()
            text += chunk_text + "\n\n"
    return text

def read_csv(file_path, chunk_size=50):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunks.append(chunk.to_string(index=False))
    return '\n\n'.join(chunks)

def summarize_text_chunks(text):
    chunk_summaries = []
    chunks = text.split('\n\n')
    for chunk in chunks:
        prompt = "Summarize the following text:\n\n" + chunk
        try:
            response = genai.generate_text(model='models/text-bison-001', prompt=prompt)
            chunk_summaries.append(response.result)
        except Exception as e:
            print(f"Error generating summary for chunk: {str(e)}")
            chunk_summaries.append("Error generating summary")
    final_summary = '\n'.join(chunk_summaries[:10])  # Change to first 10 chunk summaries
    return final_summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    summary = None
    error = None
    if request.method == 'POST':
        file = request.files.get('file')
        prompt = request.form.get('prompt')

        if file and file.filename != '':
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(file_path)

            if filename.endswith('.pdf'):
                text = read_pdf(file_path)
            elif filename.endswith('.csv'):
                text = read_csv(file_path)
            else:
                error = "Unsupported file type. Please upload a PDF or CSV file."
                return render_template('index.html', error=error)

            try:
                summary = summarize_text_chunks(text)
            except Exception as e:
                error = f"An error occurred during summarization: {str(e)}"
                return render_template('index.html', error=error)
        elif prompt:
            try:
                summary = summarize_text_chunks(prompt)
            except Exception as e:
                error = f"An error occurred during summarization: {str(e)}"
                return render_template('index.html', error=error)
        else:
            error = "Please upload a file or enter a prompt."
            return render_template('index.html', error=error)

    return render_template('index.html', summary=summary, error=error)

if __name__ == '__main__':
    app.run(debug=True)
