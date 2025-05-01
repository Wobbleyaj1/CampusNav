# Set module

class Set:
    def __init__(self):
        """Initialize the set."""
        self.items = []

    def add(self, item):
        """Add an item to the set."""
        if item not in self.items:
            self.items.append(item)

    def remove(self, item):
        """Remove an item from the set."""
        if item in self.items:
            self.items.remove(item)

    def contains(self, item):
        """Check if the set contains an item."""
        return item in self.items

    def __iter__(self):
        """Make the set iterable."""
        return iter(self.items)

    def union(self, other_set):
        """Return the union of this set and another set."""
        result = Set()
        result.items = self.items[:]
        for item in other_set.items:
            if item not in result.items:
                result.items.append(item)
        return result

    def intersection(self, other_set):
        """Return the intersection of this set and another set."""
        result = Set()
        for item in self.items:
            if item in other_set.items:
                result.add(item)
        return result

    def difference(self, other_set):
        """Return the difference of this set and another set."""
        result = Set()
        for item in self.items:
            if item not in other_set.items:
                result.add(item)
        return result

    def size(self):
        """Return the number of items in the set."""
        return len(self.items)

    def display(self):
        """Display the set."""
        print(f"Set: {self.items}")