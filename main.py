import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import speech_recognition as sr
import urllib


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
        return None


def text_to_action(text, actions):
    return None

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
    print 'files uploaded ' + str(request.files)
    file = request.files['post_file']
    # Check if the file is one of the allowed types/extensions
    text = ""
    if file:
        try:
            text = speech_to_text(file)
        except Exception:
            print "some error occured in processing"

        try:
            print 'file name is : ' + file.filename
            path_to_save = os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path_to_save)
        except Exception:
            print "Not a valid file"

        if text:
            print 'text that is recognized is ' + text
        else:
            print "No audio detected"
            text = "We couldn't recognize your voice"
            return "We couldn't recognize your voice"
    else:
        print "no file object found"
        text = "We couldn't recognize your voice"
        return "We couldn't recognize your voice"
    return urllib.quote(text, '')


if __name__ == '__main__':
    app.run(
        debug=True
    )
