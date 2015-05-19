from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt
import math


class BaseAnalysis(object):

    """Base class for analysis"""
    G = None
    H = None

    def __init__(self, graphfile, inferredfile):
        self.G = nx.readwrite.graphml.read_graphml(graphfile, node_type=int)
        self.H = nx.readwrite.graphml.read_graphml(inferredfile, node_type=int)

    def edgeCorrect(self, G=None, H=None):
        """
        Returns the number of edges in the original graph that are
        correctly predicted

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
            if gedge in hedges:
                count += 1
        return count

    def edgeError(self, G=None, H=None):
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
                count += 1
        return count

    def edgeExtra(self, G=None, H=None):
        """
        Returns the number of extraneous edges the inferred graph has.

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: int
        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H

        return self.edgeError(H, G)

    def edgeDifference(self, G=None, H=None):
        """ Returns the difference in number of edges between the two graphs.

        :param G: networkx graph of original graph (default: self.G)
        :param H: networkx graph of inferred graph (default: self.H)
        :return: int
        """
        if G is None:
            G = self.G
        if H is None:
            H = self.H
        return G.number_of_edges() - H.number_of_edges()

    def neighborMatching(self, G=None, H=None):
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

    def degreeSequence(self, G=None, H=None):
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

        gdegree = sorted(nx.degree(G).values(), reverse=True)
        hdegree = sorted(nx.degree(H).values(), reverse=True)

        degreelist = [self.__degreeSequenceHelper(x, y) for x, y
                      in zip(gdegree, hdegree)]

        return sum(degreelist) / len(degreelist)

    def nodeDegreeDifference(self, G=None, H=None):
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

        gdegree = nx.degree(G).values()
        hdegree = nx.degree(H).values()
        degreelist = [self.__degreeSequenceHelper(x, y) for x, y
                      in zip(gdegree, hdegree)]

        return sum(degreelist) / len(degreelist)

    def __degreeSequenceHelper(self, i, j):
        """ Helper function for degree sequence """
        if i is None or i == 0:
            return float(j)
        elif j is None or j == 0:
            return float(i)
        else:
            return float(abs(i - j)) / i

    # Plotting functions!
    def plotGraphs(self, G, H):
        if G is None:
            G = self.G
        if H is None:
            H = self.H

        plt.figure()
        plt.title('original graph')
        nx.draw(G, self.__circlepos(G))
        plt.figure()
        plt.title('analyzed graph, with %d' % 5)
        nx.draw(H, self.__circlepos(H))

    # def plothistogram:
    #     """ Sourced from https://networkx.github.io/documentation/latest/
    #     examples/drawing/degree_histogram.html"""

    #     degree_sequence=sorted(nx.degree(G).values(),
    #                            reverse=True)  # degree sequence
    #     #print "Degree sequence", degree_sequence
    #     dmax=max(degree_sequence)

    #     plt.loglog(degree_sequence,'b-',marker='o')
    #     plt.title("Degree rank plot")
    #     plt.ylabel("degree")
    #     plt.xlabel("rank")

    #     # draw graph in inset
    #     plt.axes([0.45,0.45,0.45,0.45])
    #     Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
    #     pos=nx.spring_layout(Gcc)
    #     plt.axis('off')
    #     nx.draw_networkx_nodes(Gcc,pos,node_size=20)
    #     nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

    def __circlePos(self, G, r0=10):
        pos = {}
        d = max(G.degree().values())
        n = G.number_of_nodes()
        for node in G.nodes():
            deg = 2 * math.pi * int(node) / n
            r = r0 * (1 - G.degree(node) / d) + .5
            pos[node] = (r * math.sin(deg), r * math.cos(deg))
        return pos
