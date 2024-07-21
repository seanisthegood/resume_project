from flask import Flask, request, render_template
import openai
from dotenv import load_dotenv
import os

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
    resume = request.files['resume'].read().decode('utf-8')
    simplified_resume = simplify_resume(resume)
    return render_template('result.html', original=resume, simplified=simplified_resume)

def simplify_resume(resume):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following resume into a simple, no-bullshit version:\n\n{resume}",
        max_tokens=1024
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
