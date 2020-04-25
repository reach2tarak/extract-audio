from flask import Flask, Response, render_template, url_for, request
from vosk import Model, KaldiRecognizer
import sys
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
     return render_template('home.html')


@app.route('/extract_audio', methods=['POST'])
def extract_audio():
	f = request.files['video_file']
	f.save(f.filename)

	now = datetime.now()
	timestamp = datetime.timestamp(now)

	output_file = "audio_"+str(int(timestamp))+".wav"

	command = "ffmpeg -i " + f.filename + " -ar 16000 -acodec pcm_s16le -f wav " + output_file
	subprocess.call(command, shell=True)
	
	if os.path.isfile(output_file):
		model = Model("model-en")
		rec = KaldiRecognizer(model, 16000)
		wf = open(output_file, "rb")
		wf.read(44)
		while True:
		    data = wf.read(2000)
		    if len(data) == 0:
		        break
		    if rec.AcceptWaveform(data):
		        res = json.loads(rec.Result())
		
		output = rec.Result()
		os.remove(f.filename)
		os.remove(output_file)
	else:
		output = "Audio file couldn't generate"	

	
	return render_template('result.html', output = output)

if __name__ == '__main__':
	app.run(debug=False)     