# Arrays and Linked Structures module

class Array:
    def __init__(self, size, default_value=None):
        """Initialize an array with a fixed size and default values."""
        self.size = size
        self.data = [default_value] * size

    def set(self, index, value):
        """Set the value at a specific index."""
        if 0 <= index < self.size:
            self.data[index] = value
        else:
            raise IndexError("Index out of bounds")

    def get(self, index):
        """Get the value at a specific index."""
        if 0 <= index < self.size:
            return self.data[index]
        else:
            raise IndexError("Index out of bounds")

    def display(self):
        """Display the array."""
        print(self.data)


class LinkedStructures:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        """Initialize the linked structure."""
        self.head = None

    def add_node(self, value):
        """Add a node to the linked structure."""
        new_node = self.Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove_node(self, value):
        """Remove a node from the linked structure."""
        current = self.head
        prev = None
        while current:
            if current.value == value:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def find_node(self, value):
        """Find a node in the linked structure."""
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def display(self):
        """Display the linked structure."""
        current = self.head
        values = []
        while current:
            values.append(current.value)
            current = current.next
        print(" -> ".join(map(str, values)))