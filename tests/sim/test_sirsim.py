import unittest
import networkx as nx
import numpy as np

from graph_inference.solver.greedysolver import GreedySolver
from graph_inference.sim.sirsim import SIRSim


class TestSIRSim(unittest.TestCase):
    """
    Simple test cases for the functionality of the SIR simulation.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unreachable_nodes(self):
        """
        :return:
        """
        G = {
            0: 1

        }
