class RouteHistory:
    def __init__(self):
        """Initialize an empty stack to store route history."""
        self.history = []

    def add_route(self, route):
        """Add a route to the history stack."""
        self.history.append(route)
        print(f"Route added to history: {route}")

    def get_history(self):
        """Retrieve the route history."""
        if not self.history:
            print("No routes in history.")
        return self.history

    def clear_history(self):
        """Clear the route history."""
        self.history.clear()
        print("Route history cleared.")