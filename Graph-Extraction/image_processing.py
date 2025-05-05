import cv2
import numpy as np
from utils import hex_to_bgr

def preprocess_image(image, target_HEX_color, grid_corners):
    """
    Preprocess the image to generate a binary mask for the target color and mask out areas outside the selected rectangle.
    
    Args:
        image: Input image as a NumPy array.
        target_HEX_color: Hex color string representing the target color to detect (e.g., "#FF0000" for red).
        grid_corners: List of two tuples [(x1, y1), (x2, y2)] defining the rectangle.

    Returns:
        binary: Binary image where the target color is highlighted and areas outside the rectangle are blacked out.
    """
    COLOR_THRESHOLD = 20  # Allowable color variation
    target_color = hex_to_bgr(target_HEX_color)  # Convert hex color to BGR format

    # Create a mask for the target color
    lower_bound = np.array(target_color) - COLOR_THRESHOLD
    upper_bound = np.array(target_color) + COLOR_THRESHOLD
    binary = cv2.inRange(image, lower_bound, upper_bound)

    # Ensure grid_corners are sorted correctly
    (x1, y1), (x2, y2) = grid_corners
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    # Create a mask for the rectangle
    rectangle_mask = np.zeros_like(binary, dtype=np.uint8)
    cv2.rectangle(rectangle_mask, (x_min, y_min), (x_max, y_max), 255, thickness=-1)

    # Apply the rectangle mask to the binary image
    binary = cv2.bitwise_and(binary, rectangle_mask)

    return binary

def detect_curve(binary_image):
    """
    Detect curve based on the binary image and average y-coordinates for each x-coordinate.
    
    Args:
        binary_image: Binary image where the curve is highlighted.
    
    Returns:
        List of (x, y) coordinates where the curve is detected, with averaged y-coordinates for each x.
    """
    # Detect pixels in the binary image
    ys, xs = np.where(binary_image == 255)
    
    # Group y-coordinates by x-coordinate and calculate the average y for each x
    unique_xs = np.unique(xs)
    averaged_points = []
    for x in unique_xs:
        y_values = ys[xs == x]
        avg_y = (np.min(y_values) + np.max(y_values)) / 2  # Average y-coordinate
        averaged_points.append((x, avg_y))
    
    return averaged_points
