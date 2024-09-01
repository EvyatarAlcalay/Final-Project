import math
class Vertex:
    """_summary_
    This class represent position on the screen.
    """
    def __init__(self,x,y,id=-1):
        self.x = x
        self.y = y
        self.id = id

    def distance_between_two_nodes(self,other):
        """calculate the distance between two nodes"""
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def __eq__(self, other):
        """ define equal nodes """
        if other == None:
            return False
        return self.x == other.x and self.y==other.y

    def __lt__(self, other):
        """
            check which node little
            sort only by height so we get:
            two first vertex are the top, two others are the bottom
        """
        return self.y < other.y


    def __repr__(self):
        """to print object"""
        return f"({self.x}, {self.y})"

    def get_tupple(self):
        return (self.x, self.y,)

    @staticmethod
    def sort_corners(vertex_list):
        """
        a list of vertex of every picture
        :return: sorted list to nw,ne,sw,se
        """
        vertex_list.sort()
        p1 = vertex_list[0]
        p2 = vertex_list[1]
        p3 = vertex_list[2]
        p4 = vertex_list[3]
        if p2.x < p1.x:
            t = p1
            p1 = p2
            p2 = t
        if p4.x < p3.x:
            t = p3
            p3 = p4
            p4 = t
        return p1,p2,p3,p4