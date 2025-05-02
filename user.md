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
   git clone https://github.com/Wobbleyaj1/CampusNav.git
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
- **Graph**: A weighted, directed graph was chosen because it provides a realistic representation of the campus map, and supports efficient shortest path calculations. This makes it the most appropriate choice for the project's requirements.
- **Tree**: An n-ary was chosen because it aligns with the hierarchical nature of campus locations, provides flexibility for updates, and supports efficient traversal for displaying data.
- **Stack**: Utilized for managing route history, allowing users to navigate backward and forward through previously traversed routes.
- **Queue**: Utilized for managing the walking guide, enabling step-by-step navigation through a route in a first in first out manner.
- **Array**: A fixed-size array was used to store frequent locations, providing fast access and efficient memory usage for managing a limited number of commonly visited locations.
- **Set**: A custom set implementation was used to ensure only unique locations are displayed in the "Frequent Locations" feature, preventing duplicates and maintaining a clean list of accessed locations.
- **List**: Used for maintaining an ordered collection of locations, as can be seen in the clicked locations tab.
- **Searching**: Uses binary search for quickly locating specific locations or features within sorted datasets, improving performance for large datasets.
- **Sorting**: Uses merge sort to organize data, such as sorting locations alphabetically, enhancing the user experience.

### Running Unit Tests
1. Navigate to the test directory:
   ```bash
   cd tests
   ```

2. Run `all_tests.py`:
   ```bash
   python all_tests.py
   ```

3. The terminal will output testing information. Look for the "OK" signaling that all tests passed.
   ```
   $ python all_tests.py
   ...............
   ----------------------------------------------------------------------
   Ran 15 tests in 0.000s

   OK
   ```

## Manual Test Plan for CampusNavigationApp Buttons

### 1. Search for a location
- Launch the application.
- Click the “Search for a location” button in the menu bar.
- Verify that a popup window appears with a combo box of location names.
- Select a valid location and click “Search.”
- Confirm that a red dot appears on the map at the location and an info card appears.
- Repeat with another location.
- Try selecting the same location again to verify it is not duplicated in the frequent locations list.

### 2. Find shortest route
- Click the “Find shortest route” button.
- Confirm that all other buttons become disabled and the prompt changes to “Select Starting Point.”
- Click on two different location markers on the map.
- Confirm that a line is drawn connecting the shortest path.
- Validate that the route is pushed to the route history.
- Ensure that buttons are re-enabled after completion.

### 3. Walking Guide
- Click the “Walking Guide” button.
- Follow any instructions or prompts to simulate walking guide functionality.
- Confirm guidance is provided on the map.
- Validate route animations.

### 4. View route history
- Click the “View route history” button.
- Confirm that a popup appears showing all previous routes taken.
- Validate that each route includes location names and distance.
- Check behavior when no routes are available.

### 5. View location tree
- Click the “View location tree” button.
- Confirm that a tree structure appears showing hierarchical relationships between locations.
- Expand/collapse nodes to verify interactive functionality.
- Check for expected node names and structure.

### 6. Searched Locations
- Click the “Searched Locations” button.
- Validate that a popup shows all locations searched during this session.
- Confirm no duplicates and a maximum of 10 recent locations.
- Add more than 10 locations and confirm that older entries are overwritten as expected.

### 7. Clicked Locations
- Click on several locations on the map manually.
- Click the “Clicked Locations” button.
- Confirm that each clicked location is listed in alphabetical order.

### 8. Exit
- Click the “Exit” button.
- Confirm that the application closes cleanly.
- Alternatively, click the window’s close (“X”) button and verify that the same exit logic executes.