import tkinter
from PIL import ImageTk, Image
from Vertex import Vertex
from Line import Line
from tkinter.messagebox import askyesno

class HangAPicture:
    """
        In this class we choose the position we want to hang the picture
    """
    WINDOW_TITLE = "Hang A Picture"
    RADIUS = 5
    DECREASE_FACTOR = 0.75
    SMALL_FACTOR = 4
    MEDIUM_FACTOR = 3
    LARGE_FACTOR = 2
    GRID_SEGMENTS = 6
    GRID_LINES = 5
    IMAGE_TO_HANG_AFTER_SLIDER = "./assets/Picture to hang after slider.png"
    INSTRUCTION = ("Select a point to hang the picture (by clicking on the screen) and "
                   "Adapt the size of the picture with the slider")
    TITLE= "Conformation"
    MESSAGE = "Are you sure you want to hang here?"


    def __init__(self, file_name, file_name_picture):
        self.exit_app = True
        #create a window
        self.root = tkinter.Tk() #define the window
        self.root.title(HangAPicture.WINDOW_TITLE)

        #create the wall and take mesurment
        self.file = Image.open(file_name) #open the picture
        self.wall = ImageTk.PhotoImage(self.file) #create a photo to paste on the canvas
        self.width = self.wall.width()  # the wall width
        self.height = self.wall.height()  # the wall heigth

        self.topFrame = tkinter.Frame(self.root)
        self.topFrame.pack(fill="both", side=tkinter.TOP)


        #define the picture I want to hang
        self.image_size = -1  #this is define the size of the image (L/M/S)
        self.file_img_to_hang = Image.open(file_name_picture)  # open the picture
        # define the initial size of the hanged picture
        self.file_img_to_hang = self.file_img_to_hang.resize(
            (int(self.file_img_to_hang.width * HangAPicture.DECREASE_FACTOR),
             int(self.file_img_to_hang.height * HangAPicture.DECREASE_FACTOR)))
        self.original_file_img_to_hang = self.file_img_to_hang
        self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang) #create the picture
        self.image_to_hang_ratio = (self.img_to_hang.width(), self.img_to_hang.height())
        self.image_to_hang_x = None
        self.img_to_hang_id = -1

        # slider code
        self.slider = tkinter.Scale(self.root,from_=1, to=10, orient= tkinter.HORIZONTAL, command=self.size_handler,
                                    bg='skyblue')
        self.slider.pack()
        self.slider.set(5)
        self.label = tkinter.Label(self.root, text=HangAPicture.INSTRUCTION, fg="skyblue", font='Caliberi') #the label
        self.label.pack()


        self.isapprovedtohang = False #a boolean represent if its legal to click on the canvas
        self.ishang = False #a boolean represent if i already hanged the image or not

        #create the canvas
        self.canvas = tkinter.Canvas(self.root, width=self.wall.width(),
                                     height=self.wall.height()) #create a canvas on the frame in size 250*300
        self.wall_image_id = self.canvas.create_image(self.wall.width() / 2,
                                                      self.wall.height() / 2,
                                                      image=self.wall) #where to put the image
        self.canvas.pack(fill="both", expand=True) #how the canvas represent itself
        self.canvas.bind("<Button 1>",self.click_handle) #define waht to do if I click on button
        self.canvas.bind("<Configure>", self.resize_handle) #define what to do if I want to resize the window
        self.canvas.addtag_all("all") #define all the things on the canvas (like vertex, lines etc.)

        #define the grid
        self.grid_lines = []
        self.point_on_grid = []  # a list here we save all the intersection points
        self.choose_point_to_hang_the_picture()

    def size_handler(self, s):
        """
        if the slider is less than 5 reduce its size
        if the slider is greater than 5 enlarge its size
        :param s:
        :return:
        """
        pos = self.slider.get() #current slider position
        self.file_img_to_hang = self.original_file_img_to_hang.resize(
            (int(self.image_to_hang_ratio[0] * pos/5),
             int(self.image_to_hang_ratio[1] * pos/5)))  # define the initial size of the hanged picture
        self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)  # create the picture
        if self.img_to_hang_id != -1:
            self.canvas.delete(self.img_to_hang_id)
            self.img_to_hang_id = self.canvas.create_image(self.select_point.x + HangAPicture.RADIUS,
                                                           self.select_point.y + HangAPicture.RADIUS,
                                                           image=self.img_to_hang)  # where to put the image

    def start(self):
        """ start tkinter main event loop """
        self.root.mainloop()


    def choose_point_to_hang_the_picture(self):
        """This is the adaptor function between the previous one to the user selected area"""
        """If the use didn't select area, the applictaion will require to select an area"""
        """If the size of the picture we want to hang is bigger than the area size, the user wiil choose a new size"""
        """after the user choose area, the function return a grid on the selected area"""
        """finally,  the program will transfer to select point on grid"""
        #now the user selected a legal area

        self.draw_grid() #after the picture selected a legal area, we draw a grid on the area
        self.draw_point_on_grid() #after we draw the grid, we draw the points in the intersections
        self.select_point_to_hang() #after that, the user will choose on of point from the intersection
        # draw grid lines

    def draw_grid(self):
        """This function is defining and drawing a grid (a net, without the intersection points) on the selected area"""
        """here we just define the grid (from where to where drawing lines). we draw every line in helper function"""
        self.isapprovedtohang = True
        area_width = self.wall.width()
        #area_height = self.border_lines[self.selected_slice][1][1] - self.border_lines[self.selected_slice - 1][0][1]
        y_diff = (self.wall.height() / HangAPicture.GRID_SEGMENTS)
        x_diff = area_width / HangAPicture.GRID_SEGMENTS
        #draw horizontal lines
        x = 0
        y = y_diff
        for i in range(HangAPicture.GRID_LINES):
            left_vertex = Vertex(x, y, -1)
            right_vertex = Vertex(x+area_width, y, -1)
            self.draw_single_line(left_vertex, right_vertex, Line.HORIZONTAL)
            y += y_diff
        #draw vertical lines
        y = 0
        x = x_diff
        for i in range(HangAPicture.GRID_LINES):
            up_vertex = Vertex(x,y,-1)
            down_vertex = Vertex(x,y+ self.wall.height(), -1)
            self.draw_single_line(up_vertex,down_vertex, Line.VERTICAL)
            x += x_diff



    def draw_single_line(self, p1, p2,direct):
        """This function is drawing line between 2 points"""
        """Here is a helper function to draw the grid"""
        id = self.canvas.create_line(p1.x + 5, p1.y + 5, p2.x + 5, p2.y + 5, smooth=True, fill='green')
        self.grid_lines.append(Line(p1, p2, id, direction=direct))

    def draw_point_on_grid(self):
        """This function is defining the intersection points on the grid and drawing them with helper function"""
        self.point_on_grid = []  # a list here we save all the intersection points
        for line1 in self.grid_lines:
            for line2 in self.grid_lines:
                if line1 != line2:
                    p = line1.is_meeting(line2)
                    if p != None and p not in self.point_on_grid:
                        self.point_on_grid.append(p)
        self.draw_vertex()

    def draw_vertex(self):
        """This is a function which draw points on the canvas."""
        """in this case, this is helper function to mark the intersection points to the user."""
        for vertex in self.point_on_grid:
            id = self.canvas.create_oval(vertex.x, vertex.y, vertex.x + 10, vertex.y + 10, fill='red')
            vertex.id = id


    def select_point_to_hang(self):
        """This function is activated after the grid (with the intersection points) was drawn"""
        """in this function the user choose one point (from the intersction points drawn in red"""
        """by clicking on the point"""
        self.ishang = True
        self.button_hang = tkinter.Button(self.topFrame, text="Hang the picture!", command=self.confirm_hang_a_picture,
                                          bg="skyblue", font='Caliberi')
        self.button_hang.pack()


    def confirm_hang_a_picture(self):
        """This function is confirm that the user want to hang the specific image in the specific point"""
        """We verify with the use if this is the point he want"""
        """If yes, the window is closeing and later we display a new window with the image on the wall"""
        answer = askyesno(HangAPicture.TITLE, HangAPicture.MESSAGE)
        if answer == True:
            self.file_img_to_hang.save(HangAPicture.IMAGE_TO_HANG_AFTER_SLIDER)
            self.exit_app = False
            self.root.destroy()

    def click_handle(self,event):
        """
            A general function which handle on clicking on the canvas (use it when we want to choose
            the point to hang an image)
        """
        if self.isapprovedtohang == False:
           return
        x = event.x
        y = event.y
        #define that if I click enough close to a red point on a grid, its will work
        close = self.point_on_grid[0]
        current = Vertex(x, y, id=None)
        for node in self.point_on_grid:
            if current.distance_between_two_nodes(node) < current.distance_between_two_nodes(close):
                close = node
        self.select_point = close
        # hang the image on the selected point
        if self.img_to_hang_id != -1:
            self.canvas.delete(self.img_to_hang_id)
        self.img_to_hang_id = self.canvas.create_image(close.x + HangAPicture.RADIUS, close.y + HangAPicture.RADIUS,
                                                       image=self.img_to_hang)  # where to put the image
        self.corner_points = [(x - HangAPicture.RADIUS) - self.img_to_hang.width() // 2,
                              (x - HangAPicture.RADIUS) + self.img_to_hang.width() // 2,
                              (y - HangAPicture.RADIUS) - self.img_to_hang.height() // 2,
                              (y - HangAPicture.RADIUS) + self.img_to_hang.height() // 2]
        self.image_to_hang_x = x
        self.image_to_hang_y = y

    def resize_handle(self, event):
        """
            a general function which resizes the image, points and lines on the canvas
        """
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        self.file = self.file.resize( (int(self.file.width*wscale),int(self.file.height*hscale)))
        self.wall = ImageTk.PhotoImage(self.file)
        self.canvas.scale("all", 0, 0, wscale, hscale)
        self.canvas.itemconfigure(self.wall_image_id, image=self.wall)  # Update the image size (optional)
        if self.point_on_grid != None:
            for point in self.point_on_grid:
                point.x = point.x*wscale
                point.y = point.y*hscale
        if self.file_img_to_hang != None and self.ishang == True:
            self.file_img_to_hang = self.file_img_to_hang.resize((int(self.file_img_to_hang.width*wscale),
                                                                  int(self.file_img_to_hang.height*hscale)))
            self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)
            if self.image_to_hang_x != None:
                self.click_handle(Vertex(self.image_to_hang_x*wscale,self.image_to_hang_y*hscale))

    def return_angle(self):
        center_point = Vertex(self.img_to_hang.width()/2,self.img_to_hang.height()/2)
        l1 = Line(Vertex(0,0), Vertex(0,self.img_to_hang.height()/2), None ,Line.VERTICAL)
        l2 = Line(Vertex(0,self.img_to_hang.height()/2), center_point, None ,Line.HORIZONTAL)
        angle = Line.calculate_angle(l1,l2)
        return angle


def run_hang_a_picture(picture, file):
    """Here we activate the operation of hanging a picture (on the processed wall)"""

    b = HangAPicture(picture, file)
    b.start()
    #corner points = point of the picture we hang
    #img_to_hang = this is the image we hang on the wall
    #wall = the procceced wall
    if b.exit_app == True:
        quit()
    selected_point_index = -1;
    for i in range(len(b.point_on_grid)):
        if b.point_on_grid[i] == b.select_point :
            selected_point_index = i
    return selected_point_index, b.corner_points, HangAPicture.IMAGE_TO_HANG_AFTER_SLIDER,b.return_angle()

if __name__ == "__main__":
    run_hang_a_picture("./assets/rectified_image.jpg", "./assets/image_to_hang.jpg")