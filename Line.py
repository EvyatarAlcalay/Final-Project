from Vertex import Vertex
import math

class Line:
    """_summary_
    This class is responsible to create lines (we use them on the grid and on the crop operation)
    """
    HORIZONTAL = 1
    VERTICAL = 2
    UNKNOWN = -1

    def __init__(self, start, end, id, direction):
        """
        Line Constructor
        :param start: Vertex (start point)
        :param end: Vertex (end point)
        :param id: TKinter ID
        :param direction: Line.Horizontal, Line.Vertical
        """
        self.start = start
        self.end = end
        self.id = id
        self.direction = direction #horizontal or vertical

    def __repr__(self):
        return f"{self.start} - {self.end}"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end or\
        self.start == other.end and self.end == other.start

    def is_meeting(self, other):
        """This function is checking if this line is meeting with other line and return the meeting point"""
        # find the meeting point
        if self.direction != other.direction:
            if self.direction == Line.HORIZONTAL:
                return Vertex(other.start.x, self.start.y)
            else:
                return Vertex(self.start.x, other.start.y)
        else:
            return None

    def start_tupple(self, type=""):
        if type == "int":
            return (int(self.start.x), int(self.start.y))
        return self.start.get_tupple()
    
    def end_tupple(self, type=""):
        if type == "int":
            return (int(self.end.x), int(self.end.y))
        return self.end.get_tupple()
    
    def is_meeting_after(self, other):
        """This function is checking if this line is meeting with other line and return the meeting point"""
        # find the meeting point
        if self.direction != other.direction:
            a_self = 0
            if self.end.x!=self.start.x:
                a_self = (self.end.y-self.start.y)/(self.end.x-self.start.x)
            b_self = self.start.y-a_self*self.start.x
            a_other = 0
            if other.end.x != other.start.x:
                a_other = (other.end.y - other.start.y) / (other.end.x - other.start.x)
            b_other = other.start.y - a_other * other.start.x
            b = b_self-b_other
            x = 0
            if a_other!=a_self:
                x = b/(a_other-a_self)
            y = a_self*x + b_self
            return Vertex(x, y)

        else:
            return 
        
    def calculate_line_length(self):
        if self.start.x == self.end.x and self.start.y == self.end.y:
            return 0
        elif self.start.x == self.end.x:
            return abs(self.end.y-self.start.y)
        elif self.start.y == self.end.y:
            return abs(self.end.x-self.start.x)
        else:
            return math.sqrt((self.end.x-self.start.x)**2+(self.end.y-self.start.y)**2)
        

    @staticmethod 
    def calculate_angle(line1,line2):
        """_summary_
        Args:
            line1 (Line): the VERTICAL Line
            line2 (Line): the HORIZONTAL Line
        Returns:
            angle: arctan(line1/line2)
        """
        len1 = line1.calculate_line_length()
        len2 = line2.calculate_line_length()
        return math.degrees(math.atan2(len1,len2))


#l1 = Line(Vertex(0,0),Vertex(3,0),-1,Line.HORIZONTAL)
#print("length l1: ", l1.calculate_line_length())
#l2= Line(Vertex(0,0),Vertex(0,4),-1,Line.VERTICAL)
#print("length l2: ", l2.calculate_line_length())
#l3 = Line(Vertex(3,0),Vertex(0,4),-1,Line.VERTICAL)
#print("length l3: ", l3.calculate_line_length())
#angle = Line.calculate_angle(l2,l1)
#print("Angle: ", angle)