from __future__ import print_function

from graph_inference.graphs.basegraph import BaseGraph


import networkx as nx
import sys

class GNPgraph(BaseGraph):
    """Generates a GNP graph."""

    def __init__(self, arg):
        super(GNPgraph, self).__init__()
        self.arg = arg

    def generate(self, n=1000, p=.5, directed=False):
        self.G = nx.fast_gnp_random_graph(n, p, None, directed)

if __name__ == "__main__":
    """ Example code """
    if len(sys.argc) < 1:
        print("syntax: python gnp outfile", file=sys.stderr)
        sys.exit(-1)
    filename = sys.argv[1]
    graph = GNPgraph()
    graph.graphml(filename)

