import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
from image_processing import preprocess_image, detect_curve
from data_extraction import pixel_to_data_coords
from interpolation import interpolate_spline
from visualization import plot_results_spline

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
        self.image_path_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_image).grid(row=0, column=2, padx=5, pady=5)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.root, width=800, height=500, bg="#1E1E1E", highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.select_corner)

        # Input for base values in a single row
        ttk.Label(self.root, text="x_min:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.x_min_entry = ttk.Entry(self.root, width=10)
        self.x_min_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="x_max:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.x_max_entry = ttk.Entry(self.root, width=10)
        self.x_max_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="y_min:").grid(row=2, column=4, padx=5, pady=5, sticky="e")
        self.y_min_entry = ttk.Entry(self.root, width=10)
        self.y_min_entry.grid(row=2, column=5, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="y_max:").grid(row=2, column=6, padx=5, pady=5, sticky="e")
        self.y_max_entry = ttk.Entry(self.root, width=10)
        self.y_max_entry.grid(row=2, column=7, padx=5, pady=5, sticky="w")

        # Process button
        ttk.Button(self.root, text="Process", command=self.process_image).grid(row=3, column=0, columnspan=8, pady=10)

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
        # Convert the image to a format suitable for Tkinter
        image = Image.fromarray(image)
        image = image.resize((800, 500), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def select_corner(self, event):
        # Record the clicked corner
        if len(self.grid_corners) < 2:
            x, y = event.x, event.y
            self.grid_corners.append((x, y))
            self.canvas.create_oval(x-5, y-5, x+5, y+5, outline="red", width=2)
        if len(self.grid_corners) == 2:
            messagebox.showinfo("Info", "Grid corners selected!")

    def process_image(self):
        # Ensure all inputs are provided
        if not self.image_path:
            messagebox.showerror("Error", "Please provide an image.")
            return
        if len(self.grid_corners) < 2:
            messagebox.showerror("Error", "Please select two grid corners.")
            return
        
        try:
            # Get base values from user input
            self.base_values["x_min"] = float(self.x_min_entry.get())
            self.base_values["x_max"] = float(self.x_max_entry.get())
            self.base_values["y_min"] = float(self.y_min_entry.get())
            self.base_values["y_max"] = float(self.y_max_entry.get())

            # Process the image
            print("Processing image...")
            image, preprocessed_image, axes_info = preprocess_image(self.image_path, target_color=(95, 142, 203))
            print("Preprocessing done...")
            curve_pixels = detect_curve(preprocessed_image)
            data_points = pixel_to_data_coords(curve_pixels, axes_info)

            # Separate x and y values
            x_vals, y_vals = zip(*data_points)
            x_vals = np.array(x_vals)
            y_vals = np.array(y_vals)

            # Perform interpolation
            spline_func = interpolate_spline(x_vals, y_vals)

            # Display the results
            plot_results_spline(x_vals, y_vals, spline_func, self.image)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()