import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from utils import hex_to_bgr

def plot_results_spline(x_vals, y_vals, spline_func, original_image, selected_points, show_points, show_spline, points_color, spline_color):
    """
    Draw the results of spline interpolation directly onto the original image using OpenCV.
    
    Args:
        x_vals: List of x-coordinates of the extracted points.
        y_vals: List of y-coordinates of the extracted points.
        spline_func: Cubic spline interpolation function.
        original_image: Original image to use as the background.
        selected_points: The points selected by the user for the first and last datapoints.
        show_points: Boolean indicating whether to show the extracted points on the image.
        show_spline: Boolean indicating whether to show the spline curve on the image.
    
    Returns:
        A PIL Image object that can be displayed in a Tkinter canvas.
    """
    # Make a copy of the original image to avoid modifying it directly
    image_copy = original_image.copy()
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)  # Convert to RGB for PIL compatibility

    # Generate x range for interpolation
    if show_points or show_spline:
        
        if not (selected_points and len(selected_points) == 2):
            raise ValueError("Invalid points selected. Please select two points.")
        
        x_range = np.linspace(min(x_vals), max(x_vals), max(x_vals) - min(x_vals) + 1)
        y_spline = spline_func(x_range)

        # Draw the extracted points
        if show_points:
            for x, y in zip(x_vals, y_vals):
                cv2.circle(image_copy, (int(x), int(y)), radius=5, color=hex_to_bgr(points_color), thickness=-1)

        # Draw the spline curve
        
        if show_spline:    
            spline_points = np.array([[int(x), int(y)] for x, y in zip(x_range, y_spline)], dtype=np.int32)
            cv2.polylines(image_copy, [spline_points], isClosed=False, color=hex_to_bgr(spline_color), thickness=2)

    # Convert the OpenCV image (BGR) to a PIL Image (RGB)
    image_rgb = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)

def plot_only_data(x_vals, y_vals, original_image): #matplotlib ONLY
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), extent=[min(x_vals), max(x_vals), min(y_vals), max(y_vals)], aspect='auto')
    plt.scatter(x_vals, y_vals, color='red',  label="Extracted Points")
    plt.legend()
    plt.grid(True)
    plt.title("Extracted Data Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_binary_image(binary_image, title="Binary Image"): #matplotlib ONLY
    """
    Plot a binary image using Matplotlib.
    
    Args:
        binary_image: 2D numpy array representing the binary image.
        title: Title of the plot (default is "Binary Image").
    """
    plt.imshow(binary_image, cmap='gray')
    plt.title(title)
    plt.axis('off')  # Hide axes for better visualization
    plt.show()