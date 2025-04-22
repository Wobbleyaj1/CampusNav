import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def plot_locations(locations, background_image_path=None):
    """Plot the locations on a 2D map using matplotlib with an optional background image."""
    if not locations:
        print("No locations available to plot.")
        return

    x_coords = []
    y_coords = []
    labels = []

    for name, coordinates in locations.items():
        try:
            x, y = map(int, coordinates.split(","))
            x_coords.append(x)
            y_coords.append(y)
            labels.append(name)
        except ValueError:
            print(f"Invalid coordinates for location '{name}': {coordinates}")

    # Create the plot
    plt.figure(figsize=(10, 8))

    # Add background image
    if background_image_path:
        try:
            print(f"Loading background image from: {background_image_path}")
            img = mpimg.imread(background_image_path)

            # Define the extent to center the image around (0, 0)
            img_height, img_width = 1674, 2600
            extent = [-img_width // 2, img_width // 2, -img_height // 2, img_height // 2]

            plt.imshow(img, extent=extent, aspect='auto')
        except FileNotFoundError:
            print(f"Background image not found at: {background_image_path}")

    # Plot the locations
    plt.scatter(x_coords, y_coords, color="blue", label="Locations")
    
    # Annotate each point with its name
    for i, label in enumerate(labels):
        plt.annotate(
            label,
            (x_coords[i], y_coords[i]),
            textcoords="offset points",
            xytext=(5, 5),
            ha="center",
            fontsize=8,  # Smaller font size
            fontweight="bold"  # Bold text
        )

    # Add labels and title
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Campus Map")
    plt.grid(True)
    plt.legend()
    plt.show()