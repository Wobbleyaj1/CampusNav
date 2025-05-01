import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_structures.queue import Queue

class queue_tests(unittest.TestCase):
    def test_enqueue(self):
        q = Queue([])
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(str(q), '1 2 3')

    def test_dequeue(self):
        q = Queue([1, 2, 3])
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_peek(self):
        q = Queue([1, 2, 3])
        self.assertEqual(q.peek(), 1)
        self.assertEqual(q.peek(), 1)

    def test_len(self):
        q = Queue([1, 2, 3])
        self.assertEqual(len(q), 3)

    def test_contains(self):
        q = Queue([1, 2, 3])
        self.assertIn(1, q)
        self.assertNotIn(4, q)

    def test_clear(self):
        q = Queue([1, 2, 3])
        self.assertGreater(len(q), 0)
        q.clear()
        self.assertEqual(len(q), 0)

if __name__ == '__main__':
    unittest.main()