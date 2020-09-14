import tkinter as tk
from tkinter import Tk, Frame, Label
from PIL import ImageGrab
from PIL import Image
import cv2
import pytesseract
import numpy
import pyperclip

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


MOUSE_COORDINATES = (None, None)
class Application(tk.Frame):
    end_coordinates=(0, 0)
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Waqas Snipping Tool")
        self.pack()
        self.create_widgets()
        self.image_processing=ImageProcessing()
        #self.master.geometry("400x100")


    def create_widgets(self):

        # creating buttons
        self.snip_button = tk.Button(self, text='Snip button\n Select numbers to copy', height=2, width=30)
        self.snip_button["command"] = self.snip_screen   #self.snipping
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)

            # creating text fields
        #T = tk.Text(root, height=2, width=30)
        # self.text_field= tk.Text(self, height=2, width=30)
        # self.text_field.insert(tk.END,"Yolo")
        # self.text_field.pack(padx=10, pady=10)
        self.l1 = tk.Label(text="This is Beta version of the software and some additional \nfuctionality  has to be  addted to the software.", fg="black", bg="white")
        self.l2=tk.Label(text="Please tally the result of the software as its not 100% accurate",fg="red", bg="white")

        self.l2.pack(side="top")
        self.l1.pack()



        # packing the buttons
        self.snip_button.pack(side="top",padx=10, pady=10)  
        self.quit.pack(side="bottom",padx=10, pady=10)

    
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


    def mouse_move(self,event):
        #print('mouse move \n',event.x, event.y)
        #will be  used in the future to create snipping box
        a=2

    def mouse_release(self, event):
        print('\nmouse end ',event.x, event.y,'\n\n')

        self.root2.destroy()
        img=self.image_processing.screenshot((event.x, event.y))
        self.image_processing.image_processing(img)      

    def take_image(self,start_coordinate):
        print ('take image')



class ImageProcessing():
    
    def __init__(self):
        super().__init__()
        self.start_coordinate=(0, 0)

    def set_startcoordinate(self, startcoordinate):
        self.start_coordinate=startcoordinate

    def screenshot(self,end_coordinate):
        screenshot_coordinates=(min(self.start_coordinate[0],end_coordinate[0]),
            min(self.start_coordinate[1],end_coordinate[1]),
            max(self.start_coordinate[0],end_coordinate[0]), 
            max(self.start_coordinate[1],end_coordinate[1]))
        
        img = ImageGrab.grab(bbox=screenshot_coordinates)
        return img

    def image_processing(self, img):
        print("image processing")
        img = numpy.array(img)

        cv2.imshow('Original', img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        cv2.imshow('Gray', img)
        #cv2.imwrite('sample.png', gray)

        dimension_images=img.shape
        image_height = dimension_images[0]
        image_width = dimension_images[1]

        image_ratio = 50/image_height
        img = cv2.resize(img, (int(image_width*image_ratio),int(image_height*image_ratio)), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('Resized', img)
        imgstr = str(pytesseract.image_to_string(img))
        print(imgstr)
        pyperclip.copy(imgstr)
        spam = pyperclip.paste()


root = tk.Tk()
try:
    root.wm_attributes("-topmost", 1)
except:
    pass
app = Application(master=root)
app.mainloop()