from __future__ import print_function

from graph_inference.graphs.basegraph import BaseGraph

import random
import networkx as nx
# import sys
# import matplotlib.pyplot as plt


class TreeGraph(BaseGraph):  # BaseGraph):
    """Generates a GNP graph."""

    def __init__(self):
        # super(TreeGraph, self).__init__()
        self.edge_weighted = False
        self.node_weighted = False
        self.graph_type = "Tree"
        self.directed = False

    def generate(self, n=1000, p=.2):
        self.G = nx.DiGraph()
        i = 0
        self.G.add_node(i)

        while i < n:
            for node in self.G.nodes():
                if random.randint(0, 1):
                    i += 1
                    self.G.add_edge(node, i)
                    if i == n:
                        break


# if __name__ == "__main__":
#     """ Example code """
#     # if len(sys.argv) < 1:
#     #   print("syntax: python tree outfile", file=sys.stderr)
#     #   sys.exit(-1)
#     # filename = sys.argv[1]
#     graph = TreeGraph()
#     graph.generate(100)
#     pos = nx.graphviz_layout(graph.G,prog="dot")
#     nx.draw(graph.G, pos, with_labels=False, arrows=False)
#     plt.show()
#     # graph.graphml(filename)
