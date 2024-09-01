import tkinter
from PIL import ImageTk, Image, ImageGrab
from Vertex import Vertex
from Line import Line
from tkinter.messagebox import askyesno
from TransformPicture import TransformPicture


class FixPicture:
    """_summary_
    This class is responsible to display the illustration the the user and enable him to choose other points th hang the picture
    """
    WINDOW_TITLE = "Fix Picture"
    RADIUS = 5
    SMALL_FACTOR = 4
    MEDIUM_FACTOR = 3
    LARGE_FACTOR = 2
    GRID_SEGMENTS = 6
    GRID_LINES = 5
    TEMP_PICTURE_FILE = "./assets/Temp picture to hang.png"
    FINAL_PICTURE_FILE = "./assets/Final picture to hang.png"
    INSTRUCTIONS = "Select a point to locate the picture"
    APPROVAL_TITLE = "Picture approval"
    MESSAGE = "Are you sure to approve the picture?"

    def __init__(self, original_picture, img_corner_points, filename_image_to_hang,
                 wall_corner_points_numpy, selected_point_index, resize_image, wall_corner_points_vertex):
        self.exit_app = True
        self.resize_image = resize_image

        self.root = tkinter.Tk()  # define the window
        self.root.title(FixPicture.WINDOW_TITLE)
        #create the wall
        self.file = Image.open(original_picture)  # open the picture
        self.wall = ImageTk.PhotoImage(self.file)  # create a photo to paste on the canvas

        self.topFrame = tkinter.Frame(self.root)
        self.topFrame.pack(fill="both", side=tkinter.TOP)
        #create label (the first one. its will be changed when the program runs)
        self.label = tkinter.Label(self.root, text=FixPicture.INSTRUCTIONS, font= "Caliberi", fg= "orange") #the label
        self.label.pack()
        #create button (its also changing)
        self.button_approve = tkinter.Button(self.topFrame, text="Approve", command=self.approve_handler,
                                                  bg="skyblue", font='Caliberi')
        self.button_approve.pack()
        #create the picture we want to hang
        self.file_img_to_hang = Image.open(filename_image_to_hang).convert("RGBA")
        #self.filename_image_to_hang = filename_image_to_hang
        self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)
        #create the canvas
        self.canvas = tkinter.Canvas(self.root, width=self.wall.width(),
                                     height=self.wall.height())  # create a canvas on the frame in size 250*300
        self.image_id = self.canvas.create_image(self.wall.width() / 2, self.wall.height() / 2,
                                                 image=self.wall, anchor="center")  # where to put the image
        self.canvas.pack(fill="both", expand=True)  # how the canvas represent itself

        #self.canvas.bind("<Configure>", self.resize_handle)
        self.canvas.bind("<Button 1>", self.click_handle)  # define waht to do if I click on button
        self.width = self.wall.width() #wall width
        self.height = self.wall.height() #wall height
        self.wall_corner_points_numpy = []
        for point in wall_corner_points_numpy:
            p = Vertex(point[0], point[1])
            self.wall_corner_points_numpy.append(p)
        self.canvas.addtag_all("all")  # define all the things on the canvas (like vertex, lines etc.)

        # define the grid
        self.wall_corner_points_vertex = wall_corner_points_vertex
        self.grid_lines = []
        self.point_on_grid = []
        self.draw_grid()
        self.draw_point_on_grid()
        self.selected_point_index = selected_point_index
        self.proportion_picture(img_corner_points, wall_corner_points_numpy)

    def start(self):
        """ start tkinter main event loop """
        self.root.mainloop()
    
    def define_width_and_height(self):
        """
        calculate the width and the height of the wall into the original picture
        :return: wall width, wall height
        """
        p1, p2, p3, p4 = Vertex.sort_corners(self.wall_corner_points_numpy)
        wall_width = p2.x-p1.x
        wall_height = p3.y-p1.y
        return wall_width,wall_height, p1



    def draw_grid(self):
        #define the corner vertex
        """
        left_line = nw_point.distance_between_two_nodes(sw_point)
        a_left = abs(sw_point.y - nw_point.y) / abs(sw_point.x - nw_point.x)
        b_left = nw_point.y - (a_left * nw_point.x)
          (195, 62)            (613, 53)


        (193, 381)            (611, 374)
        :return:
        """
        #Vertex(195, 62), Vertex(613, 53), Vertex(193, 381), Vertex(611, 374)
        nw_point, ne_point, sw_point, se_point = self.wall_corner_points_vertex
        
        factor = 10
        nw_point.x = nw_point.x-factor
        ne_point.x = ne_point.x-factor
        sw_point.x = sw_point.x-factor
        se_point.x = se_point.x-factor
        sw_point.y = sw_point.y - factor
        se_point.y = se_point.y - factor


        #DEFINE THE HORIZONTAL LINES
        left_line = nw_point.distance_between_two_nodes(sw_point)
        # y = ax+b   ==  nw_point.y = a_left*nw_point.x +b
        #                nw_point.y - a_left*nw_point.x = b
        a_left = 0
        if nw_point.x != sw_point.x:
            a_left =  (nw_point.y - sw_point.y)/(nw_point.x - sw_point.x)
        b_left = nw_point.y - (a_left*nw_point.x)
        y_diff_left = left_line / FixPicture.GRID_SEGMENTS
        right_line = ne_point.distance_between_two_nodes(se_point)
        a_right = 0
        if se_point.x != ne_point.x:
            a_right = (se_point.y - ne_point.y) / (se_point.x - ne_point.x)
        b_right = ne_point.y - (a_right * ne_point.x)
        y_diff_right = right_line / FixPicture.GRID_SEGMENTS

        #if a_left < 0: y_diff_left = y_diff_left * -1
        for m in range(1, FixPicture.GRID_SEGMENTS):
            y_left = nw_point.y + m * y_diff_left
            if a_left == 0:
                x_left = nw_point.x
            else:
                x_left = (y_left-b_left)/a_left
            vertex_left = Vertex(x_left, y_left)
            y_right = ne_point.y + m* y_diff_right
            if a_right == 0:
                x_right= ne_point.x
            else:
                x_right = (y_right-b_right)/a_right
            vertex_right = Vertex(x_right, y_right)
            self.draw_single_line(vertex_left, vertex_right, Line.HORIZONTAL)

        #DEFINE THE VERTICAL LINES
        top_line = nw_point.distance_between_two_nodes(ne_point)
        # y = ax+b   ==  nw_point.y = a_top*nw_point.x +b
        #                nw_point.y - a_top*nw_point.x = b
        a_top = 0
        if ne_point.x != nw_point.x:
            a_top = (ne_point.y-nw_point.y)/(ne_point.x-nw_point.x)
        b_top = nw_point.y-(a_top*nw_point.x)
        x_diff_top = top_line / FixPicture.GRID_SEGMENTS
        bottom_line = sw_point.distance_between_two_nodes(se_point)
        a_bottom = 0
        if se_point.x != sw_point.x:
            a_bottom = (se_point.y - sw_point.y) / (se_point.x - sw_point.x)
        b_bottom = sw_point.y - (a_bottom * sw_point.x)

        x_diff_bottom = bottom_line/FixPicture.GRID_SEGMENTS
        for m in range (1,FixPicture.GRID_SEGMENTS):
            x_top = nw_point.x +m * x_diff_top
            y_top = a_top * x_top + b_top
            vertex_top = Vertex(x_top,y_top)
            x_bottom = sw_point.x +m * x_diff_bottom
            y_bottom = a_bottom * x_bottom +b_bottom
            vertex_bottom = Vertex(x_bottom, y_bottom)
            self.draw_single_line(vertex_top, vertex_bottom, Line.VERTICAL)

        #for later use, to transform the picture we save the shipua
        self.a_left = a_left
        #self.b_left = b_left
        self.a_right = a_right
        #self.b_right = b_right
        self.a_top = a_top
        #self.b_top = b_top
        self.a_bottom = a_bottom
        #self.b_bottom = b_bottom

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
                    p = line1.is_meeting_after(line2)
                    if p != None and p not in self.point_on_grid:
                        self.point_on_grid.append(p)
        self.draw_vertex()

    def draw_vertex(self):
        """This is a function which draw points on the canvas."""
        """in this case, this is helper function to mark the intersection points to the user."""
        for vertex in self.point_on_grid:
            id = self.canvas.create_oval(vertex.x, vertex.y, vertex.x + 10, vertex.y + 10, fill='red')
            vertex.id = id

    def proportion_picture(self, corner_points, intersection_points):
        """
            This function is back the processed wall to the original state and do transformation to the
            points accordingly.
                corner points- the side points of the picture we want to hang (on the processed wall)
                process_wall_w - the width of the processed wall
                process_wall_h - the height of the processed wall
                intersection points - the points were chosen on Cam-scanner
        """
        process_wall_w = 800
        process_wall_h = 800
        if self.resize_image:

            #sort by y to get the two top intersection points
            intersection_points.sort(key=lambda a: a[1])
            top_left_point = intersection_points[0]
            top_right_point = intersection_points[1]
            bottom_left_point = intersection_points[2] if intersection_points[2][0] < intersection_points[3][0] \
                else intersection_points[3]
            #decide which is left and which is right
            if top_right_point[0] < top_left_point[0]:
                top_left_point, top_right_point = (top_right_point, top_left_point)

            xratio = process_wall_w/ (self.file.width-((top_left_point[0]+bottom_left_point[0])/2+
                                                       (self.file.width-top_right_point[0])))
            yratio = process_wall_h/ (self.file.height-((top_left_point[1]+top_right_point[1])/2+
                                                        (self.file.height-intersection_points[3][1])))
            hanged_w =self.file_img_to_hang.width
            hanged_h = self.file_img_to_hang.height
            self.file_img_to_hang = self.file_img_to_hang.resize((int(hanged_w/xratio), int(hanged_h/yratio)  ))
        self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)

        if len(self.point_on_grid) == 0:
            return

        close = self.point_on_grid[self.selected_point_index]
        self.hang_image_id = self.canvas.create_image(close.x + FixPicture.RADIUS, close.y + FixPicture.RADIUS,
                                                      image=self.img_to_hang)
        self.select_point = close
        self.file_img_to_hang.save(FixPicture.TEMP_PICTURE_FILE)

        t=True
        if self.resize_image and t:
            screen_width = 640
            screen_height= 480
            self.resize_image = False
            hang_width = self.file_img_to_hang.width
            hang_height = self.file_img_to_hang.height
            pic_nw = Vertex(0,0)
            pic_ne = Vertex(hang_width, 0)
            pic_sw = Vertex(0,hang_height)
            pic_se = Vertex(hang_width, hang_height)
            b_bottom= pic_sw.y - (self.a_bottom * pic_sw.x)
            line1 = Line(pic_sw,Vertex(screen_width,self.a_bottom*screen_width+b_bottom),0,Line.HORIZONTAL)
            b_right = pic_ne.y - (self.a_right * pic_ne.x)
            if self.a_right == 0:
                line2 = Line(pic_ne, pic_se,0, Line.VERTICAL)
            else:
                line2 = Line(pic_ne,Vertex((screen_height-b_right)/self.a_right,screen_height),0,Line.VERTICAL)
            new_se = line1.is_meeting_after(line2)
            b_left = pic_sw.y-(self.a_left*pic_sw.x)
            if self.a_left == 0:
                line3 = Line(pic_sw, pic_nw, 0, Line.VERTICAL)
            else:
                line3 = Line(pic_sw, Vertex((0-b_left)/self.a_left, 0), 0,Line.VERTICAL)
            b_top = pic_ne.y - (self.a_top * pic_ne.x)
            line4 = Line(pic_ne, Vertex(0, self.a_top * 0 + b_top),0, Line.HORIZONTAL)
            new_nw = line3.is_meeting_after(line4)
            destination_points = [new_nw,pic_ne,new_se,pic_sw]

            t = TransformPicture(FixPicture.TEMP_PICTURE_FILE,destination_points,FixPicture.FINAL_PICTURE_FILE)
            t.transformation()
            self.new_nw = new_nw
            self.new_se = new_se
            self.file_img_to_hang = Image.open(FixPicture.FINAL_PICTURE_FILE).convert("RGBA")
            self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)

        self.click_handle(self.select_point)

    def click_handle(self,event):
        """
            A general function which handle on clicking on the canvas (use it when we want to choose
            the point to hang an image)
        """

        x = event.x
        y = event.y
        #define that if I click enough close to a red point on a grid, its will work
        close = self.point_on_grid[0]
        current = Vertex(x, y, id=None)
        index = 0
        for node in self.point_on_grid:
            if current.distance_between_two_nodes(node) < current.distance_between_two_nodes(close):
                close = node
                self.selected_point_index = index
            index += 1
        self.select_point = close

        # hang the image on the selected point
        if self.hang_image_id != -1:
            self.canvas.delete(self.hang_image_id)

        #self.file_img_to_hang = Image.open(FixPicture.FINAL_PICTURE_FILE)
        #self.img_to_hang = ImageTk.PhotoImage(self.file_img_to_hang)

        self.hang_image_id = self.canvas.create_image( close.x + FixPicture.RADIUS, close.y + FixPicture.RADIUS,
                                                       image=self.img_to_hang)  # where to put the image
        self.corner_points = [(x - FixPicture.RADIUS) - self.img_to_hang.width() // 2,
                              (x - FixPicture.RADIUS) + self.img_to_hang.width() // 2,
                              (y - FixPicture.RADIUS) - self.img_to_hang.height() // 2,
                              (y - FixPicture.RADIUS) + self.img_to_hang.height() // 2]
        self.image_to_hang_x = x
        self.image_to_hang_y = y



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
        answer = askyesno(FixPicture.APPROVAL_TITLE, FixPicture.MESSAGE)
        if answer == True:
            self.exit_app = False
            self.root.destroy()


def run_fix_picture(original_picture, img_corner_points, selected_point_index, img_to_hang, wall_corner_points,
                    resize_image, vertex_corner_points):
    """
        This function is actually dispaly the wall with the hanging image
        image path - the original image
        corner points- the side points of the picture we ant to hang (on the processed wall)
        img to hang- the actual image we want to hang
        process_wall_w - the width of the processed wall
        process_wall_h - the height of the processed wall
        intersection points - the points were chosen on Cam-scanner
    """

    img_corner_points_in = []
    for p in img_corner_points:
        img_corner_points_in.append(p)
    vertex_corner_points_in = []
    for v in vertex_corner_points:
        vertex_corner_points_in.append(Vertex(v.x, v.y))
    fix_picture = FixPicture(original_picture, img_corner_points_in, img_to_hang, wall_corner_points, selected_point_index,
                             resize_image, vertex_corner_points_in)
    # final_picture = FinalPicture('./assets/Wall_a.jpg', [222, 400, 49, 165],"./image_to_hang.jpg", 806, 179)
    fix_picture.start()
    if fix_picture.exit_app == True:
        quit()
    return fix_picture.select_point, FixPicture.FINAL_PICTURE_FILE, fix_picture.selected_point_index


#unit test only
if __name__ == "__main__":
    run_fix_picture("./assets/debug_wall.jpg", #image_path
                    [341, 611, 124, 264], #corners_of_picture
                    7, #selected_point_index
                    "./distorted_image.png", #"./assets/Picture to hang after slider.png",
                    [(548, 21), (364, 141), (594, 387), (365, 441)], #wall_corner_points_numpy
                    True, #resize_images
                    [Vertex(364, 141),
                                      Vertex(548, 21),
                                      Vertex(365, 441),
                                      Vertex(594, 387)]) #wall_corner_points_vertex
    """
        image_path ./assets/wall.jpg 
        corners_of_picture [288, 664, 85, 283] 
        selected_point_index 7 
        picture_to_hang ./assets/Picture to hang after slider.jpg 
        wall_corner_points_numpy [(111, 119), (497, 149), (94, 371), (543, 473)] 
        resize_image True 
        wall_corner_points_vertex [(111, 119), (497, 149), (94, 371), (543, 473)]
    """

