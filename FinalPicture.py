import tkinter
from PIL import ImageTk, Image, ImageGrab
from Vertex import Vertex
from tkinter.messagebox import askyesno


class FinalPicture:

    RADIUS = 5
    WINDOW_TITLE = "Final Picture"
    INSTRUCTION = "Approve You're satisfied"
    APPROVAL_TITLE = "Picture approval"
    APPROVAL_MESSAGE = "Are you sure to approve the picture?"
    FINAL_PICTURE_HANGED_ON_WALL_FILE = "./assets/Wall_with_hanging-picture.png"
    DECLINER_TITLE = "Picture decliner"
    DECLINER_MESSAGE = "Are you sure to fix the picture?"

    # FinalPicture(original_picture, img_corner_points, img_to_hang, wall_corner_points)
    def __init__(self, original_picture, img_corner_points, filename_image_to_hang,
                 wall_corner_points, selected_point_index, selected_point):
        self.exit_app = True

        self.root = tkinter.Tk()  # define the window
        self.root.title(FinalPicture.WINDOW_TITLE)
        # create the wall
        self.file = Image.open(original_picture)  # open the picture
        self.wall = ImageTk.PhotoImage(self.file)  # create a photo to paste on the canvas

        self.topFrame = tkinter.Frame(self.root)
        self.topFrame.pack(fill="none", side=tkinter.TOP)
        # create label (the first one. its will be changed when the program runs)
        self.label = tkinter.Label(self.root, text=FinalPicture.INSTRUCTION, font= "Caliberi", fg= "gold")  # the label
        self.label.pack()
        # create button (its also changing)
        self.button_approve = tkinter.Button(self.topFrame, text="Approve", command=self.approve_handler,
                                             bg="skyblue", font='Caliberi')
        self.button_approve.pack(side=tkinter.LEFT, padx=(150,0))
        self.button_decline = tkinter.Button(self.topFrame, text="Decline", command=self.decline_handler,
                                             bg="skyblue", font='Caliberi')
        self.button_decline.pack(side=tkinter.RIGHT, padx=(0,150))

        # create the canvas
        self.canvas = tkinter.Canvas(self.root, width=self.wall.width(),
                                     height=self.wall.height())  # create a canvas on the frame in size 250*300
        self.image_id = self.canvas.create_image(self.wall.width() / 2, self.wall.height() / 2,
                                                 image=self.wall)  # where to put the image
        self.canvas.pack(fill="both", expand=True)  # how the canvas represent itself

        # self.canvas.bind("<Configure>", self.resize_handle)
        #self.canvas.bind("<Button 1>", self.click_handle)  # define waht to do if I click on button
        self.width = self.wall.width()  # wall width
        self.height = self.wall.height()  # wall height
        self.canvas.addtag_all("all")  # define all the things on the canvas (like vertex, lines etc.)
        # self.canvas.bind("<Button 1>",self.canvas_click_handle)
        # resize pic

        self.selected_point_index = selected_point_index
        self.selected_point = selected_point

        # create the picture we want to hang
        self.file_img_to_hang = Image.open(filename_image_to_hang)
        self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)
        self.hang_image_id = self.canvas.create_image(self.selected_point.x + FinalPicture.RADIUS,
                                                      self.selected_point.y + FinalPicture.RADIUS, image=self.img_to_hang)

        # calculate the center of the hanged image
        # self.center_image_to_hang = Vertex(int(selected_point.x + self.img_to_hang.width() / 2),
        #                                    int(selected_point.y + self.img_to_hang.height() / 2))
        self.center_image_to_hang = Vertex(int(selected_point.x),
                                           int(selected_point.y ))


    def start(self):
        """ start tkinter main event loop """
        self.root.mainloop()


    def resize_handle(self, event):
        """
            resizes the image, points and lines on the canvas
        """
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        self.file = self.file.resize((int(self.file.width * wscale), int(self.file.height * hscale)))
        self.wall = ImageTk.PhotoImage(self.file)
        self.canvas.scale("all", 0, 0, wscale, hscale)
        self.canvas.itemconfigure(self.image_id, image=self.wall)  # Update the image size (optional)

    def approve_handler(self):
        """
        This function handle the case the user approves the picture
        """
        answer = askyesno(FinalPicture.APPROVAL_TITLE, FinalPicture.APPROVAL_MESSAGE)
        if answer == True:
            self.save_final_picture()
            self.exit_app = True
            self.root.destroy()

    def save_final_picture(self):
        #todo fix this function
        x=self.canvas.winfo_x()  #x coordinate of the nw point of the canvas
        y=self.canvas.winfo_y()  #y coordinate of the nw point of the canvas
        canvas_width = self.file.width
        canvas_height = self.file.height
        im = ImageGrab.grab(bbox=(x,y,x+canvas_width,y+canvas_height))
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(FinalPicture.FINAL_PICTURE_HANGED_ON_WALL_FILE, format='JPEG', quality=95)
    def decline_handler(self):
        answer = askyesno(FinalPicture.DECLINER_MESSAGE, FinalPicture.DECLINER_MESSAGE)
        if answer == True:
            self.exit_app = False
            self.root.destroy()


def run_final_picture(original_picture, img_corner_points, selected_point_index,
                      img_to_hang, wall_corner_points, selected_point):
    """
        This function is actually dispaly the wall with the hanging image
        image path - the original image
        corner points- the side points of the picture we ant to hang (on the processed wall)
        img to hang- the actual image we want to hang
        process_wall_w - the width of the processed wall
        process_wall_h - the height of the processed wall
        intersection points - the points were chosen on Cam-scanner
    """
    final_picture = FinalPicture(original_picture, img_corner_points, img_to_hang, wall_corner_points,
                               selected_point_index, selected_point)
    # final_picture = FinalPicture('./assets/Wall_a.jpg', [222, 400, 49, 165],"./image_to_hang.jpg", 806, 179)
    final_picture.start()
    return final_picture.exit_app, final_picture.center_image_to_hang

# unit test only
if __name__ == "__main__":
    #(original_picture, img_corner_points, selected_point_index,img_to_hang, wall_corner_points, selected_point)
    run_final_picture('./assets/wall.jpg',
                      [149, 387, 116, 272], 12,
                      "./assets/Final picture to hang.png", [(627, 130), (276, 143), (276, 386), (626, 398)],
                      Vertex(267.66, 195.333))


    #original_picture, img_corner_points, selected_point_index, img_to_hang, wall_corner_points, selected_point