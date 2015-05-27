from __future__ import print_function

from graph_inference.graphs.basegraph import BaseGraph


import networkx as nx
import sys


class GNPgraph(BaseGraph):
    """Generates a GNP graph."""

    def __init__(self):
        super(GNPgraph, self).__init__()
        self.edge_weighted = False
        self.node_weighted = False
        self.graph_type = "GNP"
        self.directed = False

    def generate(self, n=1000, p=.5, directed=False):
        self.G = nx.fast_gnp_random_graph(n, p, None, directed)
        self.p = p
        self.n = n
        self.directed = directed

    def description(self):
        """ Returns a description of the graph """
        retstr = "GNP with " + str(self.n) + " nodes and p = " + str(self.p)
        return retstr

if __name__ == "__main__":
    """ Example code """
    if len(sys.argc) < 1:
        print("syntax: python gnp outfile", file=sys.stderr)
        sys.exit(-1)
    filename = sys.argv[1]
    graph = GNPgraph()
    graph.graphml(filename)
