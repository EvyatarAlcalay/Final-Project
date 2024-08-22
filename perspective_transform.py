import cv2
import numpy as np


def rectify_quadrilateral_area(src_img, src_points, output_width=800):
    """
    Extracts and rectifies the quadrilateral area defined by src_points from the source image.

    Parameters:
    - src_img: The source image from which to extract the quadrilateral.
    - src_points: A list of four (x, y) tuples representing the corners of the quadrilateral.
                  The points should be in the order [top-left, top-right, bottom-right, bottom-left].
    - output_width: Desired width of the output rectified image. The height will be calculated based on the quadrilateral's aspect ratio.

    Returns:
    - rectified_img: The rectified image where the quadrilateral has been transformed to a rectangle.
    """

    # Calculate the height of the quadrilateral to maintain aspect ratio
    width_top = np.linalg.norm(src_points[0] - src_points[1])
    width_bottom = np.linalg.norm(src_points[2] - src_points[3])
    height_left = np.linalg.norm(src_points[0] - src_points[3])
    height_right = np.linalg.norm(src_points[1] - src_points[2])

    # Calculate the aspect ratio of the quadrilateral
    quad_width = (width_top + width_bottom) / 2
    quad_height = (height_left + height_right) / 2
    aspect_ratio = quad_height / quad_width

    # Calculate output height to maintain the aspect ratio
    output_height = int(output_width * aspect_ratio)

    # Destination points for the perspective transformation
    dst_points = np.array([[0, 0], [output_width - 1, 0],
                           [output_width - 1, output_height - 1], [0, output_height - 1]], dtype=np.float32)

    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(src_points.astype(np.float32), dst_points)

    # Apply the perspective transformation to rectify the image
    rectified_img = cv2.warpPerspective(src_img, M, (output_width, output_height))
    return rectified_img


def compute_perspective_transform(src_img, src_points, output_width=800):
    # Calculate width/height of the quadrilateral
    width_top = np.sqrt(((src_points[1][0] - src_points[0][0]) ** 2) + ((src_points[1][1] - src_points[0][1]) ** 2))
    width_bottom = np.sqrt(((src_points[2][0] - src_points[3][0]) ** 2) + ((src_points[2][1] - src_points[3][1]) ** 2))
    width_avg = (width_top + width_bottom) / 2

    height_left = np.sqrt(((src_points[3][0] - src_points[0][0]) ** 2) + ((src_points[3][1] - src_points[0][1]) ** 2))
    height_right = np.sqrt(((src_points[2][0] - src_points[1][0]) ** 2) + ((src_points[2][1] - src_points[1][1]) ** 2))
    height_avg = (height_left + height_right) / 2

    # Maintain aspect ratio
    aspect_ratio = width_avg / height_avg
    output_height = int(output_width / aspect_ratio)

    dst_points = np.float32([[0, 0], [output_width, 0], [output_width, output_height], [0, output_height]])
    M = cv2.getPerspectiveTransform(np.float32(src_points), dst_points)
    rectified_img = cv2.warpPerspective(src_img, M, (output_width, output_height))

    return rectified_img, M



def apply_inverse_perspective_transform(processed_img, M, original_img, src_points):
    """
    Apply the inverse perspective transformation to place the processed image back into its original perspective in the original image.
    processed_img: The processed image that needs to be placed back.
    M: The perspective transformation matrix.
    original_img: The original image where the processed image will be placed.
    src_points: The source points in the original image (corners of the quadrilateral).
    Returns the original image with the processed image placed back in perspective.
    """
    # Compute the inverse perspective transform matrix
    Minv = cv2.getPerspectiveTransform(
        np.float32([[0, 0], [processed_img.shape[1], 0], [processed_img.shape[1],
                                                          processed_img.shape[0]],
                                                            [0, processed_img.shape[0]]]), np.float32(src_points))

    # Apply the inverse perspective transform to the processed image
    original_with_processed = cv2.warpPerspective(processed_img, Minv, (original_img.shape[1], original_img.shape[0]))

    # Combine the processed image with the original image using the source points
    mask = np.zeros_like(original_img, dtype=np.uint8)
    cv2.fillConvexPoly(mask, np.int32(src_points), (255, 255, 255))
    result = cv2.bitwise_or(original_img, mask)

    return result

def process_rectified_image(rectified_img):
    """
    Perform desired operations on the rectified image.
    rectified_img: The image to process.
    Returns the processed image.
    """

    # Placeholder function for processing the rectified image
    processed_img = rectified_img.copy()
    return processed_img


