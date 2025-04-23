from scipy.interpolate import CubicSpline
from numpy.polynomial.polynomial import Polynomial
from sympy import symbols, expand, lambdify

def interpolate_lagrange(x_vals, y_vals):
    """
    Uses symbolic Lagrange interpolation and returns a function and its symbolic polynomial.
    """
    x = symbols('x')
    n = len(x_vals)
    poly = 0
    for i in range(n):
        term = y_vals[i]
        for j in range(n):
            if i != j:
                term *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        poly += term

    poly = expand(poly)
    f_lambdified = lambdify(x, poly, modules='numpy')
    return f_lambdified, poly

def interpolate_spline(x_vals, y_vals):
    return CubicSpline(x_vals, y_vals)
