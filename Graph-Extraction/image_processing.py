import cv2
import numpy as np
from utils import hex_to_bgr

def preprocess_image(image, target_HEX_color):
    """
    Preprocess the image to generate a binary mask for the target color.
    
    Args:
        image_path: Path to the input image.
        target_color: Tuple representing the BGR color to detect (e.g., (255, 0, 0) for blue).
    
    Returns:
        binary: Binary image where the target color is highlighted.
    """
    COLOR_TRESHOLD = 20 # Allowable color variation
    target_color = hex_to_bgr(target_HEX_color)  # Convert hex color to BGR format
    # Create a mask for the target color
    lower_bound = np.array(target_color) - COLOR_TRESHOLD
    upper_bound = np.array(target_color) + COLOR_TRESHOLD
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Convert the mask to binary format
    _, binary = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    
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
