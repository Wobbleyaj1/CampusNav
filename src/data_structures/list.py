# List module

class List:
    def __init__(self):
        """Initialize the list."""
        self.items = []

    def add(self, item):
        """Add an item to the list."""
        self.items.append(item)

    def remove(self, item):
        """Remove an item from the list."""
        if item in self.items:
            self.items.remove(item)

    def get(self, index):
        """Retrieve an item by its index."""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def contains(self, item):
        """Check if the list contains an item."""
        return item in self.items

    def size(self):
        """Return the number of items in the list."""
        return len(self.items)

    def display(self):
        """Display the list."""
        print(f"List: {self.items}")