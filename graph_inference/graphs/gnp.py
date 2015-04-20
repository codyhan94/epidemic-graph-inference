from graph_inference.graphs.basegraph import BaseGraph

import networkx as nx
import sys

class GNPgraph(BaseGraph):
    """Generates a GNP graph."""

    def __init__(self, arg):
        super(GNPgraph, self).__init__()
        self.arg = arg
        self.generate()

    def generate(self, n=1000, p=.5, directed=False):
        self.G = nx.fast_gnp_random_graph(n, p, None, directed)

if __name__ == "__main__":
    """ Example code """
    filename = sys.argv[1]
    graph = GNPgraph()
    graph.graphml(filename)

