from __future__ import print_function

import networkx as nx


class BaseAnalysis(object):

    """Base class for analysis"""
    G = None
    H = None

    def ___init___(self, graphfile, inferredfile):
        self.G = nx.readwrite.graphml.read_graphml(graphfile)
        self.H = nx.readwrite.graphml.read_graphml(inferredfile)

    def edgeerror(self, G=None, H=None):
        """
        Returns the number of edges in the original graph that aren't
        in the inferred graph.

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
        return self.edgeerror(H, G)

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

    def neighbormatching(self, G=None, H=None):
        """ Returns the graph similarity based on Neighbor Matching[Ref]
        Derived from 'wadsashika'_

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: fractional float (from 0 to 1)
        .. [Ref] Measuring Similarity of Graph Nodes by Neighbor Matching, Faculty of Mathematics, University of Belgrade
        .. _wadsashika: https://wadsashika.wordpress.com/2014/09/19/measuring-graph-similarity-using-neighbor-matching/

        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H

        if not G.is_directed():
            print("G is not a directed graph! Converting to directed graph")
            G = G.to_directed()
        if not H.is_directed():
            print("H is not a directed graph! Converting to directed graph")
            H = H.to_directed()

        gnodes = G.nodes()
        hnodes = H.nodes()

        # TODO

    def degreesequence(self, G=None, H=None):
        """ Returns how similar two graphs are by comparing their degree sequence.
        The sum of scaled things
        of ratio of

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: fractional float (from 0 to 1)
        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H

        gdegree = nx.degree(G).sort(reversed=True)
        hdegree = nx.degree(H).sort(reversed=True)
        degreelist = map(self.__degreesequencehelper, gdegree, hdegree)

        return sum(degreelist) / len(degreelist)

    def nodedegreedifference(self, G=None, H=None):
        """ Returns how similar two graphs are by comparing the degree of each
        corresponding node

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: fractional float (from 0 to 1)
        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H

        gdegree = nx.degree(G)
        hdegree = nx.degree(H)
        degreelist = map(self.__degreesequencehelper, gdegree, hdegree)

        return sum(degreelist) / len(degreelist)

    def __degreesequencehelper(self, i, j):
        """ Helper function for degree sequence """
        if i is None:
            return float(j)
        elif j is None:
            return float(i)
        else:
            return float(abs(i - j)) / i
