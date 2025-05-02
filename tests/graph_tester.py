import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_structures.graph import Graph

class graph_tests(unittest.TestCase):
    def test_graph(self):
        g = Graph()
        for i in range(6):
            g.add_node(i)
        g.add_edge(0, 1, 10)
        g.add_edge(1, 2, 10)
        g.add_edge(2, 3, 10)
        g.add_edge(0, 4, 10)
        g.add_edge(4, 3, 15)
        g.add_edge(0, 5, 10)
        g.add_edge(5, 3, 10)

        path, dis = g.find_shortest_path(0, 3)
        self.assertEqual(path, [0, 5, 3])
        self.assertEqual(dis, 20)

        g.remove_node(5)
        path, dis = g.find_shortest_path(0, 3)
        self.assertEqual(path, [0, 4, 3])
        self.assertEqual(dis, 25)

        g.remove_edge(4, 3)
        path, dis = g.find_shortest_path(0, 3)
        self.assertEqual(path, [0, 1, 2, 3])
        self.assertEqual(dis, 30)
        self.assertEqual(g.get_edge_weight(0, 4), 10)
        

if __name__ == '__main__':
    unittest.main()