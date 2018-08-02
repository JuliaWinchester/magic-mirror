from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import datetime
import gc
import json
import subprocess
import threading
import time

class Panoptikun:
	def __init__(self, time_window = None):
		self.polling = 0
		self.app_launched = 0
		self.time_window = time_window
		self.frame_avg = None
		self.start_time = None
		self.cons_mov_frames = 0
		self.wake()
		self.capture_loop()
		
	def init_camera(self):
		self.camera = PiCamera(resolution = (640,480), framerate = 16)
		self.raw_capture = PiRGBArray(self.camera, size = (640, 480))
		time.sleep(5)

	def sleep(self, secs):
		self.kill_camera()
		time.sleep(secs)
		self.wake()

	def sleep_until(self, hour):
		self.kill_camera()
		gc.collect()
		cur_time = datetime.datetime.now()
		wake_time = cur_time.replace(hour=5)
		delta_time = wake_time - cur_time
		if delta_time.total_seconds() >= 0:
			time.sleep(delta_time.total_seconds())
			self.wake()
		else:
			time.sleep(86400.0 + delta_time.total_seconds())
			self.wake()

	def wake(self):
		self.set_polling_off()
		self.init_camera()
		if self.time_window is not None:
			self.start_time = datetime.datetime.now()
		threading.Timer(10.0, self.set_polling_on).start()		

	def kill_camera(self):
		self.camera.close()

	def set_polling_on(self):
		self.polling = 1

	def set_polling_off(self):
		self.polling = 0

	def launch_app(self):
		print('launching app')
		cur_time = datetime.datetime.now()
		def sys_launch(app):
			cmd = 'export DISPLAY=:0.0; /opt/vc/bin/tvservice -o; tmux kill-session -t mode; cd ../mode/' + app + '; sh init.sh; /opt/vc/bin/tvservice -p; sleep 5; xset dpms force on; xset -dpms'
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
			out,err = p.communicate()
			return out

		rand = 0
		if (
		     (cur_time.hour >= 5 and cur_time.hour <= 11) or 
		     (cur_time.hour >= 16 and cur_time.hour <= 19)
		   ):
			app = 'status'
		else: 
			app_conf = json.load(open('conf.json', 'r'))
			if app_conf['app_last'] and app_conf['app_last_time']:
				cur_time = datetime.datetime.now()
				start_time = datetime.datetime.strptime(app_conf['app_last_time'], "%Y-%m-%dT%H:%M:%S.%f")
				if (cur_time - start_time).total_seconds() < 10800:
					app = app_conf['app_last']
				else:
					rand = 1
			else: 
				rand = 1

		if rand:
			app = 'img_shuffle'
			json.dump({'app_last': '', 'app_last_time': ''}, open('conf.json', 'w'))

		sys_launch(app)
		self.app_launched = 1
		self.time_window = 5 * 60

	def kill_app(self):
		print('killing app')
		cmd = 'export DISPLAY=:0.0; /opt/vc/bin/tvservice -o; tmux kill-session -t mode'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		out,err = p.communicate()
		self.app_launched = 0
		self.time_window = None

	def moving_pixels(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		if self.frame_avg is None:
			self.frame_avg = gray.copy().astype("float")
			self.raw_capture.truncate(0)
			return 0

		# accumulate weighted average between current frame and previous frames,
		# then compute difference between current frame and running average
		cv2.accumulateWeighted(gray, self.frame_avg, 0.5)
		frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.frame_avg))
		thresh = cv2.threshold(frame_delta, 5, 255, cv2.THRESH_BINARY)
		return cv2.countNonZero(thresh[1])

	def capture_loop(self):
		for f in self.camera.capture_continuous(self.raw_capture, format = 'bgr', use_video_port=True):
			cur_time = datetime.datetime.now()
			if cur_time.hour >= 1 and cur_time.hour <= 5:
				print('snoozing, goodnight')
				self.sleep_until(5)

			p = self.moving_pixels(f.array)
			print(p)
			if p > 10000 and self.polling:
				self.cons_mov_frames += 1
				if self.cons_mov_frames == 3:
					if self.app_launched:
						print('motion detected while app is up, sleeping again')
						extra_sleep = self.time_window - (datetime.datetime.now() - self.start_time).total_seconds()
						self.sleep(15 * 60 + extra_sleep)
					else:
						print('motion detected with no app, launching app')
						self.launch_app()
						self.sleep(15 * 60)
			else:
				self.cons_mov_frames = 0

			if self.time_window and (datetime.datetime.now() - self.start_time).total_seconds() >= (5 * 60):
				print('no motion in time window, killing app')
				self.kill_app()
				
			self.raw_capture.truncate(0)

if __name__ == "__main__":
    panoptikun = Panoptikun()
