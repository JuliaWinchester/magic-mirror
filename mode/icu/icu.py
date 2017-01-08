from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import datetime
import threading
import time

# initialize camera and grab reference to raw capture
camera = PiCamera(resolution = (640,480), framerate = 16)
camera.hflip = True
camera.vflip = True
raw_capture = PiRGBArray(camera, size = (640, 480))
time.sleep(2.5)

class Polling:
	on = 1
	def turn_on(self):
		self.on = 1
	def turn_off(self):
		self.on = 0

# capture frames from camera, initializing background model if needed
avg = None
for f in camera.capture_continuous(raw_capture, format = 'bgr', use_video_port=True):
	frame = f.array
	motion_detected = 0

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if avg is None:
		avg = gray.copy().astype("float")
		raw_capture.truncate(0)
		continue

	# accumulate weighted average between current frame and previous frames,
	# then compute difference between current frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
	thresh = cv2.threshold(frame_delta, 5, 255, cv2.THRESH_BINARY)
	cv2.imshow('thresh', thresh[1])
	print(cv2.countNonZero(thresh[1]))
	
	if cv2.countNonZero(thresh[1]) > 10000 && Polling.on:
		# save the original frame image, turn off polling, turn it back on in 60 secs
		print('Saving image, not polling camera for 60 secs.')
		cv2.imwrite(datetime.datetime.now().strftime('%Y-%m-%d_H%H-M%M-S%S')+'.png', frame)
		Polling.turn_off()
		t = threading.Timer(60.0, Polling.turn_on)
		t.start()
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
		
	raw_capture.truncate(0)

camera.release()
cv2.destroyAllWindows()

