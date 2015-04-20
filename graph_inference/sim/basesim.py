from __future__ import print_function

from abc import ABCMeta, abstractmethod

import sys

import numpy as np

class BaseSim(object):
    """Base class for network inference simulations."""

    __metaclass__ = ABCMeta

    def __init__(self, graph, n_cascades):
        self.G = self.load_graph(graph)
        self.n_cascades = n_cascades
        pass

    def dprint(self, *args):
        if self.DEBUG:
            print('DEBUG: ', *args, file=sys.stderr)

    @abstractmethod
    def load_graph(self, graph):
        """Loads the specified graph file. """
        return

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
