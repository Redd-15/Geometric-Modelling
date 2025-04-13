import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Placeholder: axis detection should return scale info later
    axes_info = {"x_origin": 50, "y_origin": 450, "x_scale": 1, "y_scale": 1}
    
    return binary, axes_info

def detect_curve(binary_image):
    # Detect white pixels (i.e., curve on binary image)
    ys, xs = np.where(binary_image == 255)
    return list(zip(xs, ys))
