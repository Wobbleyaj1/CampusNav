# Queue module

class Queue:
    def __init__(self, source: list = []):
        """Initialize the queue."""
        self.list = source

    def isEmpty(self) -> bool:
        """Checks if the queue is empty."""
        return not any(self.list)
    
    def __len__(self):
        """Gets the number of items in the queue."""
        return len(self.list)
    
    def __str__(self):
        """Returns the queue as a string."""
        string = ''
        for i in self.list:
            string += str(i) + ' '
        return string[:-1]
    
    def __contains__(self, item):
        """Checks if an item is in the queue."""
        return item in self.list
    
    def enqueue(self, item):
        """Adds an item to the end of the queue."""
        self.list.append(item)

    def dequeue(self):
        """Removes and returns the item in the front of the queue."""
        if not any(self.list):
            raise IndexError("Stack is Empty.")
        return self.list.pop(0)
    
    def clear(self):
        """Empties the queue."""
        self.list = []
    
    def peek(self):
        """Returns the item in the front of the queue without removing it."""
        if not any(self.list):
            raise IndexError("Stack is Empty.")
        return self.list[0]
