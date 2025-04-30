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
├── data/
│   ├── campus_map.json         # Graph structure of the campus
│   ├── location_features.json  # Metadata for each campus location
├── src/
│   ├── __init__.py
|   ├── route_history.py
│   ├── location_manager.py
│   ├── utils.py                # Helper functions (searching, sorting, etc.)
│   ├── main.py                 # Main app logic
├── tests/
│   ├── test_graph.py
│   └── test_nav.py
├── README.md
└── requirements.txt
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
- Provide interaction for:
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

1. Clone the repo:
   ```bash
   git clone https://github.com/Wobbleyaj1/CampusNav.git
   cd CampusNav
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python src/campus_nav.py
   ```

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
