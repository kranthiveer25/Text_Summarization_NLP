from flask import Flask, render_template, request
from text_summary import summarizer
import PyPDF2
import docx

app = Flask(__name__)

def extract_text_from_file(file):
    """Extracts text from a file (PDF, TXT, DOCX)"""
    if file.filename.endswith('.txt'):
        return file.read().decode("utf-8")
    elif file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    summary, original_txt, len_orig_txt, len_summary = "", "", 0, 0
    if request.method == 'POST':
        rawtext = request.form.get("rawtext", "")
        file = request.files.get("file")

        if file and file.filename:
            rawtext = extract_text_from_file(file)

        if rawtext:
            summary, original_txt, len_orig_txt, len_summary = summarizer(rawtext)

    return render_template("summary.html", summary=summary, original_txt=original_txt, len_orig_txt=len_orig_txt, len_summary=len_summary)

if __name__ == "__main__":
    app.run(debug=True)
