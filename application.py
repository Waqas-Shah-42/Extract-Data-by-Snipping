import tkinter as tk
from tkinter import Label
from PIL import ImageGrab
import cv2
import pytesseract
import numpy
import pyperclip
import datetime
import os

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


MOUSE_COORDINATES = (None, None)


class Application(tk.Frame):
    end_coordinates = (0, 0)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Waqas Snipping Tool")
        self.pack()
        self.text_field = [4]
        self.create_widgets()
        self.image_processing = ImageProcessing()

    def create_widgets(self):

        # creating buttons
        self.snip_button = tk.Button(self, text='Snip button\n Select text to copy', height=2, width=30)
        self.snip_button["command"] = self.snip_screen
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)

        self.l1 = tk.Label(text="This is Beta version of the software and some additional \nfuctionality  has to be  added to the software.", fg="black", bg="white")
        self.l2 = tk.Label(text="Please tally the result of the software as its not 100% accurate", fg="red", bg="white")

        self.l2.pack(side="top")
        self.l1.pack()

        # packing the buttons
        self.snip_button.pack(side="top", padx=10, pady=10)
        self.quit.pack(side="bottom", padx=10, pady=10)

            # creating text fields / future feature
        # for i in range(1, 5):
        #     self.text_field.append(tk.Text(self, height=1, width=20))
        #     self.text_field[i].insert(tk.END,str(i))
        #     self.text_field[i].pack(side='top', padx=10, pady=10)
        #     print(len(self.text_field))

    def snip_screen(self):    # This fuction snips the area from the image
        print("Beginning Snipping")

        # instantiates snipping window
        self.root2 = tk.Tk()
        self.root2.attributes('-alpha', 0.1)
        self.root2.attributes("-fullscreen", True)
        self.root2.title("Don't close this window")

        lbl1 = Label(self.root2, bg='SlateGray3', width=15, height=20, cursor='tcross')
        lbl1.pack(fill='both', expand='yes', padx=0)

        # creating bindings
        self.root2.bind("<ButtonPress-1>", self.mouse_press)
        self.root2.bind("<ButtonRelease-1>", self.mouse_release)
        self.root2.bind("<B1-Motion>", self.mouse_move)

    def mouse_press(self, event):
        self.image_processing.set_startcoordinate((event.x, event.y))

    def mouse_move(self, event):
        # print('mouse move \n',event.x, event.y)
        # will be  used in the future to create snipping box
        pass

    def mouse_release(self, event):
        print('\nmouse end ', event.x, event.y, '\n\n')

        self.root2.destroy()
        img = self.image_processing.screenshot((event.x, event.y))
        self.image_processing.image_processing(img)

    def take_image(self, start_coordinate):
        print('take image')


class ImageProcessing():

    def __init__(self):
        super().__init__()
        self.start_coordinate = (0, 0)

    def set_startcoordinate(self, startcoordinate):
        self.start_coordinate = startcoordinate

    def screenshot(self, end_coordinate):
        screenshot_coordinates = (min(self.start_coordinate[0], end_coordinate[0]),
            min(self.start_coordinate[1], end_coordinate[1]),
            max(self.start_coordinate[0], end_coordinate[0]),
            max(self.start_coordinate[1], end_coordinate[1]))

        img = ImageGrab.grab(bbox=screenshot_coordinates)
        print(datetime.datetime.now())
        print(type(datetime.datetime.now()))
        nm_img = "Images\img "+str(datetime.datetime.now())
        nm_img = nm_img.replace(':', ' ')
        nm_img = nm_img.replace('.', '')
        nm_img = nm_img+'.png'
        print(nm_img)
        img.save(nm_img)
        return img

    def image_processing(self, img):
        print("image processing")
        img = numpy.array(img)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        dimension_images = img.shape
        image_height = dimension_images[0]
        image_width = dimension_images[1]

        image_ratio = 50/image_height
        img_temp = cv2.resize(img, (int(image_width*image_ratio), int(image_height*image_ratio)), interpolation=cv2.INTER_CUBIC)

        imgstr1 = str(pytesseract.image_to_string(img_temp))
        pyperclip.copy(imgstr1)
        # spam = pyperclip.paste()


root = tk.Tk()
try:
    root.wm_attributes("-topmost", 1)
except:
    pass
app = Application(master=root)
app.mainloop()
