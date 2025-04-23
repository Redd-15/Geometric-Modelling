from image_processing import preprocess_image, detect_curve
from data_extraction import pixel_to_data_coords
from interpolation import interpolate_lagrange, interpolate_spline
from visualization import plot_results_both, plot_only_data, plot_binary_image, plot_results_spline
from utils import downsample_points
import numpy as np

def main():
    image_path = "C:/Users/sikor/Documents/ME/Geometric-Modelling/Graph-Extraction/test_images/test.png"
    image, preprocessed_image, axes_info = preprocess_image(image_path, target_color=(95, 142, 203))

    # Plot the binary image for debugging
    plot_binary_image(preprocessed_image, title="Preprocessed Image")
    
    # Detect curve pixels
    curve_pixels = detect_curve(preprocessed_image) 
    
    # Convert pixel coordinates to data coordinates
    data_points = pixel_to_data_coords(curve_pixels, axes_info)

    # Separate x and y values
    x_vals, y_vals = zip(*data_points)
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)

    # Downsample the data points for faster processing
    #num_points = 100  # Adjust the number of points to retain
    #x_vals, y_vals = downsample_points(x_vals, y_vals, num_points)

    # Ensure there are enough points for interpolation
    if len(x_vals) < 2 or len(y_vals) < 2:
        raise ValueError("Not enough data points after downsampling for interpolation.")

    # Perform interpolation
    #lagrange_func, lagrange_expr = interpolate_lagrange(x_vals, y_vals)
    spline_func = interpolate_spline(x_vals, y_vals)
 
    # Plot the results
    plot_results_spline(x_vals, y_vals, spline_func, image)
    #plot_only_data(x_vals, y_vals, image)

if __name__ == "__main__":
    main()
