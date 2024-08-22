# import the Python Image
# processing Library
import tkinter
from PIL import ImageTk, Image
from tkinter.messagebox import askyesno
import cv2
from Line import Line

class Rotation:

    #INPUT_PICTURE_FILE = "./assets/Image to hang before cropping.jpg"
    WINDOW_TITLE = "Rotation"
    OUTPUT_PICTURE_FILE = "./assets/Rotated Image.png"
    INSTRUCTION = "Please rotate the picture as you want"
    APPROVAL_MESSAGE = "Are you sure to approve the picture?"
    APPROVAL_WINDOW = "Picture approval"

    def __init__(self, file_name):
        self.exit_app = True
        self.root = tkinter.Tk() #define the window
        self.root.title(Rotation.WINDOW_TITLE)
        self.file = Image.open(file_name).convert('RGBA') #open the picture
        self.img = ImageTk.PhotoImage(self.file) #create a photo to paste on the canvas

        self.topFrame = tkinter.Frame(self.root)
        self.topFrame.pack(fill="none", side=tkinter.TOP)
        # create label (the first one. its will be changed when the program runs)
        self.label = tkinter.Label(self.root, text=Rotation.INSTRUCTION, font= "Caliberi", fg= "purple", bg='pink')  # the label
        self.label.pack()

        # create buttons
        self.button_approve = tkinter.Button(self.topFrame, text="Approve", command=self.approve_handler,
                                             bg="skyblue", font='Caliberi')
        self.button_approve.pack(side=tkinter.LEFT, padx=(0,0))
        self.button_rotation = tkinter.Button(self.topFrame,text = "Rotate", command = self.rotate_handler,
                                              bg = "skyblue", font = 'Caliberi')
        self.button_rotation.pack(side=tkinter.LEFT, padx=(0,0))

        # create the canvas
        self.canvas = tkinter.Canvas(self.root, width=self.img.width(), height=self.img.height())
        # where to put the image
        self.image_id = self.canvas.create_image(self.img.width() / 2, self.img.height() / 2, image = self.img)
        self.canvas.pack(fill="both", expand=True) #how the canvas represent itself
        #self.canvas.bind("<Configure>", self.resize_handle)
        self.width = self.img.width()
        self.height = self.img.height()
        self.canvas.addtag_all("all") #define all the things on the canvas (like vertex, lines etc.)

        # setup default image direction
        if self.img.width() > self.img.height():
            self.direction = Line.HORIZONTAL
        else:
            self.direction = Line.VERTICAL


    def start(self):
        """ start tkinter main event loop """
        self.root.mainloop()

    def approve_handler(self):
        """
        This function handle the case the user approves the picture
        """
        answer = askyesno(Rotation.APPROVAL_WINDOW, Rotation.APPROVAL_MESSAGE)
        if answer == True:
            self.exit_app = False
            self.file.save(Rotation.OUTPUT_PICTURE_FILE)
            self.root.destroy()

    def rotate_handler(self):
        """
        This is a picture which rotate the picture by 90 degrees evey time we rotated it
        :return: the rotated picture
        """
        self.file = self.file.rotate(90,expand=True,fillcolor=(0,0,0,0))
        self.img = ImageTk.PhotoImage(self.file)
        #self.canvas = tkinter.Canvas(self.root, width=self.img.width(),
                                     #height=self.img.height())  # create a canvas on the frame in size 250*300
        self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(self.img.width() / 2, self.img.height() / 2,
                                                 image=self.img)  # where to put the image
        if self.img.width() > self.img.height():
            self.direction = Line.HORIZONTAL
        else:
            self.direction = Line.VERTICAL
        self.canvas.pack(fill="both", expand=True)  # how the canvas represent itself

def run_rotation(file_name):
    """
    This function activate this interface
    :param picture: the picture we crop
    :param prompt: insrutcions what to do
    :param tosave: if to save the picture to assets or not
    :param points: the corner of the wall/pictures
    :return: The points of the picture/wall as we defined it
    """
    b = Rotation(file_name = file_name)
    b.start()
    if b.exit_app == True:
        quit()
    return b.OUTPUT_PICTURE_FILE, b.direction

if __name__ == "__main__":
    run_rotation("./assets/surf.jpg")