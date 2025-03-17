import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource

# Define the parametric torus surface.
# You can change these equations to visualize other surfaces.
def torus(u, v, R=2, r=1):
    """
    Parametric equations for a torus.
    u, v are parameters in [0, 2*pi].
    R is the distance from the center of the tube to the center of the torus.
    r is the radius of the tube.
    """
    x = (R + r * np.cos(u)) * np.cos(v)
    y = (R + r * np.cos(u)) * np.sin(v)
    z = r * np.sin(u)
    return x, y, z

# Compute partial derivatives (tangent vectors) analytically for a torus.
def torus_derivatives(u, v, R=2, r=1):
    # Partial derivative with respect to u
    du_x = -r * np.sin(u) * np.cos(v)
    du_y = -r * np.sin(u) * np.sin(v)
    du_z = r * np.cos(u)
    du = np.array([du_x, du_y, du_z])
    
    # Partial derivative with respect to v
    dv_x = -(R + r * np.cos(u)) * np.sin(v)
    dv_y = (R + r * np.cos(u)) * np.cos(v)
    dv_z = 0
    dv = np.array([dv_x, dv_y, dv_z])
    
    return du, dv

# Choose a specific (u0, v0) for which we display the point,
# the parameter lines (tangent directions) and the surface normal.
u0 = np.pi / 4   # adjust as desired
v0 = np.pi / 3   # adjust as desired

# Evaluate the surface point at (u0, v0)
point = np.array(torus(u0, v0))
# Compute the tangent vectors at (u0, v0)
du, dv = torus_derivatives(u0, v0)
# Surface normal: cross product of du and dv (and then normalize)
normal = np.cross(du, dv)
normal = normal / np.linalg.norm(normal)

# Set up a grid for u and v to plot the surface.
u = np.linspace(0, 2*np.pi, 60)
v = np.linspace(0, 2*np.pi, 60)
U, V = np.meshgrid(u, v)
X, Y, Z = torus(U, V)

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

# Labeling and view adjustments.
ax.set_title("Parametric Surface Visualization with Parameter Lines and Normal")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()

# Improve layout and display the plot.
plt.tight_layout()
plt.show()
