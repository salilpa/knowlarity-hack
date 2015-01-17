import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import speech_recognition as sr


# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['wav', 'mp3'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def speech_to_text(speech_wav):
    r = sr.Recognizer()
    with sr.WavFile(speech_wav) as source:              # use "test.wav" as the audio source
        audio = r.record(source)
    try:
        return r.recognize(audio)   # recognize speech using Google Speech Recognition
    except LookupError:                                 # speech is unintelligible
        return "Could not understand audio"

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file:
        text = ""
        try:
            text = speech_to_text(file)
        except Exception:
            print "some error occured in processing"
        print 'file name is : ' + file.filename
        print 'text that is recognized is ' + text
        return text
    else:
        print "error"
        return "error"


if __name__ == '__main__':
    app.run(
        debug=True
    )
