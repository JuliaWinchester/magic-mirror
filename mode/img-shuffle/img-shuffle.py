from PIL import Image, ImageTk
from os.path import join, isfile
from os import listdir
from random import choice
from threading import Timer 
from sys import argv, version_info
import time

# Version-dependent imports
if version_info.major == 3:
	import tkinter as tk
else:
	import Tkinter as tk

class ShuffleWindow:
	def __init__(self, t, img_dir):
		self.imgs = [join(img_dir, f) for f in listdir(img_dir) if isfile(join(img_dir,f)) and '.conf' not in f]
		self.l = None
		self.sw = 0
		self.sh = 0
		self.t = t
		self.init_GUI()

	def init_GUI(self):
		self.root = tk.Tk()
		self.root.attributes('-fullscreen', True)
		self.sw = self.root.winfo_screenwidth()
		self.sh = self.root.winfo_screenheight()
		self.l = tk.Label(self.root, width=self.sw, height=self.sh, bg="black")
		self.l.pack()
		Timer(1.0, self.image_loop).start()
		self.root.mainloop()
	
	def display_img(self, img_path):
		img = self.load_image(img_path)
		tk_img = ImageTk.PhotoImage(img)
		self.l.configure(image = tk_img)
		self.l.image = tk_img

	def image_loop(self):
		img_path = choice(self.imgs)
		self.display_img(img_path)
		Timer(self.t*60, self.image_loop).start()

	def load_image(self, img_path):
		img = Image.open(img_path)
		if img.width/self.sw > img.height/self.sh:
			new_width = self.sw
			new_height = float(self.sw)/float(img.width) * float(img.height)
		else:
			new_width =  float(self.sh)/float(img.height) * float(img.width)
			new_height = self.sh
		return img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

if __name__ == '__main__':
	shuffle_window = ShuffleWindow(float(argv[1]), argv[2])
