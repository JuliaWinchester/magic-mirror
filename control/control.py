"""Control web app for magic mirror modes and functions

"""
import os
import subprocess
import json
import shutil
from threading import Timer
from flask import Flask
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
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

@app.route('/get-control-conf')
def get_control_conf():
	if os.path.isfile('static/control.conf'):
		with open('static/control.conf','r') as f:
			data = json.load(f)
		return jsonify(data)
	else:
		return 'No conf file found'

@app.route('/image-shuffle', methods=['POST'])
def image_shuffle():
	data = request.get_json()
	with open('static/control.conf','w') as f:
		json.dump(data, f)
	path = data['conf']['album']['path']
	if validate_album_path(path):
		sh_path = os.path.join('../../control/', path)
		cmd = 'cd ../mode/img-shuffle && sh init.sh ' + str(data['conf']['minBtwnShuffle']) + " " + sh_path
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		out,err = p.communicate()
		return out
	else:
		return 'Invalid directory path'


# Images shuffle album edit back-end functions

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif','bmp','tiff'])

def validate_album_path(path):
	path = os.path.normpath(path)
	base_dir = 'static/album/assets/img_albums'
	good_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir)]
	norm_dirs = [os.path.normpath(d) for d in good_dirs]
	if path not in norm_dirs:
		return False
	else:
		return True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
	if validate_album_path(path):
		imgs = [os.path.join(path, f) for f in os.listdir(path) 
			if '.conf' not in f 
			and os.path.isfile(os.path.join(path, f))]
		img_dict = [{'src': img} for img in imgs]
		return jsonify(images=img_dict)
	else:
		return 'Nope sorry'

@app.route('/album/upload-image', methods=['POST'])
def upload_image():
	path = os.path.normpath(request.form.get('album'))
	if not validate_album_path(path):
		return 'No valid path'
	if 'file' not in request.files:
		return 'No file part in request'
	file = request.files['file']
	if file.filename == '':
		return 'No file uploaded'
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(path, filename))
		return 'File uploaded'

@app.route('/album/delete-image', methods=['POST'])
def delete_image():
	img_path = os.path.normpath(request.get_json()['image'])
	if validate_album_path(os.path.split(img_path)[0]) and os.path.isfile(img_path):
		os.remove(img_path)
		return 'File deleted'
	else:
		return 'Invalid image path'

@app.route('/album/new-album', methods=['POST'])
def new_album():
	album_name = request.get_json()['albumName']
	album_tail = secure_filename(album_name)
	base_dir = 'static/album/assets/img_albums'
	if not os.path.isdir(os.path.join(base_dir,album_tail)):
		os.mkdir(os.path.join(base_dir,album_tail))
		with open(os.path.join(base_dir,album_tail,album_tail+'.conf'),'w') as f:
			f.write('{ "name": "' + album_name + '" }')
		return 'Album created'
	else:
		return 'Directory already exists'
	return request.get_json()['albumName']

@app.route('/album/delete-album', methods=['POST'])
def delete_album():
	path = os.path.normpath(request.get_json()['path'])
	if validate_album_path(path) and os.path.isdir(path):
		shutil.rmtree(path)
		return 'Album deleted'
	else:
		return 'Invalid directory path'

if __name__ == '__main__':
	app.run(host= '0.0.0.0')
