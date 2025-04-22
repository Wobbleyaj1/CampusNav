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
        return string
    
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
        self.list[len(self.list)-1]

if __name__ == "__main__":
    q = Queue()
    for i in range(5):
        q.enqueue(i)
    print(f'Size: {len(q)}')
    print(f'Front Value: {q.peek()}')
    print(f'Queue: {q}')
    print(f'Contains 3: {3 in q}')
    for i in range(3):
        print(f'Dequeues: {q.dequeue()}')
    print(f'Queue: {q}')
    q.clear()
    print(f'Emptied Queue.')
    print(f'Queue: {q}')
