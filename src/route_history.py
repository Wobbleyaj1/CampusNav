from data_structures.stack import Stack

class RouteHistory:
    def __init__(self):
        """Initialize a stack to store route history."""
        self.history = Stack()

    def add_route(self, route):
        """Add a route to the history stack."""
        self.history.push(route)

    def get_history(self):
        """Retrieve the route history as a list."""
        return self.history.list

    def clear_history(self):
        """Clear the route history."""
        self.history.clear()
        print("Route history cleared.")