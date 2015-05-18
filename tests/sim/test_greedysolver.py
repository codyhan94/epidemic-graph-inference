from pdb import set_trace
import unittest
import numpy as np

from graph_inference.solver.greedysolver import GreedySolver


class TestGreedySolverMethods(unittest.TestCase):
    """
    Simple test cases for the functionality of the greedy algorithm.
    """

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
        Tests mutiple cascades on three nodes in a line graph.

        Graph:
            0 -> 1 -> 2
        """
        cascades = np.array([[0, 1, 2]])
        solver = GreedySolver(cascades)

        # Test that each node identifies its parental neighborhood correctly
        # when 0 is the seed node.
        self.assertEqual(solver.solve_node(0), [])
        self.assertEqual(solver.solve_node(1), [0])
        self.assertEqual(solver.solve_node(2), [1])

        # Test the same as above but with 2 as the seed node, changing the
        # direction of the above arrows.
        solver.cascades = np.array([[2, 1, 0]])
        self.assertEqual(solver.solve_node(0), [1])
        self.assertEqual(solver.solve_node(1), [2])
        self.assertEqual(solver.solve_node(2), [])

        # Test having the middle node as the seed.
        solver.cascades = np.array([[1, 0, 1]])
        self.assertEqual(solver.solve_node(0), [1])
        self.assertEqual(solver.solve_node(1), [])
        self.assertEqual(solver.solve_node(2), [1])

    def test_three_nodes_circle(self):
        """
        Tests multiple cascades on three nodes.

        Graph:
            0 _ 1
             \ /
              2
        """
        # Two cascades with 0 as the seed, one where all nodes get infected
        # and one where only node 1 gets infected. Similarly, two cascades
        # with 1 as a seed, one where all nodes get infected and one where
        # only 0 gets infected. Likewise for node 2, but with an imbalance.
        cascades = np.array(
            [[0, 1, 1], [0, 1, np.inf], [1, 0, 1], [1, 0, np.inf],
             [1, 1, 0], [np.inf, 0, 1]])
        solver = GreedySolver(cascades)

        self.assertEqual(solver.solve_node(0), [1])
        self.assertEqual(solver.solve_node(1), [0])
        self.assertEqual(solver.solve_node(2), [1])
