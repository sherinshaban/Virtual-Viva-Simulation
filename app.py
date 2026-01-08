from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # to allow for web page send requests from browser
import google.generativeai as genai   # to use gemini
import PyPDF2
import docx
import os
import json

#------------------------------------------------------------#

# mean that files html exist with python file
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # to connect with server

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index2.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# ----------------------------gemini-----------------------------------------#

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})

# ---------------------------read file (pdf/docx)---------------------------------------#

def read_pdf(file_stream):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages[:30]: # Max 30 pages
            text += page.extract_text() or ""
    except Exception as e: return ""
    return text

def read_docx(file_stream):
    text = ""
    try:
        doc = docx.Document(file_stream)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e: return ""
    return text

# -----------------API----------------------------------------------------#
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename
    
    
    text = ""
    if filename.endswith('.pdf'):
        text = read_pdf(file)
    elif filename.endswith('.docx'):
        text = read_docx(file)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    if not text:
        return jsonify({"error": "Could not extract text"}), 400

    # send text to prompt
    prompt = """
    Act as a university professor. Analyze the text.
    Generate 3 diverse interview questions based on the content.
    Output purely JSON format: [{"question": "..."}]
    """
    try:
        full_prompt = f"{prompt}\n\nContent:\n{text}"
        response = model.generate_content(full_prompt)
        questions_json = json.loads(response.text)
        
        # show questoin in html
        return jsonify({"questions": questions_json})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/grade', methods=['POST'])
def grade_answer():
    # respond data from frontend
    data = request.json
    question = data.get('question')
    student_answer = data.get('answer')

    print(f"Question: {question}")
    print(f"Answer: {student_answer}")

    if not student_answer:
        return jsonify({"score": 0, "feedback": "Try Again"})

# evaluate the answer
    prompt = f"""
    Evaluate this answer for an interview.
    Question: {question}
    Answer: {student_answer}
    
    Output strictly JSON: {{"score": (0-10), "feedback": "Short feedback"}}
    """
    try:
        response = model.generate_content(prompt)
        
        clean_text = response.text.replace('```json', '').replace('```', '')
        result = json.loads(clean_text)
        return jsonify(result)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"score": 0, "feedback": "A correction error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)