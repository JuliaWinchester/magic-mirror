"""Control web app for magic mirror modes and functions

"""
import subprocess
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def main_page():
	return app.send_static_file('index.html')

@app.route('/reboot', methods=['POST'])
def reboot():
	if request.remote_addr == "192.168.0.100":
		cmd = "sudo reboot"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		if output == "":
			output = "missing"
		return output
	else:
		return request.remote_addr

if __name__ == '__main__':
	app.run(host= '0.0.0.0')