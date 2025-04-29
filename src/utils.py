import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk

def extract_coordinates_and_labels(locations):
    """Extract x, y coordinates and labels from the locations list."""
    x_coords = []
    y_coords = []
    labels = []

    for location in locations:
        try:
            x_coords.append(location["x"])
            y_coords.append(location["y"])
            labels.append(location["name"])
        except KeyError as e:
            print(f"Missing key {e} in location: {location}")

    return x_coords, y_coords, labels

def add_background_image(ax, background_image_path):
    """Add a background image to the plot."""
    if background_image_path:
        try:
            img = mpimg.imread(background_image_path)
            img_height, img_width = 1674, 2600
            extent = [-img_width // 2, img_width // 2, -img_height // 2, img_height // 2]
            ax.imshow(img, extent=extent, aspect='auto')
        except FileNotFoundError:
            print(f"Background image not found at: {background_image_path}")

def plot_locations(locations, background_image_path=None, allow_selection=False):
    """
    Plot the locations on a 2D map using matplotlib with an optional background image.
    Optionally allow the user to select a point on the map.
    
    Args:
        locations (dict): Dictionary of location names and their coordinates.
        background_image_path (str): Path to the background image.
        allow_selection (bool): If True, allow the user to select a point on the map.
    
    Returns:
        tuple or None: Selected coordinates (x, y) if allow_selection is True, otherwise None.
    """
    if not locations:
        print("No locations available to plot.")
        return None

    # Extract coordinates and labels
    x_coords, y_coords, labels = extract_coordinates_and_labels(locations)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Add background image
    add_background_image(ax, background_image_path)

    # Plot the locations
    ax.scatter(x_coords, y_coords, color="blue", label="Locations")

    # Annotate each point with its name
    for i, label in enumerate(labels):
        ax.annotate(
            label,
            (x_coords[i], y_coords[i]),
            textcoords="offset points",
            xytext=(5, 5),
            ha="center",
            fontsize=8,
            fontweight="bold"
        )

    # Add labels and title
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Campus Map")
    plt.grid(True)
    plt.legend()

    # Handle point selection if enabled
    selected_point = []
    if allow_selection:
        def onclick(event):
            if event.xdata and event.ydata:
                selected_point.append((int(event.xdata), int(event.ydata)))
                plt.close()

        fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return selected_point[0] if selected_point else None

def select_nearest_location(event, locations):
    """Find the nearest location to the clicked coordinates."""
    if event.xdata is not None and event.ydata is not None:
        nearest_location = min(
            locations,
            key=lambda loc: ((loc["x"] - event.xdata) ** 2 + (loc["y"] - event.ydata) ** 2) ** 0.5,
        )
        return nearest_location
    return None