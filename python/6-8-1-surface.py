import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource

# Define the parametric surface.
def surface(x, y):
    """
    Parametric equations for the surface.
    x, y are parameters.
    """
    z = x**3 + (x - 2)**2 + (y + 1)**3 - (y + 2)**2
    return z

# Compute partial derivatives (tangent vectors) analytically for the surface.
def surface_derivatives(x, y):
    # Partial derivative with respect to x
    dz_dx = 3*x**2 + 2*(x - 2)
    
    # Partial derivative with respect to y
    dz_dy = 3*(y + 1)**2 - 2*(y + 2)
    
    return dz_dx, dz_dy

# Choose a specific (x0, y0) for which we display the point,
# the parameter lines (tangent directions) and the surface normal.
x0 = 1   # adjust as desired
y0 = 2   # adjust as desired

# Evaluate the surface point at (x0, y0)
z0 = surface(x0, y0)
point = np.array([x0, y0, z0])

# Compute the tangent vectors at (x0, y0)
dz_dx, dz_dy = surface_derivatives(x0, y0)
du = np.array([1, 0, dz_dx])
dv = np.array([0, 1, dz_dy])

# Surface normal: cross product of du and dv (and then normalize)
normal = np.cross(du, dv)
normal = normal / np.linalg.norm(normal)

# Set up a grid for x and y to plot the surface.
x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = surface(X, Y)

# Create a light source to simulate shading.
ls = LightSource(azdeg=45, altdeg=65)
# Use the light source to shade the colormap (here using the "viridis" colormap).
rgb = ls.shade(Z, cmap=cm.viridis, blend_mode='soft')

# Create the figure and 3D axes.
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with vivid colors.
ax.plot_surface(X, Y, Z, facecolors=rgb, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

# Highlight the selected surface point.
ax.scatter(point[0], point[1], point[2], color='r', s=100, label='Surface Point')

# Plot the parameter lines (tangent directions) at the point.
# We plot short segments in the direction of du and dv.
tangent_scale = 0.8
du_line = np.array([point, point + tangent_scale * du])
dv_line = np.array([point, point + tangent_scale * dv])
ax.plot(du_line[:, 0], du_line[:, 1], du_line[:, 2], color='b', linewidth=3, label='Parameter Line (du)')
ax.plot(dv_line[:, 0], dv_line[:, 1], dv_line[:, 2], color='m', linewidth=3, label='Parameter Line (dv)')

# Plot the surface normal vector at the point.
normal_scale = 1.2
normal_line = np.array([point, point + normal_scale * normal])
ax.plot(normal_line[:, 0], normal_line[:, 1], normal_line[:, 2], color='k', linewidth=3, label='Normal Vector')

# Set Z axis limits
ax.set_zlim(-10, 10)

# Labeling and view adjustments.
ax.set_title("Parametric Surface Visualization with Parameter Lines and Normal")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()

# Improve layout and display the plot.
plt.tight_layout()
plt.show()