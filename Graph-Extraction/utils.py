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