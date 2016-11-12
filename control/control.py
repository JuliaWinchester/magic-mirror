"""Control web app for magic mirror modes and functions

"""
from subprocess import call
from flask import Flask
app = Flask(__name__)

@app.route('/')
def main_page():
	return app.send_static_file('index.html')

@app.route('/reboot', methods=['POST'])
def reboot():
	call('sudo reboot')
	return 'Rebooting!'

if __name__ == '__main__':
	app.run(host= '0.0.0.0')