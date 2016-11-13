"""Control web app for magic mirror modes and functions

"""
import os
import subprocess
import json
from threading import Timer
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def main_page():
	return app.send_static_file('index.html')

@app.route('/status', methods=['POST'])
def status():
	cmd = 'cd ../mode/status && sh init.sh'
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	out,err = p.communicate()
	return out

@app.route('/reboot', methods=['POST'])
def reboot():
	def call_reboot():
		subprocess.Popen('sudo reboot', stdout=subprocess.PIPE, shell=True)
	Timer(10.0, call_reboot).start()
	return 'Rebooting in 10 seconds, goodbye!'

# Images shuffle album edit back-end functions
@app.route('/album')
def album_page():
	return app.send_static_file('album/album.html')

@app.route('/album/get-albums')
def get_albums():
	base_dir = 'static/album/assets/img_albums'
	dir_names = os.listdir(base_dir)
	albums = []
	for dir_name in dir_names:
		with open(os.path.join(base_dir, dir_name, dir_name+'.conf')) as f:
			data = json.load(f)
		albums.append({'name': data['name'], 'path': os.path.join(base_dir, dir_name)})
	return jsonify(albums=albums)

@app.route('/album/get-images')
def get_images():
	path = os.path.normpath(request.args.get('path'))
	base_dir = 'static/album/assets/img_albums'
	good_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir)]
	norm_dirs = [os.path.normpath(d) for d in good_dirs]
	if path not in norm_dirs:
		return 'Nope sorry'
	else:
		imgs = [os.path.join(path, f) for f in os.listdir(path) 
					if '.conf' not in f 
					and os.path.isfile(os.path.join(path, f))]
		img_dict = [{'src': img} for img in imgs]
		return jsonify(images=img_dict)

if __name__ == '__main__':
	app.run(host= '0.0.0.0')
