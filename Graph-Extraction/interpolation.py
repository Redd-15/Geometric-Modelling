from scipy.interpolate import CubicSpline

def interpolate_spline(x_vals, y_vals):
    return CubicSpline(x_vals, y_vals)
