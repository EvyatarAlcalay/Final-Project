import tkinter
from PIL import ImageTk, Image, ImageGrab
from tkinter.messagebox import askyesno
from Vertex import Vertex
import cv2
import numpy as np


class AlignPicture:
    def __init__(self, input_picture_file, output_picture_file, point_list, destination_points_list=None):
        """
        :param input_picture_file: for camscanner: "./assets/image_to_hang.jpg"
        :param output_picture_file: for camscanner: "./assets/Picture to hang.jpg"
        :param point_list: nw,ne,sw,se
        """
        self.input_picture_file = input_picture_file
        self.output_picture_file = output_picture_file
        self.source_points = np.array([[point_list[0].x, point_list[0].y], [point_list[1].x, point_list[1].y],
                                       [point_list[2].x, point_list[2].y], [point_list[3].x, point_list[3].y]])
        self.x_width = point_list[1].distance_between_two_nodes(point_list[0])
        self.y_width = point_list[0].distance_between_two_nodes(point_list[2])
        if destination_points_list == None:
            self.destination_points = np.array([[0, 0], [self.x_width, 0], [0, self.y_width], [self.x_width, self.y_width], ])
        else:
            self.destination_points = np.array([
                                                [destination_points_list[0].x, destination_points_list[0].y],
                                                [destination_points_list[1].x, destination_points_list[1].y],
                                                [destination_points_list[2].x, destination_points_list[2].y],
                                                [destination_points_list[3].x, destination_points_list[3].y],])

    def align_and_save(self):
        source_image = cv2.imread(self.input_picture_file)
        t_source_image = source_image.copy()
        h = self.get_homography_matrix(self.source_points, self.destination_points)
        destination_image = cv2.warpPerspective(t_source_image, h, (int(self.x_width), int(self.y_width)))
        cv2.imwrite(self.output_picture_file, destination_image)

    def get_homography_matrix(self, src, dst):
        A = []
        b = []
        for i in range(len(src)):
            s_x, s_y = src[i]
            d_x, d_y = dst[i]
            A.append([s_x, s_y, 1, 0, 0, 0, (-d_x) * (s_x), (-d_x) * (s_y)])
            A.append([0, 0, 0, s_x, s_y, 1, (-d_y) * (s_x), (-d_y) * (s_y)])
            b += [d_x, d_y]
        A = np.array(A)
        h = np.linalg.lstsq(A, b, rcond=None)[0]
        h = np.concatenate((h, [1]), axis=-1)
        return np.reshape(h, (3, 3))

