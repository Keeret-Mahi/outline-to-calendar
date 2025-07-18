from flask import Flask, render_template, flash, redirect, request, session, url_for
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

from forms import UploadForm
from outline_parser import extract_section_info
from calendar_utils import make_calendar


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads' 

# Upload Outlines Page
@app.route("/", methods=["GET", "POST"])
def upload():
    form = UploadForm()


    if form.validate_on_submit():
        uploaded_files = []

        for file in form.outlines.data:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            uploaded_files.append(filename)

        session['uploaded_files'] = uploaded_files
        return redirect("sections") 

    
    return render_template("upload.html", title="Outline -> Calendar", form=form)

# Section Numbers Page
@app.route("/sections", methods=['GET'])
def success():
    files = session.get('uploaded_files', [])
    return render_template("sections.html", uploaded_files=files)

# Process Sections
@app.route('/process_sections', methods=['POST'])
def process_sections():
    total = int(request.form['total_files'])
    info_list = []

    for i in range(1, total + 1):
        filename = request.form.get(f'filename_{i}')
        section = request.form.get(f'section_{i}')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            try:
                info = extract_section_info(soup, section)
                info_list.append(info)
            except ValueError as e:
                flash(f"{filename}: {str(e)}", "error")
                return redirect(url_for('errors'))

    return make_calendar(info_list)

# Error Messags
@app.route('/errors')
def errors():
    return render_template("errors.html")

# Debug
if __name__ == "__main__":
    app.run(debug=True)
