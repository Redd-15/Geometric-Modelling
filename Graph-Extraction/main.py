from image_processing import preprocess_image, detect_curve
from data_extraction import pixel_to_data_coords
from interpolation import interpolate_lagrange, interpolate_spline
from visualization import plot_results

def main():
    image_path = "C:/Users/sikor/Documents/ME/Geometric-Modelling/Graph-Extraction/test_images/test.png"
    preprocessed, axes_info = preprocess_image(image_path)
    curve_pixels = detect_curve(preprocessed)
    
    data_points = pixel_to_data_coords(curve_pixels, axes_info)

    x_vals, y_vals = zip(*data_points)

    lagrange_poly = interpolate_lagrange(x_vals, y_vals)
    spline_func = interpolate_spline(x_vals, y_vals)

    plot_results(x_vals, y_vals, lagrange_poly, spline_func)

if __name__ == "__main__":
    main()
