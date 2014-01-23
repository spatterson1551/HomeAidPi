from TextToSpeech import *
from flask import Flask
from flask import render_template
from flask import request
import sys
from subprocess import call


app = Flask(__name__)
devices = ['Xbox', 'Projector']

@app.route("/")
def menu():
	return render_template("main.html", devices=devices)

@app.route("/<device_name>")
def remote(device_name):
	if device_name == "Xbox":
		return render_template("main.html/#Xbox")
	if device_name == "Projector":
		return render_template("main.html/#Projector")
	
@app.route("/<device_name>/clicked/<op>")
def sendCommand(device_name, op):
	call(["irsend", "SEND_ONCE", device_name, op])
	return ""

@app.route("/clicked/<message>")
def sayMessage(message):
	print message
	speakSpeechFromText(message)
	return ""
	
if __name__ == "__main__":
	app.run('0.0.0.0', port=80)
	