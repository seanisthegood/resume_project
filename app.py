from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import pymupdf # PyMuPDF for PDF
from docx import Document  # python-docx for DOCX

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']
    file_type = file.filename.split('.')[-1].lower()
    if file_type == 'txt':
        resume = file.read().decode('utf-8')
    elif file_type == 'pdf':
        resume = extract_text_from_pdf(file)
    elif file_type == 'docx':
        resume = extract_text_from_docx(file)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    simplified_resume = simplify_resume(resume)
    return jsonify({
        'original': resume,
        'simplified': simplified_resume
    })

def extract_text_from_pdf(file):
    doc = pymupdf.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text

def simplify_resume(resume):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following resume into a simple, no-bullshit version:\n\n{resume}",
        max_tokens=1024
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
