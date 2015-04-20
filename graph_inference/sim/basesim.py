from graph_inference.graphs import basegraph
from abc import ABCMeta, abstractmethod

import numpy as np

class BaseSim(object):
    """Base class for network inference simulations."""

    __metaclass__ = ABCMeta

    def __init__(self, graph, n_cascades):
        self.graph = graph
        self.n_cascades = n_cascades
        pass

    @abstractmethod
    def step(self):
        """Runs one step of the simulation.

        :return: Nothing
        """
        return

    @abstractmethod
    def run(self):
        """Runs the simulation and returns the output (vector of times)

        :return: numpy array
        """
        return
