def pixel_to_data_coords(pixel_points, density=1):
    data_points = []
    for i, (x, y) in enumerate(pixel_points):
        if i % density == 0:  # Only append every nth point
            data_x = x
            data_y = y
            data_points.append((data_x, data_y))
    if data_points[-1] != pixel_points[-1]:
        data_points.append(pixel_points[-1])
    return data_points
