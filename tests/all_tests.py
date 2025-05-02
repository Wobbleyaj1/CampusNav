import unittest
from graph_tester import graph_tests
from queue_tester import queue_tests
from stack_tester import stack_tests
from tree_tester import tree_tests

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(graph_tests))
    suite.addTest(loader.loadTestsFromTestCase(queue_tests))
    suite.addTest(loader.loadTestsFromTestCase(stack_tests))
    suite.addTest(loader.loadTestsFromTestCase(tree_tests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())