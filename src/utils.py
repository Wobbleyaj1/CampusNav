import matplotlib.pyplot as plt

def plot_locations(locations):
    """Plot the locations on a 2D map using matplotlib."""
    if not locations:
        print("No locations available to plot.")
        return

    # Extract coordinates and labels
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
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color="blue", label="Locations")
    
    # Annotate each point with its name
    for i, label in enumerate(labels):
        plt.annotate(label, (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(5, 5), ha="center")

    # Add labels and title
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Campus Map")
    plt.grid(True)
    plt.legend()
    plt.show()