# 📍 Campus Navigation & Route Planner

A Python-based navigation system that helps users find the shortest and most efficient routes around a college campus. It uses fundamental data structures and algorithms including graphs, trees, stacks, queues, lists, and more — making it both a practical tool and an educational showcase.

---

## 📖 Project Overview

This system models the campus layout as a graph where:
- **Nodes** represent campus locations (buildings, landmarks, facilities)
- **Edges** represent pathways or roads between those locations

Users can:
- Look up details about campus locations
- Find the shortest route between two places
- View information like distance
- Look at past routes
- Follow along while walking campus

---

## 🗂️ Project Structure

```
CampusNav/
├── assets/
│   ├── mercer_map.png
├── data/
│   ├── campus_map.json         # Graph structure of the campus
│   ├── location_features.json  # Metadata for each campus location
├── src/
│   ├── data_structures/
│       ├── array.py
│       ├── graph.py
│       ├── list.py
│       ├── queue.py
│       ├── searching_sorting.py
│       ├── set.py
│       ├── stack.py
│       ├── tree.py
│   ├── location_manager.py
│   ├── utils.py                # Helper functions (searching, sorting, etc.)
│   ├── main.py                 # Main app logic
├── tests/
│   ├── all_tests.py
│   ├── graph_tester.py
│   ├── queue_tester.py
│   ├── stack_tester.py
│   └── tree_tester.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── user.md
```

---

## 📌 Features

- 📌 Store and manage campus locations and connections using a graph
- 🔍 Find the shortest routes between two locations on campus
- 🗺️ View details about campus buildings, landmarks, and services
- 📦 Uses:
  - Graphs (Unit 12)
  - Sets & Dictionaries (Unit 11)
  - Trees (Unit 10)
  - Lists (Unit 9)
  - Queues (Unit 8)
  - Stacks (Unit 7)
  - Arrays and Linked Structures (Unit 4)
  - Searching, Sorting (Unit 3)
  - Collections (Unit 2)

---

## 🚀 MVP (Minimum Viable Product)

- Load campus locations and connections from `campus_map.json`
- Display location details from `locations.json`
- Implement shortest path finding using Dijkstra’s algorithm
- Provide GUI for:
  - Displaying campus location names
  - Finding a route between two locations
  - Viewing details for a given location

---

## 📚 Technologies

- **Python 3.11+**
- JSON for data storage
- Command-line interface (CLI)

---

## 🛠️ Setup Instructions

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
1. Navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Run the main application:
   ```bash
   python main.py
   ```

3. The application will launch a graphical user interface (GUI) displaying the campus map.

---

## 🧪 Running Unit Tests

1. Navigate to the `tests` directory:
   ```bash
   cd tests
   ```

2. Run all tests:
   ```bash
   python all_tests.py
   ```

3. The terminal will output testing information. Look for the "OK" signaling that all tests passed:
   ```
   $ python all_tests.py
   ...............
   ----------------------------------------------------------------------
   Ran 15 tests in 0.000s

   OK
   ```

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
