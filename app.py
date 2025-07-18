from flask import Flask, render_template, flash, redirect, request, session
from dotenv import load_dotenv
import os
from forms import UploadForm
from werkzeug.utils import secure_filename

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
        #flash("File(s) uploaded successfully!", "success")
        #print("Uploaded files:", uploaded_files)
    
    return render_template("upload.html", title="Outline -> Calendar", form=form)

# Section Numbers Page
@app.route("/sections")
def success():
    files = session.get('uploaded_files', [])
    return render_template("sections.html", uploaded_files=files)

# Process Sections
@app.route('/process_sections', methods=['POST'])
def process_sections():
    total = int(request.form['total_files'])
    file_section_pairs = []

    for i in range(1, total + 1):
        filename = request.form.get(f'filename_{i}')
        section  = request.form.get(f'section_{i}')
        file_section_pairs.append((filename, section))

    # Do something with file_section_pairs
    return render_template('summary.html', data=file_section_pairs)


# Debug
if __name__ == "__main__":
    app.run(debug=True)
