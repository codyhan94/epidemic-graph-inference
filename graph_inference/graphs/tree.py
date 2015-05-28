from __future__ import print_function

from graph_inference.graphs.basegraph import BaseGraph

import random
import networkx as nx
import sys
# import matplotlib.pyplot as plt


class TreeGraph(BaseGraph):  # BaseGraph):
    """Generates a Tree"""

    def __init__(self):
        # super(TreeGraph, self).__init__()
        self.edge_weighted = False
        self.node_weighted = False
        self.graph_type = "Tree"
        self.directed = True

    def generate(self, n=1000, p=.2):
        self.G = nx.DiGraph()
        i = 0
        self.G.add_node(i)
        self.n = n
        self.p = p
        while i < n:
            for node in self.G.nodes():
                if random.random() < p:
                    i += 1
                    self.G.add_edge(node, i)
                    if i == n:
                        break

    def generate_powerlaw(self, n, gamma=3, create_using=nx.DiGraph):
        "Generates a random powerlaw tree using nx.random_powerlaw_tree"
        done = False
        tries = 1000
        while(tries < 10000000 and not done):
            try:
                self.G = nx.random_powerlaw_tree(n, gamma, tries=10000,
                                                 create_using=nx.DiGraph)
                self.G = nx.DiGraph(self.G)
                done = True
            except nx.NetworkXError:
                done = False
                tries *= 10
        if not done:
            print("Unable to generate such powerlaw tree. Try a smaller graph")
            print("Aborting")
            sys.exit(1)

    def description(self):
        """ Returns a description of the graph """
        retstr = "Tree with " + str(self.n) + " nodes and p = " + str(self.p)
        return retstr


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
