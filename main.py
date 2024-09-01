import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import cv2

from TakeAPicture import run_take_a_picture
from CamScanner import run_camscanner
from Rotation import run_rotation
from HangAPicture import run_hang_a_picture
from perspective_transform import compute_perspective_transform
from FixPicture import run_fix_picture
from FinalPicture import run_final_picture
from visualization import draw_intersection_points
from ultralytics import YOLOWorld
from LivePicture import run_YOLO

PICTURE_PROMPT = "Take a picture of the image to hang and wait 3 seconds after you take the picture"
PICTURE_FILE_BEFORE_CROPPING = "Image to hang before cropping.jpg"
PICTURE_CROP_PROMPT = "Please Crop the Picture to define the Picture you hang"
PICTURE_TO_HANG_FILE = "./assets/Picture to hang.jpg"
WALL_PROMPT = "Take a picture of the wall and wait 3 seconds after you take the picture"
WALL_FILE = "wall.jpg"
WALL_CROP_PROMPT = "Please Crop the Picture to define the Wall"
WALL_FILE_WITH_CORNERS_MARKED = "./assets/Wall with Borders Points.jpg"
RECTIFIED_IMAGE = "assets/rectified_image.jpg"


def order_points(pts):
    # Ensure pts is a numpy array
    pts = np.array(pts, dtype="float32")

    # Sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # Grab the left-most and right-most points from the sorted x-coordinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # Now, sort the left-most coordinates according to their y-coordinates
    # to grab the top-left and bottom-left points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # Now, sort the right-most coordinates according to their y-coordinates
    # to grab the top-right and bottom-right points, respectively
    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (tr, br) = rightMost

    # Return the coordinates in top-left, top-right, bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")

def save_result(image, result_path):
    cv2.imwrite(result_path, image)

def draw_result_with_intersection_points(image, intersection_points):
    #print("Intersection Points: ", intersection_points)
    draw_intersection_points(image, intersection_points)
    return image

def rectify_image(image, ordered_points):
    rectified_img, M = compute_perspective_transform(image, np.array(ordered_points, dtype=np.float32))
    cv2.imwrite("./assets/rectified_image.jpg", rectified_img)
    #print("Rectified image shape:", rectified_img.shape)
    return rectified_img

def main():

    # take a picture of the photo to hang and save it to assets
    picture_to_hang_file = run_take_a_picture(
        propmpt=PICTURE_PROMPT, file_name_to_save=PICTURE_FILE_BEFORE_CROPPING, color= "green")

    #we assume that the picture we will hang is a rectangle picture
    picture_corner_points_numpy, picture_corner_points_vertex = run_camscanner(picture_to_hang_file,PICTURE_CROP_PROMPT,True)
    ###print("Picture Corner Points (in numpy): ", picture_corner_points_numpy)
    ###print("Picture Corner Points (in vertex): ", picture_corner_points_vertex)
    picture_to_hang_file = PICTURE_TO_HANG_FILE #open the file of picture to hang (after transform before rotation)

    #if the picture is fliped, you can rotate it
    picture_to_hang_file, direction = run_rotation(picture_to_hang_file)

    #take a picture of the wall and save it to assets
    wall_picture_file = run_take_a_picture(propmpt=WALL_PROMPT, file_name_to_save=WALL_FILE, color="red")

    #open the cam-scanner interface to "define the wall"
    wall_corner_points_numpy, wall_corner_points_vertex = run_camscanner(wall_picture_file,WALL_CROP_PROMPT, False)
    ###print("Wall Corner Points (in numpy): ", wall_corner_points_numpy)
    ###print("Wall Corner Points (in vertex): ", wall_corner_points_vertex)

    # Duplicate the wall and save the result to assets
    original_image = cv2.imread(wall_picture_file)
    duplicate_image_path = 'assets/Duplicate Wall.jpg'
    save_result(original_image, duplicate_image_path)

    # Order the Corner Points NUMPY of the wall
    wall_corner_points_numpy_sorted = order_points(wall_corner_points_numpy)

    # Confirm wall borders
    result_image = cv2.imread(duplicate_image_path)
    result_image = draw_result_with_intersection_points(result_image, wall_corner_points_numpy)
    save_result(result_image, WALL_FILE_WITH_CORNERS_MARKED)

    # Rectify the image
    rectify_image(original_image, wall_corner_points_numpy_sorted)

    # hang the picture
    selected_point_index, corners_of_picture, picture_to_hang_file, angle = run_hang_a_picture(RECTIFIED_IMAGE, picture_to_hang_file)
    ###print("selected_point_index: ",selected_point_index)
    ###print("Corners of picture to hang: ", corners_of_picture)

    """
        image path - the original image
        corner points- the side points of the picture we ant to hang (on the processed wall)
        img to hang- the actual image we want to hang
        process_wall_w - the width of the processed wall
        process_wall_h - the height of the processed wall
        intersection points - the points were chosen on Cam-scanner
    """
    resize_image = True
    done_fix = False
    center_image_to_hang = None
    while not done_fix:
        #original_picture, img_corner_points, selected_point_index, img_to_hang, wall_corner_points_numpy
        ###print("PICTURE TO HANG FIX-PICTURE:", picture_to_hang_file) #Picture to hang after slider.png
        selected_point_out, picture_to_hang_file, selected_point_index = (
            run_fix_picture(wall_picture_file, corners_of_picture, selected_point_index,picture_to_hang_file,
                            wall_corner_points_numpy, resize_image, wall_corner_points_vertex))
        ###print("PICTURE TO HANG FINAL-PICTURE:", picture_to_hang_file) #Final picture to hang.png
        done_fix, center_image_to_hang = run_final_picture(wall_picture_file, corners_of_picture, selected_point_index,
                            picture_to_hang_file, wall_corner_points_numpy, selected_point_out)
        resize_image = False

    #After we qfinished the Ilustration, run the live picture
    center_image_to_hang.x = center_image_to_hang.x-5
    center_image_to_hang.y = center_image_to_hang.y-5
    #print("wall_corner_points_vertex", wall_corner_points_vertex)
    print("center_image_to_hang", center_image_to_hang)
    run_YOLO(center_image_to_hang, wall_corner_points_vertex, direction)


if __name__ == "__main__":
    # image_path = './assets/Wall_a.jpg'
    main()



