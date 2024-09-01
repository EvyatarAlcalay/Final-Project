import cv2
import numpy as np


def draw_lines(image, lines):
    # Define a list of colors in BGR format
    colors = [
        (0, 0, 255),  # Red
        (0, 255, 0),  # Green
        (255, 0, 0),  # Blue
        (0, 255, 255),  # Yellow

    ]

    # Iterate through the lines, drawing each one in a different color
    for i, line in enumerate(lines):
        if line is not None:  # Ensure the line exists
            color = colors[i % len(colors)]  # Cycle through colors
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), color, 3)



def draw_representative_lines(image, representative_lines):
    """
    Draw representative lines on the image.
    representative_lines: List of lines represented as ((x1, y1), (x2, y2)).
    """
    for line in representative_lines:
        (x1, y1), (x2, y2) = line
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 3)


def find_intersection_points(lines):
    intersection_points = []

    # Print lines for testing
    print("Input lines:", lines)

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            # Correctly unpack line coordinates based on your input format
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]

            # Calculate the denominator
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom == 0:
                continue  # Lines are parallel; no intersection

            # Calculate the intersection point
            px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)) / denom
            py = ((x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)) / denom

            # Check if the intersection is within the line segments
            if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and \
               min(x3, x4) <= px <= max(x3, x4) and min(y3, y4) <= py <= max(y3, y4):
                intersection_points.append((int(px), int(py)))

    # Print intersection points for testing
    print("Intersection points:", intersection_points)

    return intersection_points


def draw_intersection_points(image, points):
    """
    Draws circles at intersection points on the given image.
    """
    for point in points:
        cv2.circle(image, point, radius=5, color=(0, 255, 0), thickness=-1)  # Green circles

