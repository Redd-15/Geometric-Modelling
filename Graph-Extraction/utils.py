from scipy.spatial.distance import cdist
import numpy as np

def downsample_points(x_vals, y_vals, num_points):
    """
    Downsample points to retain the overall structure of the curve.

    Args:
        x_vals: Array of x-coordinates.
        y_vals: Array of y-coordinates.
        num_points: Number of points to retain.

    Returns:
        Downsampled x and y coordinates.
    """
    points = np.column_stack((x_vals, y_vals))
    selected_points = [points[0]]  # Start with the first point

    # Iteratively select points based on distance
    for _ in range(num_points - 1):
        remaining_points = np.array([p for p in points if not any(np.allclose(p, sp) for sp in selected_points)])
        distances = cdist([selected_points[-1]], remaining_points).flatten()
        next_point = remaining_points[np.argmax(distances)]
        selected_points.append(next_point)

    selected_points = np.array(selected_points)
    return selected_points[:, 0], selected_points[:, 1]

def hex_to_bgr(hex_color):
    """
    Convert a hex color code to BGR format for OpenCV.
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))

def linear_interpolation(val, in_min, in_max, out_min, out_max):
    """
    Perform linear interpolation to map a value from one range to another.
    
    Args:
        val: The value to interpolate.
        in_min: Minimum of the input range.
        in_max: Maximum of the input range.
        out_min: Minimum of the output range.
        out_max: Maximum of the output range.
    
    Returns:
        Interpolated value in the output range.
    """
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def validate_float_input(value, field_name):
    """
    Validate that the input value can be converted to a float.
    
    Args:
        value: The input value as a string.
        field_name: The name of the field (for error messages).
    
    Returns:
        The input value converted to a float.
    
    Raises:
        ValueError: If the input value is empty or cannot be converted to a float.
    """
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid number.")
    
def RGB2BRG_in_hex(rgb):
    return f"#{rgb[5:7]}{rgb[3:5]}{rgb[1:3]}"