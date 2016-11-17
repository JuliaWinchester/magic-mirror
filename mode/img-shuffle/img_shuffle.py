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
        self.new_image_waiting = 0
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

    def set_image(self, img):
        if self.anim_playing == 1:
            if self.queued_image == None:
                print("can't play new image yet, putting it in queue")
                self.new_image_waiting = 1
                self.queued_image = img
            return
        else:
            self.new_image_waiting = 0
            self.queued_image = None
            if img.lower()[-3:] == 'gif':
                self.set_anim_image(img)
            else:
                self.set_static_image(img)

    def set_static_image(self, img):
        pil_img = self.resize_image(Image.open(img))
        tk_img = ImageTk.PhotoImage(pil_img)
        self.configure(image = tk_img)
        self.image = tk_img

    def construct_anim_frames(self, pil_img):
        seq = []
        try:
            while 1:
                seq.append(pil_img.copy())
                pil_img.seek(len(seq))
        except EOFError:
            pass

        first = self.resize_image(seq[0].convert('RGBA'))
        self.frames = [ImageTk.PhotoImage(first)]

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = self.resize_image(temp.convert('RGBA'))
            self.frames.append(ImageTk.PhotoImage(frame))
        print('frame construction done')

    def set_anim_image(self, img):
        img = Image.open(img)

        self.construct_anim_frames(img)
        
        try:
            self.delay = img.info['duration']
            if self.delay == 0:
                self.delay = 100
        except KeyError:
            print('defaulting to standard delay amount')
            self.delay = 100

        self.index = 0
        self.cancel = self.after(self.delay, self.anim_play)

    def anim_play(self):
        self.anim_playing = 1
        print(self.index)
        self.configure(image = self.frames[self.index])
        self.index += 1
        if self.index == len(self.frames):
            self.index = 0
            print(self.index)
            if self.new_image_waiting == 1:
                self.anim_playing = 0
                print('gif animation ended, playing new image:')
                print(self.queued_image)
                return self.set_image(self.queued_image)
        self.cancel = self.after(self.delay, self.anim_play)

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
        print('new loop, sending new image of path:')
        img_path = choice(self.imgs)
        print(img_path)
        self.l.set_image(img_path)
        Timer(self.t*60, self.image_loop).start()

if __name__ == '__main__':
    shuffle_window = ShuffleWindow(float(argv[1]), argv[2])
