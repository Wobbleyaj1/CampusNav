#Tree data structure

class Tree:
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = []

    def add_edge(self, parent, child):
        """Add an edge between a parent and child node."""
        if parent not in self.nodes:
            self.add_node(parent)
        if child not in self.nodes:
            self.add_node(child)
        self.nodes[parent].append(child)

    def get_children(self, node):
        """Get the children of a given node."""
        return self.nodes.get(node, [])