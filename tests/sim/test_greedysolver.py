import unittest
import numpy as np

from graph_inference.solver.greedysolver import GreedySolver

class TestGreedySolverMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_two_nodes_one_cascade(self):
        """
        Tests that the greedy solver predicts correctly given two nodes,
        one infecting the other. Should produce one directed edge A -> B.

        Graph:
            0 -> 1
        """
        cascades = np.array([[0, 1]])
        solver = GreedySolver(cascades)

        # The right node should have a parental neighborhood containing the
        # left node.
        self.assertEqual(solver.solve_node(0), [])
        self.assertEqual(solver.solve_node(1), [0])

        # Test the other direction (right is the seed this time)
        cascades = np.array([[1, 0]])
        solver.cascades = cascades

        self.assertEqual(solver.solve_node(0), [1])
        self.assertEqual(solver.solve_node(1), [])

    def test_three_nodes_line(self):
        """
        Tests one cascade on three nodes in a line graph.

        Graph:
            0 -> 1 -> 2
        """
        cascades = np.array([])
        pass
