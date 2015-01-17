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
import getcosine


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
    with sr.WavFile(speech_wav) as source:  # use "test.wav" as the audio source
        audio = r.record(source)
    try:
        return r.recognize(audio)  # recognize speech using Google Speech Recognition
    except LookupError:  # speech is unintelligible
        return None


def text_to_action(text):
    phrase_ques = []
    phrase_ques.append("We couldn't recognize your voice")
    phrase_ques.append("When is delivery time for pizza")
    phrase_ques.append("What is the cost of Macbook")
    phrase_ques.append("What is the delivery address for my order")
    phrase_ques.append("Hello world")
    phrase_ques.append("When is next Bus for Goa?")
    phrase_ques.append("Book an appointment for surgeon")
    phrase_ques.append("What is the tracking status of my last order")
    phrase_ques.append("Book a table for two for the evening")
    phrase_ques.append("I have lost my credit card")
    phrase_ques.append("I want a new credit card")

    phrase_ans = []
    phrase_ans.append("We couldn't recognize your voice. Try again?")
    phrase_ans.append("Delivery time is Wednesday 14th of January")
    phrase_ans.append("Macbook costs 1.5 lakhs")
    phrase_ans.append("Delivery address is MG Road Bangalore")
    phrase_ans.append("Hello indeed, good friend. Why don't you ask me a question?")
    phrase_ans.append("Next Bus is at 8 pm today")
    phrase_ans.append("Your doctor appointment has been fixed.")
    phrase_ans.append("Your order will be delivered tomorrow.")
    phrase_ans.append("Your Booking has been confirmed.")
    phrase_ans.append("Do not worry. Your credit card has been blocked")
    phrase_ans.append("Your request for a new credit card has been placed.")


    inputString = text
    maxIndex = -1
    maxScore = 0
    index = 0
    for ques in phrase_ques:
        score = getcosine.get_matching(ques, inputString)
        if (score > maxScore):
            maxScore = score
            maxIndex = index
        index = index + 1

    if (maxIndex > -1):
        print "Matched question is", phrase_ques[maxIndex]
        print "Response is", phrase_ans[maxIndex]
    else:
        print "No Match found"
        maxIndex = 0
    return phrase_ans[maxIndex]


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
            path_to_save = os.path.join(os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'],
                                        file.filename)
            file.save(path_to_save)
        except Exception:
            print "Not a valid file"

        if text:
            print 'text that is recognized is ' + text
        else:
            print "No audio detected"
            text = "We couldn't recognize your voice"
    else:
        print "no file object found"
        text = "We couldn't recognize your voice"
    return urllib.quote(text_to_action(text), '')


if __name__ == '__main__':
    app.run(
        debug=True
    )
