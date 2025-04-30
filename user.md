## Complex Software Engineering Problem

The Campus Navigation System addresses the complex problem of providing an intuitive and interactive solution for navigating large and intricate campus environments. It integrates advanced data structures, such as graphs for shortest path calculations and trees for hierarchical location categorization, with a user-friendly graphical interface. The system ensures efficient route planning, location search, and real-time interaction, solving challenges related to spatial data visualization, user accessibility, and dynamic route management.

## Accessing and Using the Software

### Prerequisites
To use the Campus Navigation System, ensure the following prerequisites are met:
- Python 3.8 or higher is installed on your system.
- Required Python libraries are installed. These can be found in the `requirements.txt` file.

### Installation and Setup
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-repo/CampusNav.git
   cd CampusNav
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Navigate to the src directory:
   ```bash
   cd src
   ```

2. Run the main application
   ```bash
   python main.py
   ```

3. The application will launch a graphical user interface (GUI) displaying the campus map.

### Using the Application
Search for a Location: Use the "Search for a location" button to find specific locations on the map.
Find Shortest Route: Click "Find shortest route" to calculate and display the shortest path between two locations.
Walking Guide: Use the "Walking Guide" feature for step-by-step navigation.
View Route History: Access previously traversed routes using the "View route history" button.
Frequent Locations: View commonly visited locations with the "Frequent Locations" option.
Exit: Close the application by clicking the "Exit" button.

## Classes and Methods Developed

### CampusNavigationApp
The `CampusNavigationApp` class serves as the main controller for the application, managing the user interface and interactions with the campus map.

#### Key Methods:
- **`__init__`**: Initializes the application, setting up the map and user interface components.
- **`initialize_map()`**: Loads the campus map, displays locations, and sets up the graphical interface.
- **`update_prompt_text(text: str)`**: Updates the prompt text displayed on the map.
- **`clear_info_card()`**: Clears any displayed information cards on the map.
- **`display_info_card(name: str, x: int, y: int)`**: Displays an information card for a selected location, constrained within the map bounds.
- **`normal_click(event)`**: Handles normal click events, selecting the nearest location and displaying its information.
- **`search_location()`**: Allows users to search for a location and display its information.

### LocationManager
The `LocationManager` class manages the data related to campus locations, including their coordinates and features.

#### Key Methods:
- **`get_visible_Locations()`**: Retrieves a list of locations currently visible on the map.
- **`location_features`**: A dictionary mapping location names to their notable features.

### Utility Functions
- **`render_location_info(ax, canvas, text, x, y)`**: Renders an information card at the specified position on the map.
- **`clear_current_marker(marker, ax)`**: Clears the current marker from the map.
- **`select_nearest_location(event, locations)`**: Selects the location nearest to the user's click event.
- **`add_background_image(ax, image_path)`**: Adds a background image to the map.

### Data Structures
- **Graph**: Used for shortest path calculations between locations.
- **Tree**: Used for hierarchical categorization of locations.
- **Stack/Queue**: Utilized for managing user interactions and route history.