from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def handle_incoming_call():
    response = VoiceResponse()

    gather = Gather(
        action='/handle-keypress',
        method='POST',
        num_digits=1,
        timeout=5
    )
    gather.say("Press 1 to start analysing soil. Press 2 to fetch the sensor data")
    response.append(gather)
    response.say("We didn't receive any input. Goodbye.")

    return Response(str(response), mimetype='text/xml')

@app.route("/handle-keypress", methods=['POST'])
def handle_keypress():
    digit_pressed = request.form.get('Digits')
    caller = request.form.get('From')

    response = VoiceResponse()

    if digit_pressed == '1':
        response.say("You selected one, strating analysis ")
        requests.get('https://moisure-data-backend.onrender.com/trigger-analysis')
    elif digit_pressed == '2':
        response.say("You selected  two,sending data via sms ")
        requests.post('https://twilio-appwrite-backend.onrender.com/api/create-user-and-send')
    else:
        response.say("Invalid input. Goodbye.")

    return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)
