from graph_inference.graphs.basegraph import BaseGraph

import networkx as nx

class GNPgraph(BaseGraph):
    """Generates a GNP graph."""

    def __init__(self, arg):
        super(GNPgraph, self).__init__()
        self.arg = arg

    def generate(self, n=1000, p=.5, directed=False):
        self.G = nx.fast_gnp_random_graph(n, p, None, directed)
