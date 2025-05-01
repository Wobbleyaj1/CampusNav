import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_structures.tree import Tree

class tree_tests(unittest.TestCase):
    def test_tree(self):
        t = Tree()
        for i in range(7):
            t.add_node(i)
        t.add_edge(0, 1)
        t.add_edge(0, 2)
        t.add_edge(1, 3)
        t.add_edge(1, 4)
        t.add_edge(2, 5)
        t.add_edge(2, 6)

        self.assertTrue(t.get_children(0), [1, 2])
        self.assertTrue(t.get_children(1), [3, 4])
        self.assertTrue(t.get_children(2), [5, 6])


if __name__ == '__main__':
    unittest.main()