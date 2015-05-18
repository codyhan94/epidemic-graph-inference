from graph_inference.solver.basesolver import BaseSolver

from collections import Counter

import numpy as np
import networkx as nx


class MLESolver(BaseSolver):
    """A MLE solver that solves a per-node convex optimization problem to
    determine each node's parental neighborhood.

    The algorithm comes from Netrapalli's paper.
    """

    def __init__(self, cascades):
        """
        Sets up an instance of the greedy solver with a list of cascades.

        :param cascades: numpy array of cascades
        :return: None
        """
