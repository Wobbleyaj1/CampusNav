# Stacks module

class Stack:
    def __init__(self, source: list = []):
        """Initialize the stack."""
        self.list = source

    def push(self, item):
        """Add an item to the top of the stack."""
        self.list.append(item)

    def pop(self):
        """Remove and return the item at the top of the stack."""
        if len(self.list) == 0:
            raise IndexError("Stack is empty.")
        return self.list.pop()

    def peek(self):
        """Return the item at the top of the stack without removing it."""
        return self.list[len(self.list)-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self.list) == 0

    def __len__(self):
        """Return the number of items in the stack."""
        return len(self.list)

    def __str__(self):
        """Display the stack."""
        string = ''
        for i in self.list:
            string += i + ' '
        return str(string)
    
if __name__ == "__main__":
    s = Stack()
    for i in range(5):
        s.push(str(i))
    print(f"Size: {len(s)}")
    print(f"Top Value: {s.peek()}")
    print(f"Stack: {s}")
    while (not s.is_empty()):
        print(f"pop: {s.pop()}")
    print("Stack is empty")