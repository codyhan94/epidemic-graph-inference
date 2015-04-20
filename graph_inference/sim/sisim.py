from graph_inference.sim.basesim import BaseSim
from graph_inference.graphs import basegraph

import random

import numpy as np
import networkx as nx

class SISim(BaseSim):
    """Base class for network inference simulations."""

    def __init__(self, graph_file, n_cascades, mu=0.1):
        """Set up a
        """
        self.G = nx.read_graphml(graph_file)
        self.n_cascades = n_cascades
        self.mu = mu

        self.initialize_graph()
        pass

    def initialize_graph(self):
        """Set up the graph.."""
        return

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
