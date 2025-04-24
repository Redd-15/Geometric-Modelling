import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import cv2
from PIL import Image, ImageTk
import numpy as np
from image_processing import preprocess_image, detect_curve
from data_extraction import pixel_to_data_coords
from interpolation import interpolate_spline
from visualization import plot_results_spline
from utils import linear_interpolation, validate_float_input, RGB2BRG_in_hex

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Interpolation App")
        self.root.geometry("900x700")
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.image_path = None
        self.image = None
        self.grid_corners = []
        self.base_values = {"x_min": 0, "x_max": 0, "y_min": 0, "y_max": 0}
        self.data_density = 1  # Default data density

        # Default colors for spline and points
        self.spline_color = "#00FF00"  # Green
        self.points_color = "#FF0000"  # Red
        self.selected_graph_color = "#FFFFFF"  # Default graph color (black)

        # Apply a modern theme
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a modern theme
        self.style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Arial", 10))
        self.style.configure("TButton", background="#4E4E4E", foreground="white", font=("Arial", 10))
        self.style.configure("TEntry", fieldbackground="#4E4E4E", foreground="white", font=("Arial", 10))

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Input for image path
        ttk.Label(self.root, text="Image Path:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.image_path_entry = ttk.Entry(self.root, width=50)
        self.image_path_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        ttk.Button(self.root, text="Browse", command=self.browse_image).grid(row=0, column=3, padx=5, pady=5)

        # Input for base values in a single column
        ttk.Label(self.root, text="X Minimum Value:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.x_min_entry = ttk.Entry(self.root, width=10)
        self.x_min_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="X Maximum Value:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.x_max_entry = ttk.Entry(self.root, width=10)
        self.x_max_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="Y Minimum Value:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.y_min_entry = ttk.Entry(self.root, width=10)
        self.y_min_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="Y Maximum Value:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.y_max_entry = ttk.Entry(self.root, width=10)
        self.y_max_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Input for datapoint density
        ttk.Label(self.root, text="Datapoint Density:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.data_density_entry = ttk.Entry(self.root, width=10)
        self.data_density_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Graph color picker button
        ttk.Button(self.root, text="Graph Color Picker", command=self.enable_graph_color_picker).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.graph_color_square = tk.Label(self.root, bg=self.selected_graph_color, width=2, height=1)
        self.graph_color_square.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Color pickers for spline and points
        ttk.Button(self.root, text="Pick Spline Color", command=self.pick_spline_color).grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.spline_color_square = tk.Label(self.root, bg=self.spline_color, width=2, height=1)
        self.spline_color_square.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(self.root, text="Pick Points Color", command=self.pick_points_color).grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.points_color_square = tk.Label(self.root, bg=self.points_color, width=2, height=1)
        self.points_color_square.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # Checkboxes for visualization options
        self.show_spline = tk.BooleanVar(value=True)
        self.show_points = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Show Spline", variable=self.show_spline, bg="#2E2E2E", fg="white", selectcolor="#4E4E4E").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.root, text="Show Points", variable=self.show_points, bg="#2E2E2E", fg="white", selectcolor="#4E4E4E").grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Buttons below the input fields
        ttk.Button(self.root, text="Process", command=self.process_image).grid(row=10, column=0, padx=5, pady=10, sticky="w")
        ttk.Button(self.root, text="Clear Points", command=self.clear_points).grid(row=10, column=1, padx=5, pady=10, sticky="w")

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.root, width=800, height=500, bg="#1E1E1E", highlightthickness=0)
        self.canvas.grid(row=1, column=2, rowspan=10, columnspan=3, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.select_corner)

        # Input field for x value and label
        ttk.Label(self.root, text="Enter x value:").grid(row=11, column=2, padx=5, pady=5, sticky="e")
        self.x_input_entry = ttk.Entry(self.root, width=15)
        self.x_input_entry.grid(row=11, column=3, padx=5, pady=5, sticky="w")
        self.x_input_entry.bind("<Return>", self.calculate_y_value)  # Trigger calculation on Enter key

        # Checkbox for inverting the x-axis
        self.invert_x_axis = tk.BooleanVar(value=False)  # Default: x-axis is not inverted
        tk.Checkbutton(self.root, text="Invert X-Axis", variable=self.invert_x_axis, bg="#2E2E2E", fg="white", selectcolor="#4E4E4E").grid(row=11, column=2, padx=5, pady=5, sticky="w")

    def browse_image(self):
        # Open file dialog to select an image
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.image_path_entry.delete(0, tk.END)
        self.image_path_entry.insert(0, self.image_path)
        self.load_image()

    def load_image(self):
        # Load and display the image on the canvas
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, image):
        """
        Display an image on the canvas. Converts NumPy arrays to PIL Image if necessary.
        
        Args:
            image: A PIL Image object or a NumPy array to display.
        """
        # Convert NumPy array to PIL Image if necessary
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        # Clear the canvas before displaying the new image
        self.canvas.delete("all")

        # Get the dimensions of the image
        width, height = image.size

        # Resize the canvas to match the image dimensions
        self.canvas.config(width=width, height=height)

        # Convert the PIL Image to a format suitable for Tkinter
        self.tk_result_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_result_image)

    def select_corner(self, event):
        """
        Record the clicked corner or remove the last selected point.
        """
        x, y = event.x, event.y

        # Add a new point if fewer or more than 2 points are selected
        if len(self.grid_corners) < 2:
            self.grid_corners.append((x, y))
            self.canvas.create_oval(x-5, y-5, x+5, y+5, outline="red", width=2)
            if len(self.grid_corners) == 2:
                messagebox.showinfo("Info", "Grid corners selected!")
        else:
            messagebox.showerror("Info", "Grid corners are already selected!")

    def clear_points(self):
        """
        Clear all selected points and reset the canvas.
        """
        self.grid_corners = []  # Clear the list of selected points
        self.canvas.delete("all")  # Clear all drawings on the canvas
        self.display_image(self.image)  # Redisplay the original image

    def process_image(self):
        # Ensure all inputs are provided
        if not self.image_path:
            messagebox.showerror("Error", "Please provide an image.")
            return
        if len(self.grid_corners) < 2:
            messagebox.showerror("Error", "Please select two grid corners.")
            return

        try:
            # Validate and get base values from user input
            self.base_values["x_min"] = validate_float_input(self.x_min_entry.get(), "x_min")
            self.base_values["x_max"] = validate_float_input(self.x_max_entry.get(), "x_max")
            self.base_values["y_min"] = validate_float_input(self.y_min_entry.get(), "y_min")
            self.base_values["y_max"] = validate_float_input(self.y_max_entry.get(), "y_max")

            # Get datapoint density
            self.data_density = int(validate_float_input(self.data_density_entry.get(), "Datapoint Density"))
            if self.data_density <= 0:
                raise ValueError("Datapoint Density must be a positive integer.")

            if self.grid_corners[0][0] > self.grid_corners[1][0]:
                self.grid_corners[0], self.grid_corners[1] = self.grid_corners[1], self.grid_corners[0]  # Swap points if necessary

            # Process the image
            preprocessed_image = preprocess_image(self.image, self.selected_graph_color)  # TODO: Make target color configurable
            curve_pixels = detect_curve(preprocessed_image)
            data_points = pixel_to_data_coords(curve_pixels, self.data_density)

            # Separate x and y values
            x_vals, y_vals = zip(*data_points)
            x_vals = np.array(x_vals)
            y_vals = np.array(y_vals)

            # Perform interpolation
            self.spline_func = interpolate_spline(x_vals, y_vals)  # Store the spline function for later use

            result_image = plot_results_spline(
                x_vals, y_vals, self.spline_func, self.image, self.grid_corners,
                self.show_points.get(), self.show_spline.get(),
                self.points_color, self.spline_color  # Pass the selected colors
            )

            # Display the result image on the canvas
            self.display_image(result_image)
            self.result_image = result_image  # Store the result image for later use

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def calculate_y_value(self, event):
        """
        Calculate the y value for the given x input using the spline interpolation
        and draw a vertical line on the canvas at the corresponding point.
        """
        try:
            # Get the x value from the input field
            x_input = float(self.x_input_entry.get())

            # Ensure the x value is within the valid range
            if not (self.base_values["x_min"] <= x_input <= self.base_values["x_max"]):
                messagebox.showerror("Error", f"x value must be between {self.base_values['x_min']} and {self.base_values['x_max']}.")
                return

            # Interpolate x_input to pixel coordinates (grid corners)
            if self.invert_x_axis.get():
                x_pixel = linear_interpolation(
                    x_input,
                    self.base_values["x_min"],
                    self.base_values["x_max"],
                    self.grid_corners[1][0],
                    self.grid_corners[0][0]  # Reverse the mapping for inverted x-axis
                )
            else:
                x_pixel = linear_interpolation(
                    x_input,
                    self.base_values["x_min"],
                    self.base_values["x_max"],
                    self.grid_corners[0][0],
                    self.grid_corners[1][0]
                )

            # Use the spline function to calculate the corresponding pixel y value
            y_pixel = self.spline_func(x_pixel)

            # Interpolate y_pixel back to data coordinates (y_min to y_max)
            y_value = linear_interpolation(
                y_pixel,
                self.grid_corners[1][1],  # Note: Reverse the mapping for y-axis inversion
                self.grid_corners[0][1],
                self.base_values["y_min"],
                self.base_values["y_max"]
            )

            # Clear the canvas and redisplay the image
            self.canvas.delete("line")  # Remove any existing vertical line
            self.display_image(self.result_image)

            # Draw a vertical line at the calculated x position
            self.canvas.create_line(
                x_pixel, 0, x_pixel, self.result_image.size[1],
                fill="blue", width=1, tags="line"
            )

            # Optionally, display the calculated y value
            messagebox.showinfo("Result", f"For x = {x_input}, y = {y_value:.2f}")

        except ValueError:
            messagebox.showerror("Error", "Invalid x value. Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def pick_spline_color(self):
        """
        Open a color picker dialog to select the color for the spline.
        Update the spline color square's background color to the selected color.
        """
        color_code = colorchooser.askcolor(title="Pick Spline Color")[1]
        if color_code:
            self.spline_color = color_code  # Store the selected color
            # Update the spline color square's background color
            self.spline_color_square.configure(bg=self.spline_color)

    def pick_points_color(self):
        """
        Open a color picker dialog to select the color for the points.
        Update the points color square's background color to the selected color.
        """
        color_code = colorchooser.askcolor(title="Pick Points Color")[1]
        if color_code:
            self.points_color = color_code  # Store the selected color
            # Update the points color square's background color
            self.points_color_square.configure(bg=self.points_color)

    def enable_graph_color_picker(self):
        """
        Enable the user to select a pixel on the image to set the graph color.
        """
        messagebox.showinfo("Info", "Click on the image to select the graph color.")
        self.canvas.bind("<Button-1>", self.pick_graph_color)  # Bind left-click to pick_graph_color

    def pick_graph_color(self, event):
        """
        Get the color of the pixel clicked on the image and store it in self.selected_graph_color.
        Update the Graph Color Picker square's background color to the selected color.
        """
        try:
            # Get the x and y coordinates of the click
            x, y = event.x, event.y

            # Ensure the image is loaded
            if self.image is None:
                messagebox.showerror("Error", "No image loaded.")
                return

            # Convert the canvas coordinates to image coordinates
            if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
                # Get the color of the pixel at (x, y)
                b, g, r = self.image[y, x]  # OpenCV uses BGR format
                self.selected_graph_color = f"#{r:02x}{g:02x}{b:02x}"  # Convert to hex format, but image is in BRG format so that needs converting too
                # Display the selected color
                messagebox.showinfo("Selected Color", f"Selected Graph Color: {self.selected_graph_color}")

                # Update the Graph Color Picker square's background color
                self.graph_color_square.configure(bg=RGB2BRG_in_hex(self.selected_graph_color))

                # Unbind the click event after selection
                self.canvas.bind("<Button-1>", self.select_corner)  # Rebind to select_corner
            else:
                messagebox.showerror("Error", "Click within the image boundaries.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()