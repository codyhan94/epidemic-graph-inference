from __future__ import print_function

import networkx as nx

class BaseAnalysis(object):
    """Base class for analysis"""
    G = None
    H = None
    def ___init___(self, graphfile, inferredfile):
        self.G = nx.read_graphml(graphfile)
        self.H = nx.read_graphml(inferredfile)

    def edgeerror(self, G=None, H=None):
        """
        Returns the number of edges in the original graph that aren't in the inferred graph.

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: int
        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H
        gedges = G.edges()
        hedges = H.edges()
        count = 0
        for gedge in gedges:
            if gedge not in hedges:
                count += 0
        return count

    def edgeextra(self, G=None, H=None):
        """
        Returns the number of extraneous edges the inferred graph has.
        
        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: int
        """
        return self.edgeerror(H,G)

    def edgedifference(self, G=None, H=None):
        """ Returns the difference in number of edges between the two graphs.

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: int
        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H
        return G.number_of_nodes() - H.number_of_nodes()

