def pixel_to_data_coords(pixel_points, axes_info):
    data_points = []
    for x, y in pixel_points:
        data_x = (x - axes_info["x_origin"]) * axes_info["x_scale"]
        data_y = (axes_info["y_origin"] - y) * axes_info["y_scale"]
        data_points.append((data_x, data_y))
    return data_points
