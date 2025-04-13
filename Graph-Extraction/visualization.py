import numpy as np
import matplotlib.pyplot as plt
import cv2

def plot_results(x_vals, y_vals, lagrange_poly, spline_func, original_image):
    """
    Plot the results of interpolation with the original image as the background.
    
    Args:
        x_vals: List of x-coordinates of the extracted points.
        y_vals: List of y-coordinates of the extracted points.
        lagrange_poly: Lagrange interpolation polynomial function.
        spline_func: Cubic spline interpolation function.
        original_image: Original image to use as the background.
    """
    x_range = np.linspace(min(x_vals), max(x_vals), 500)

    y_lagrange = lagrange_poly(x_range)
    y_spline = spline_func(x_range)

    # Plot the original image as the background
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), extent=[min(x_vals), max(x_vals), min(y_vals), max(y_vals)], aspect='auto')

    # Plot the extracted points
    plt.scatter(x_vals, y_vals, color='red', label="Extracted Points", zorder=2)

    # Plot the interpolation results
    plt.plot(x_range, y_lagrange, color='blue', label="Lagrange Interpolation", zorder=1)
    plt.plot(x_range, y_spline, color='green', linestyle='dashed', label="Cubic Spline Interpolation", zorder=1)

    plt.legend()
    plt.grid(True)
    plt.title("Graph Data Interpolation with Original Image")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_only_data(x_vals, y_vals, original_image):
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), extent=[min(x_vals), max(x_vals), min(y_vals), max(y_vals)], aspect='auto')
    plt.scatter(x_vals, y_vals, color='red',  label="Extracted Points")
    plt.legend()
    plt.grid(True)
    plt.title("Extracted Data Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_binary_image(binary_image, title="Binary Image"):
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