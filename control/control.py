"""Control web app for magic mirror modes and functions

"""
import subprocess
from threading import Timer
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def main_page():
	return app.send_static_file('index.html')

@app.route('/reboot', methods=['POST'])
def reboot():
	def call_reboot():
		subprocess.Popen('sudo reboot', stdout=subprocess.PIPE, shell=True)
	Timer(10.0, call_reboot).start()
	return 'Rebooting in 10 seconds, goodbye!'
	
if __name__ == '__main__':
	app.run(host= '0.0.0.0')