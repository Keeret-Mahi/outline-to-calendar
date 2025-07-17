from flask import Flask, render_template, flash, redirect, request
from dotenv import load_dotenv
import os
from forms import UploadForm
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads' 

@app.route("/", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        files_filenames = []
        for file in form.outlines.data:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            files_filenames.append(filename)
        flash("File(s) uploaded successfully!", "success")
        print("Uploaded files:", files_filenames)
        return redirect("/")  # redirect after POST to avoid form resubmission
    return render_template("upload.html", title="Outline -> Calendar", form=form)

if __name__ == "__main__":
    app.run(debug=True)
