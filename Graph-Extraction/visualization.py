import numpy as np
import matplotlib.pyplot as plt

def plot_results(x_vals, y_vals, lagrange_poly, spline_func):
    x_range = np.linspace(min(x_vals), max(x_vals), 500)

    y_lagrange = lagrange_poly(x_range)
    y_spline = spline_func(x_range)

    plt.scatter(x_vals, y_vals, label="Extracted Points")
    plt.plot(x_range, y_lagrange, label="Lagrange Interpolation")
    plt.plot(x_range, y_spline, label="Cubic Spline Interpolation", linestyle='dashed')
    plt.legend()
    plt.grid(True)
    plt.title("Graph Data Interpolation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_only_data(x_vals, y_vals):
    plt.scatter(x_vals, y_vals, label="Extracted Points")
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