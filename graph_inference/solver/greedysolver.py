from graph_inference.solver.basesolver import BaseSolver

import numpy as np


class GreedySolver(BaseSolver):
    """A simple greedy algorithm for determining parental neighborhoods.

    The algorithm comes from Netrapalli's paper.
    """

    def __init__(self, cascades):
        """
        Sets up an instance of the greedy solver with a list of cascades.

        :param cascades: numpy array of cascades
        :return: None
        """
        super(GreedySolver, self).__init__(cascades)

    def solve_node(self, node):
        """
        Computes the parental neighborhood for a particular node.

        :param node: integer index of node
        :return: numpy array of indices corresponding to nodes
        """
        return np.ndarray(node)
