from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    outlines = MultipleFileField(
        'Upload Outlines as HTML Files (up to 20)',
        validators=[FileRequired(), FileAllowed(['html', 'htm'], 'HTML only!')])
    submit = SubmitField('Next')