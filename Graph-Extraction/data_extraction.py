import numpy as np
from tkinter import filedialog
from utils import interpolate_linearly

def convert_pixel_to_data_coords(pixel_points, density=1):
    data_points = []
    for i, (x, y) in enumerate(pixel_points):
        if i % density == 0:  # Only append every nth point
            data_x = x
            data_y = y
            data_points.append((data_x, data_y))
    if data_points[-1] != pixel_points[-1]:
        data_points.append(pixel_points[-1])
    return data_points

def calculate_y_value(x_input, base_values, grid_corners, invert_x_axis, spline_func):
        """
        Calculate the y value for the given x input using the spline interpolation.
        """
        try:

            # Ensure the x value is within the valid range
            if not (base_values["x_min"] <= x_input <= base_values["x_max"]):
                raise ValueError(f"x value must be between {base_values['x_min']} and {base_values['x_max']}.")
                

            # Interpolate x_input to pixel coordinates (grid corners)
            if invert_x_axis:
                x_pixel = grid_corners[1][0] + grid_corners[0][0] - interpolate_linearly(
                    x_input,
                    base_values["x_min"],
                    base_values["x_max"],
                    grid_corners[0][0],
                    grid_corners[1][0]# Reverse the mapping for inverted x-axis
                )
            else:
                x_pixel = interpolate_linearly(
                    x_input,
                    base_values["x_min"],
                    base_values["x_max"],
                    grid_corners[0][0],
                    grid_corners[1][0]
                )

            # Use the spline function to calculate the corresponding pixel y value
            y_pixel = spline_func(x_pixel)

            # Interpolate y_pixel back to data coordinates (y_min to y_max)
            y_value = interpolate_linearly(
                y_pixel,
                grid_corners[1][1],  # Note: Reverse the mapping for y-axis inversion
                grid_corners[0][1],
                base_values["y_min"],
                base_values["y_max"]
            )

            return x_pixel, y_value
        
        except ValueError:
            raise ValueError(e)
        except Exception as e:
            raise Exception(e)

def export_to_csv(spline_func, x_min, x_max, num_points, base_values, grid_corners, invert_x_axis):
    """
    Export the specified number of (x, y) points to a CSV file.

    Args:
        spline_func: The spline function to calculate y values.
        x_min: The minimum x value.
        x_max: The maximum x value.
        num_points: The number of points to export.

    Returns:
        None
    """
    try:
        # Generate evenly spaced x values between x_min and x_max
        x_values = np.linspace(x_min, x_max, num_points)

        # Calculate corresponding y values using the spline function
        y_values = [calculate_y_value(x, base_values, grid_corners, invert_x_axis, spline_func)[1] for x in x_values]

        # Ask the user for a file location to save the CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return  # User canceled the save dialog

        # Write the data to the CSV file
        with open(file_path, "w") as file:
            file.write("x,y\n")  # Write the header
            for x, y in zip(x_values, y_values):
                file.write(f"{x},{y}\n")

        return file_path  # Return the file path for confirmation

    except ValueError as e:
        raise ValueError(e)
    except Exception as e:
        raise Exception(e)

