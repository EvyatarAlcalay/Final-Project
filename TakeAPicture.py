import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    WINDOW_TITLE = "Take a Picture"
    SECOND = 1000 #second = 1000ms
    TIMER_INITIAL = 3
    DELAY = TIMER_INITIAL * SECOND
    DEVICE_INTERNAL = 0
    DEVICE_EXTERNAL = 1

    def __init__(self, window, window_title,prompt, file_name_to_save, color, video_source=0):
        """
        initialize the camera
        :param window: The window of the Camera
        :param window_title: The window title
        :param prompt: The text which instruct which picture to take
        :param file_name_to_save: the file which in we save the token picture
        :param color: the color of the prompt
        :param video_source:
        """
        self.exit_app = True
        self.window = window
        self.window.title(window_title)
        self.prompt = prompt
        self.color = color
        self.file_name_to_save = file_name_to_save
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        self.width = self.vid.width
        self.height = self.vid.height
        # Button that lets the user take a snapshot
        self.button_shoot=tkinter.Button(window, text="Shoot!", command=self.shoot_handle, bg="skyblue",
                                         font='Caliberi')
        self.button_shoot.pack(anchor=tkinter.CENTER, expand=True)
        # Create a canvas that can fit the above video source size
        self.timer_label = tkinter.Label(self.window, text=self.prompt, font= "Caliberi", fg= self.color)
        self.timer_label.pack()
        self.timer = self.TIMER_INITIAL
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        self.canvas.bind("<Configure>", self.resize_handle)
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.wscale = 1
        self.hscale = 1
        self.delay = 15
        self.update()
        self.window.mainloop()

    def shoot_handle(self):

        self.timer_label.config(text=str(self.timer), font= ("Caliberi", 30), fg= self.color)

        if (self.timer > 0):
            self.window.after(1000, self.shoot_handle)
            self.timer = self.timer - 1
            self.window.update()
        else:
            self.window.after_cancel(self.after_task)
            self.snapshot()

    def snapshot(self):
        self.should_exit = False
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        # self.should_exit = False
        if ret:
            cv2.imwrite("./assets/"+self.file_name_to_save, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            self.taken_picture = "./assets/"+self.file_name_to_save
            self.exit_app = False
            try:
                self.window.destroy()
            except:
                pass

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.raw_image = PIL.Image.fromarray(frame);
            #print("in update", self.wscale)
            self.raw_image = self.raw_image.resize((int(self.raw_image.width * self.wscale),
                                                    int(self.raw_image.height * self.hscale)))
            self.photo = PIL.ImageTk.PhotoImage(image = self.raw_image)
            self.image_id =self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.after_task = self.window.after(self.delay, self.update)

    def resize_handle(self, event):
        """
            resizes the image, points and lines on the canvas
        """
        self.wscale = float(event.width) / self.width
        self.hscale = float(event.height) / self.height
        #self.width = event.width
        #self.height = event.height
        # self.img = ImageTk.PhotoImage(self.file)
        self.canvas.scale("all", 0, 0, self.wscale, self.hscale)
        self.canvas.itemconfigure(self.image_id, image=self.photo)  # Update the image size (optional)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)
     # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def run_take_a_picture(propmpt, file_name_to_save, color):
    b = App(tkinter.Tk(), App.WINDOW_TITLE, propmpt, file_name_to_save,color, App.DEVICE_EXTERNAL)
    if b.exit_app == True:
        quit()
    return b.taken_picture

if __name__ == "__main__":
    run_take_a_picture("prompt you ", "wall.jpg", "green")
    # Create a window and pass it to the Application object
