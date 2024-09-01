import tkinter
from PIL import ImageTk, Image
from tkinter.messagebox import askyesno
from Vertex import Vertex
from AlignPicture import AlignPicture

class CamScanner:
    """_summary_
    This class s responsible to crop pictures
    """
    WINDOW_TITLE = "Cam-Scanner"
    INPUT_PICTURE_FILE = "./assets/Image to hang before cropping.jpg"
    OUTPUT_PICTURE_FILE = "./assets/Picture to hang.jpg"
    INSTRUCTION = "Crop"
    MESSAGE = "Are you sure you want to crop like this?"
    TITLE = "Conformation"

    def __init__(self, file_name,prompt,tosave,points):
        self.exit_app = True
        self.root = tkinter.Tk() #define the window
        self.root.title(CamScanner.WINDOW_TITLE)
        self.prompt = prompt
        self.file = Image.open(file_name) #open the picture
        self.img = ImageTk.PhotoImage(self.file) #create a photo to paste on the canvas
        self.button_finish = tkinter.Button(self.root,text = CamScanner.INSTRUCTION, command = self.finish_handle,
                                            bg = "skyblue", font = 'Caliberi')
        self.button_finish.pack()
        self.label = tkinter.Label(self.root, text=self.prompt, font= "Caliberi", fg= "blue")
        self.label.pack()

        # create a canvas on the frame in size 250*300
        self.canvas = tkinter.Canvas(self.root, width=self.img.width(), height=self.img.height())

        # where to put the image
        self.image_id = self.canvas.create_image(self.img.width() / 2, self.img.height() / 2, image = self.img)
        self.canvas.pack(fill="both", expand=True) #how the canvas represent itself
        self.canvas.bind("<Button 1>",self.click_handle)
        self.vertex_list = []
        self.lines_list = []
        self.canvas.bind("<Configure>", self.resize_handle)
        self.width = self.img.width()
        self.height = self.img.height()
        self.canvas.addtag_all("all") #define all the things on the canvas (like vertex, lines etc.)
        if points != None:
            start = len(points) - 4
            for point in points[start:]:
                self.vertex_list.append(Vertex(point[0],point[1],-1))
            self.draw_vertex()
        self.tosave = tosave


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
        self.file = self.file.resize( (int(self.file.width*wscale),int(self.file.height*hscale)))
        self.img = ImageTk.PhotoImage(self.file)
        self.canvas.scale("all",0,0,wscale,hscale)
        self.canvas.itemconfigure(self.image_id, image=self.img)  # Update the image size (optional)
        for node in self.vertex_list:
            node.x = node.x*wscale
            node.y = node.y*hscale
        self.create_shape_after_resize()

    def create_shape_after_resize(self):
        """create a shape after resize"""
        for node in self.vertex_list:
            self.canvas.delete(node.id)
            node.id = self.canvas.create_oval(node.x,node.y,node.x+10,node.y+10, fill = 'red')
        if len(self.vertex_list) == 4:
            self.draw_square()

    def save_crop_picture(self):
        """
        This function is saving a copy of the cropped picture
        :return:
        """
        nw_point, ne_point, sw_point, se_point = Vertex.sort_corners(self.vertex_list)
        c = AlignPicture(CamScanner.INPUT_PICTURE_FILE, CamScanner.OUTPUT_PICTURE_FILE,
                         [nw_point, ne_point, sw_point, se_point])
        c.align_and_save()

    def click_handle(self,event):
        """
            on mouse click get click coordinates
            if there are less than 4 points draw a point and add to point list
            if there are 4 points find the closest existing point and move it
            if there are 4 points draw lines between them
        """
        x = event.x
        y = event.y
        if len(self.vertex_list) < 4:
            id = self.canvas.create_oval(x,y,x+10,y+10,fill='red')
            self.vertex_list.append(Vertex(x,y,id))
        else:
            close = self.vertex_list[0]
            current = Vertex(x,y,id = None)
            for node in self.vertex_list:
                if current.distance_between_two_nodes(node) <current.distance_between_two_nodes(close):
                    close = node
            self.canvas.delete(close.id)
            close.id = self.canvas.create_oval(x,y,x+10,y+10,fill='red')
            close.x = x
            close.y = y
        if len(self.vertex_list) == 4:
            self.draw_square()

    def draw_vertex(self):
        """
        This is helper function which help to draw the whole square. its painting vertex.
        """
        for vertex in self.vertex_list:
            id = self.canvas.create_oval(vertex.x, vertex.y, vertex.x + 10, vertex.y + 10, fill='red')
            vertex.id = id
        self.draw_square()


    def draw_square(self):
        """
            sort the point list by height 
            so points 0, 1 are the top and points 2, 3 are the bottom
        """
        for line in self.lines_list:
            self.canvas.delete(line)
        self.lines_list.clear()
        nw_point,ne_point,sw_point,se_point = Vertex.sort_corners(self.vertex_list)
        self.draw_single_line(nw_point,ne_point)
        self.draw_single_line(ne_point,se_point)
        self.draw_single_line(se_point,sw_point)
        self.draw_single_line(sw_point,nw_point)
        self.corner_vertex = []
        self.corner_vertex.append(nw_point)
        self.corner_vertex.append(ne_point)
        self.corner_vertex.append(sw_point)
        self.corner_vertex.append(se_point)

    def draw_single_line(self, p1, p2):
        """This function is drawing line between 2 points"""
        id = self.canvas.create_line(p1.x + 5, p1.y + 5, p2.x + 5, p2.y + 5, smooth=True, fill='red')
        self.lines_list.append(id)

    def finish_handle(self):
        """
        This function handle the case the user is finish to define the wall.
        """
        if len(self.vertex_list) <4:
            return
        answer = askyesno(CamScanner.TITLE, CamScanner.MESSAGE)
        if answer == True:
            self.exit_app = False
            if self.tosave == True:
                self.save_crop_picture()
            self.root.destroy()

def run_camscanner(picture,prompt, tosave=False, points=None):
    """
    This function activate this interface
    :param picture: the picture we crop
    :param prompt: insrutcions what to do
    :param tosave: if to save the picture to assets or not
    :param points: the corner of the wall/pictures
    :return: The points of the picture/wall as we defined it
    """
    b = CamScanner(file_name = picture,prompt=prompt, tosave = tosave, points = points)
    b.start()
    corner_points_numpy = []
    for vertex in b.vertex_list:
        corner_points_numpy.append((int(vertex.x),int(vertex.y)))
    if b.exit_app == True:
        quit()
    return corner_points_numpy, b.corner_vertex

if __name__ == "__main__":
    run_camscanner(CamScanner.INPUT_PICTURE_FILE, True, True)
