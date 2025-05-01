import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_structures.stack import Stack

class TestStack(unittest.TestCase):
    def test_push(self):
        s = Stack([])
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(str(s), '1 2 3')

    def test_pop(self):
        s = Stack([1, 2, 3])
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_peek(self):
        s = Stack([1, 2, 3])
        self.assertEqual(s.peek(), 3)
        self.assertEqual(s.peek(), 3)

    def test_is_empty(self):
        s = Stack([])
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_len(self):
        s = Stack([1, 2, 3])
        self.assertEqual(len(s), 3)

    def test_contains(self):
        s = Stack([1, 2, 3])
        self.assertTrue(2 in s)
        self.assertFalse(4 in s)

    def test_clear(self):
        s = Stack([1, 2 ,3])
        self.assertGreater(len(s), 0)
        s.clear()
        self.assertEqual(len(s), 0)

if __name__ == '__main__':
    unittest.main()