from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Upload Page
@app.route("/")
def upload():
    #form = UploadForm()
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)