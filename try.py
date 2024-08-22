# import cv2
# import numpy as np

# def sort_points(points):
#     points = sorted(points, key=lambda x: x[1])  # Sort by y-coordinate to separate top and bottom points
#     top_points = sorted(points[:2], key=lambda x: x[0])  # Sort top points by x-coordinate
#     bottom_points = sorted(points[2:], key=lambda x: x[0])  # Sort bottom points by x-coordinate
#     return [top_points[0], top_points[1], bottom_points[1], bottom_points[0]]  # Return sorted points

# def distort_image_to_shape(input_image_path, output_image_path, large_image_points):
#     # Sort the points to match the order: top-left, top-right, bottom-right, bottom-left
#     sorted_points = sort_points(large_image_points)

#     # Load the small image with alpha channel
#     small_image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
#     if small_image is None:
#         raise FileNotFoundError(f"Image at path {input_image_path} not found.")

#     # Ensure the image has an alpha channel
#     if small_image.shape[2] != 4:
#         raise ValueError("Input image does not have an alpha channel (RGBA).")

#     # Get the dimensions of the small image
#     small_height, small_width = small_image.shape[:2]

#     # Define the original points (corners of the small image)
#     original_points = np.float32([[0, 0], [small_width, 0], [small_width, small_height], [0, small_height]])

#     # Define the points in the larger image to which we want to map the small image
#     target_points = np.float32(sorted_points)

#     # Compute the bounding box of the target points
#     min_x = min(p[0] for p in sorted_points)
#     max_x = max(p[0] for p in sorted_points)
#     min_y = min(p[1] for p in sorted_points)
#     max_y = max(p[1] for p in sorted_points)
#     target_width = max_x - min_x
#     target_height = max_y - min_y

#     # Adjust the target points relative to the bounding box
#     adjusted_target_points = np.float32([
#         [p[0] - min_x, p[1] - min_y] for p in sorted_points
#     ])

#     # Ensure output size is large enough to contain the transformed image
#     output_size = (target_width, target_height)

#     # Compute the perspective transformation matrix
#     matrix = cv2.getPerspectiveTransform(original_points, adjusted_target_points)

#     # Split the image into its RGBA channels
#     channels = cv2.split(small_image)
#     transformed_channels = []

#     # Perform the perspective transformation on each channel
#     for channel in channels:
#         transformed_channel = cv2.warpPerspective(channel, matrix, output_size)
#         transformed_channels.append(transformed_channel)

#     # Merge the transformed channels back together
#     output_image = cv2.merge(transformed_channels)

#     # Save the output image with transparency
#     cv2.imwrite(output_image_path, output_image)
#     print(f"Distorted image saved to {output_image_path}")

  #  """
   # function  that the output image aligns with the slopes of the four sides of the quadrilateral defined by the large_image_points
   # """

import cv2
import numpy as np

def sort_points(points):
    centroid = np.mean(points, axis=0)

    def angle_from_centroid(point):
        return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])
    
    points = sorted(points, key=angle_from_centroid)
    return [points[0], points[1], points[2], points[3]]

def distort_image_to_shape(input_image_path, output_image_path, large_image_points):
    sorted_points = sort_points(np.array(large_image_points))

    small_image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
    if small_image is None:
        raise FileNotFoundError(f"Image at path {input_image_path} not found.")
    if small_image.shape[2] != 4:
        raise ValueError("Input image does not have an alpha channel (RGBA).")

    small_height, small_width = small_image.shape[:2]
    original_points = np.float32([[0, 0], [small_width, 0], [small_width, small_height], [0, small_height]])
    target_points = np.float32(sorted_points)

    # Compute the bounding box of the target points
    min_x = min(p[0] for p in target_points)
    max_x = max(p[0] for p in target_points)
    min_y = min(p[1] for p in target_points)
    max_y = max(p[1] for p in target_points)
    target_width = int(max_x - min_x)  # Ensure these are integers
    target_height = int(max_y - min_y)

    # Adjust target points for the transformation
    adjusted_target_points = np.float32([
        [p[0] - min_x, p[1] - min_y] for p in target_points
    ])

    # Compute the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(original_points, adjusted_target_points)

    # Perform the perspective transformation
    output_image = cv2.warpPerspective(small_image, matrix, (target_width, target_height))

    # Save the output image with transparency
    cv2.imwrite(output_image_path, output_image)
    print(f"Distorted image saved to {output_image_path}")

# Example usage
input_image_path = './assets/test_hang_picture.png'  # Path to the small image with RGBA channels
output_image_path = 'distorted_image.png'  # Path to save the distorted image
large_image_points = [(548, 21), (364, 141), (594, 387), (365, 441)]  # Coordinates of the large image points

distort_image_to_shape(input_image_path, output_image_path, large_image_points)

