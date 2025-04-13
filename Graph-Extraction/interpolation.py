from scipy.interpolate import CubicSpline
from numpy.polynomial.polynomial import Polynomial
import numpy as np
from scipy.interpolate import lagrange as scipy_lagrange

def interpolate_lagrange(x_vals, y_vals):
    return scipy_lagrange(x_vals, y_vals)

def interpolate_spline(x_vals, y_vals):
    return CubicSpline(x_vals, y_vals)
