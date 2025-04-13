from image_processing import preprocess_image, detect_curve
from data_extraction import pixel_to_data_coords
from interpolation import interpolate_lagrange, interpolate_spline
from visualization import plot_results, plot_only_data

def main():
    image_path = "C:/Users/sikor/Documents/ME/Geometric-Modelling/Graph-Extraction/test_images/test.png"
    preprocessed_image, axes_info = preprocess_image(image_path, target_color=(95, 142, 203))
    curve_pixels = detect_curve(preprocessed_image) 
    
    data_points = pixel_to_data_coords(curve_pixels, axes_info)

    x_vals, y_vals = zip(*data_points)
    #print (data_points)

    #lagrange_poly = interpolate_lagrange(x_vals, y_vals)
    #spline_func = interpolate_spline(x_vals, y_vals)
 
    plot_only_data(x_vals, y_vals)
    #plot_results(x_vals, y_vals, lagrange_poly, spline_func)

if __name__ == "__main__":
    main()
