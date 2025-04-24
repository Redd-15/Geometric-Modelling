# Geometric modelling coursework and assignment
**Name:** Sikora Dávid ádám \
**Neptune:** IRE699 \
**Semester:** 2024/25/II

## Coursework
* JavaScript 2D curve implementations:
    * Lagrange interpolation
    * de Casteljau algorithm with a slider to set parameter (resulting Bezier curve traced)
    * NURBS approximation
* Python surface implementation:
    * visualize a given surface and its normal vector
    * calculations by hand for the same surface and its tangent plane

## Assignment - Graph data reading app

**Goal**: Read graph images → extract raw data points → perform interpolation (Lagrange, Spline) → visualize.
## **Step-by-Step Development Plan**

### **1. Input Handling**
- **Objective**: Load graph images into your program.
  - Use `Pillow`, `OpenCV`, or `matplotlib` for image input.


### **2. Preprocessing the Image**
- **Objective**: Prepare the image for feature extraction.
  - Convert to grayscale or binary (thresholding) using `OpenCV`.
  - Apply edge detection (e.g., Canny). (**Not needed.**)
  - Clean up noise (morphological operations: erosion, dilation).

### **3. Axis and Scale Detection**
- **Objective**: Detect axes and determine the coordinate system.
  - Identify x- and y-axes using Hough line transform.
  - Optionally ask user to mark known points or origin.
  - Implement a manual mode if auto-detection fails. (**Stayed at simplest solution for maximising accuracy.**)

### **4. Data Point Extraction**
- **Objective**: Extract coordinates of the plotted curve.
  - Detect curve pixels using color or intensity segmentation.
  - Transform image coordinates to data coordinates based on axis scale.
  - Interpolate or simplify points (e.g., with Ramer–Douglas–Peucker algorithm). (**Point density can be choosen by user.**)

### **5. Coordinate Calibration**
- **Objective**: Map image pixel positions to actual (x, y) data values.
  - Use known axis limits or allow user input.
  - Linearly scale pixel coordinates accordingly.

### **6. Interpolation Algorithms**
- **Objective**: Implement mathematical interpolation.
  - Implement **Lagrange interpolation** (manual or via `scipy.interpolate.lagrange`). (**Removed, because of high number of points!**)
  - Implement **Cubic Spline interpolation** (e.g., `scipy.interpolate.CubicSpline`).

### **7. Visualization**
- **Objective**: Plot the raw and interpolated data.
  - Use `matplotlib` to plot:
    - Extracted raw data points.
    - Lagrange and Spline interpolation curves.
  - Optionally overlay original graph image as background.

### **8. User Interface (Optional but Helpful)**
- **Objective**: Create a simple interface for usability.
  - Use `Tkinter`, or `PyQt`.
  - Allow: image upload, axis calibration, method selection, result export.

### **9. Export Results**
- **Objective**: Provide output in usable formats.
  - Save interpolated function results to CSV or TXT.
  - Save plots as PNG/PDF. (Not required if csv export is possible)
  - Allow function export (e.g., as symbolic expression using `sympy`). (**Possible, but not implemented.**)


> [!IMPORTANT]
> **Out of the 9 objectives all were met during development. Some was only possible in part, but I would say the project was highly succesful**
