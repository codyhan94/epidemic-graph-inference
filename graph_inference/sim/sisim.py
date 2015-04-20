from graph_inference.sim.basesim import BaseSim
from graph_inference.graphs import basegraph

import numpy as np
import networkx as nx

class SISim(BaseSim):
    """Base class for network inference simulations."""

    def __init__(self, graph, n_cascades):
        """Set up a
        """
        self.graph = graph
        self.n_cascades = n_cascades
        pass

    def step(self):
        """Runs one step of the simulation.

        :return: Nothing
        """
        return

    def run(self):
        """Runs the simulation and returns the output (vector of times)

        :return: numpy array
        """
        return
