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

class BetterLabel(tk.Label):
    def __init__(self, root, bg='black', image=''):
        self.w = root.winfo_screenwidth()
        self.h = root.winfo_screenheight()
        self.anim_playing = 0
        self.queued_image = None

        tk.Label.__init__(self, root, width=self.w, height=self.h, bg=bg)
        if image != "":
            self.set_image(image)
    
    def resize_image(self, pil_img):
        if float(pil_img.width)/float(self.w) > float(pil_img.height)/float(self.h):
            new_width = self.w
            new_height = float(self.w)/float(pil_img.width) * float(pil_img.height)
        else:
            new_width =  float(self.h)/float(pil_img.height) * float(pil_img.width)
            new_height = self.h
        return pil_img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

    def display_image(self, img):
        if self.queued_image == None:
            self.set_image(img)
            if self.anim_playing == 0:
                self.play_queued_image()

    def set_image(self, img):
        if img.lower()[-3:] == 'gif':
            self.set_anim(img)
        else:
            self.set_static(img)

    def set_static(self, img):
        pil_img = self.resize_image(Image.open(img))
        tk_img = ImageTk.PhotoImage(pil_img)
        self.queued_image = tk_img

    def set_anim(self, img):
        pil_img = Image.open(img)

        seq = []
        try:
            while 1:
                seq.append(pil_img.copy())
                pil_img.seek(len(seq))
        except EOFError:
            pass

        first = self.resize_image(seq[0].convert('RGBA'))
        frames = [ImageTk.PhotoImage(first)]

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = self.resize_image(temp.convert('RGBA'))
            frames.append(ImageTk.PhotoImage(frame))
        
        try:
            delay = pil_img.info['duration']
            if delay == 0:
                delay = 100
        except KeyError:
            delay = 100

        self.queued_image = {'frames': frames, 'delay': delay}

    def play_queued_image(self):
        img = self.queued_image
        self.queued_image = None
        if type(img) == dict:
            self.anim_index = 0
            self.play_anim(img)
        else:
            self.play_static(img)

    def play_anim(self, img):
        self.anim_playing = 1
        self.configure(image = img['frames'][self.anim_index])
        self.anim_index += 1
        if self.anim_index == len(img['frames']):
            self.anim_index = 0
            if self.queued_image != None:
                self.anim_playing = 0
                return self.play_queued_image()
        self.cancel = self.after(img['delay'], self.play_anim, img)

    def play_static(self, img):
        self.configure(image = img)
        self.image = img

class ShuffleWindow:
    def __init__(self, t, img_dir):
        self.imgs = [join(img_dir, f) for f in listdir(img_dir) if isfile(join(img_dir,f)) and '.conf' not in f]
        self.t = t
        self.init_GUI()

    def init_GUI(self):
        self.root = tk.Tk()
        #self.root.attributes('-fullscreen', True)
        self.l = BetterLabel(self.root)
        self.l.pack()
        Timer(1.0, self.image_loop).start()
        self.root.mainloop()
    
    def image_loop(self):
        img_path = choice(self.imgs)
        self.l.display_image(img_path)
        Timer(self.t*60, self.image_loop).start()

if __name__ == '__main__':
    shuffle_window = ShuffleWindow(float(argv[1]), argv[2])
