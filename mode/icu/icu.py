from picamera.array import PiRGBArray
from picamera import picamera
import cv2
import time

# initialize camera and grab reference to raw capture
camera = PiCamera(resolution = (640,480), framerate = 16)
raw_capture = PiRGBArray(camera, size = (640, 480))
time.sleep(2.5)

# capture frames from camera, initializing background model if needed
avg = None
for f in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port=True):
	frame = f.array
	motion_detected = 0

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if avg is None:
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue

	# accumulate weighted average between current frame and previous frames,
	# then compute difference between current frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
	thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)

	cv2.imshow('Thresh', thresh)
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break

camera.release()
cv2.destroyAllWindows()

