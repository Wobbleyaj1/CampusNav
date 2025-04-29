import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk
from matplotlib.patches import FancyBboxPatch

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

def parse_route_details(route_text):
    """Parse route details from the route text."""
    route_details = route_text.split(":")[1].strip()
    location_names_part = route_details.split(" (")[0]
    location_names = location_names_part.strip("[]").replace("'", "").split(", ")

    distance_start = route_text.rfind("(Distance: ") + len("(Distance: ")
    distance_end = route_text.rfind("m)")
    distance = route_text[distance_start:distance_end].strip()

    return location_names, distance


def format_route_label(current_index, history, location_names, distance):
    """Format the route label text."""
    if len(location_names) >= 2:
        from_location = location_names[0]
        to_location = location_names[-1]
        route_index = f"Route {current_index + 1}/{len(history)}"
        return f"{route_index}\nFrom: {from_location}\nTo: {to_location}\nDistance: {distance}m"
    else:
        return "Invalid route data."


def update_route_on_map(ax, canvas, location_manager, location_names):
    """Update the route on the map."""
    # Convert location names to IDs
    location_ids = [location_manager.get_location_id(name) for name in location_names]

    # Clear the previous route line from the map
    for line in ax.lines:
        if line.get_label() == "Shortest Route":
            line.remove()

    # Get coordinates for the route and draw it on the map
    route_coords = [
        location_manager.get_location_coordinates(location_id) for location_id in location_ids
    ]
    x_coords, y_coords = zip(*route_coords)
    ax.plot(x_coords, y_coords, color="red", linewidth=2, label="Shortest Route")
    ax.legend()
    canvas.draw()
    
def create_popup_window(title, width, height):
    """Create and configure a popup window."""
    popup = tk.Toplevel()
    popup.title(title)
    popup.geometry(f"{width}x{height}")
    return popup

def clear_current_marker(current_marker, ax):
    """Clear the current marker from the map."""
    if current_marker and current_marker[0] in ax.lines:
        current_marker[0].remove()

def render_location_info(ax, canvas, text, textX, textY):
    """Render location info as a text box on the map."""
    # Clear previous info card
    if hasattr(render_location_info, "previous_text_obj") and render_location_info.previous_text_obj:
        if render_location_info.previous_text_obj in ax.texts:
            render_location_info.previous_text_obj.remove()
        render_location_info.previous_text_obj = None

    if hasattr(render_location_info, "previous_box") and render_location_info.previous_box:
        if render_location_info.previous_box in ax.patches:
            render_location_info.previous_box.remove()
        render_location_info.previous_box = None

    # Render the new text
    text_obj = ax.text(textX, textY, text, va='top', ha='left')
    renderer = canvas.get_renderer()
    bbox = text_obj.get_window_extent(renderer=renderer)
    inv = ax.transData.inverted()
    bbox_data = bbox.transformed(inv)

    # Draw a box around the text
    width = bbox_data.width
    height = bbox_data.height
    box = FancyBboxPatch((textX - 10, textY - height - 10), width + 20, height + 20,
                         boxstyle="round,pad=3", edgecolor='black',
                         facecolor='lightyellow', zorder=1)
    ax.add_patch(box)

    # Save references to the current text and box
    render_location_info.previous_text_obj = text_obj
    render_location_info.previous_box = box

    # Render to canvas
    canvas.draw()

def add_menu_buttons(menu_frame, buttons):
    """Add buttons to the menu frame."""
    for text, command in buttons:
        button = tk.Button(menu_frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)