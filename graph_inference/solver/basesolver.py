from __future__ import print_function

from abc import ABCMeta, abstractmethod

import sys


class BaseSolver(object):
    """Base solver class.

    Takes takes as input the output of simulations and produces parental
    neighborhoods as output.
    """

    __metaclass__ = ABCMeta

    def __init__(self, cascades):
        self.cascades = cascades

    def dprint(self, *args):
        if self.DEBUG:
            print('DEBUG: ', *args, file=sys.stderr)

    @abstractmethod
    def solve_node(self, node):
        """Solves for the parental neighborhood of a particular node."""
        raise NotImplementedError

    # @abstractmethod
    # def step(self):
    #     """Runs one step of the simulation.

    #     :return: Nothing
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # def run(self):
    #     """Runs the simulation and returns the output (vector of times)

    #     :return: numpy array
    #     """
    #     raise NotImplementedError
