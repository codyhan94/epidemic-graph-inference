from __future__ import print_function
import sys
import os
sys.path.append(os.getcwd())

from graph_inference.graphs.basegraph import BaseGraph

import random
import networkx as nx
import sys


class DegreeDistributiongraph(BaseGraph):
    """Generates a graphml file from an edge list graph

    Note that the default is a directed graph.
    """

    def __init__(self):
        super(DegreeDistributiongraph, self).__init__()
        self.edge_weighted = False
        self.node_weighted = False
        self.graph_type = "DegreeSequence"
        self.directed = True

    def generate(self, degreelist, directed=False):
        self.directed = directed
        self.G = nx.configuration_model(degreelist)
        # remove parallel edges and self loops
        self.G = nx.Graph(self.G)
        self.G.remove_edges_from(self.G.selfloop_edges())

    def generatePareto(self, n=100, directed=False, exponent=1.0):
        dl = nx.utils.create_degree_sequence(n, nx.utils.pareto_sequence,
                                             max_tries=50, exponent=exponent)
        self.generate(dl, directed)
        self.graph_type = "Pareto"

    def generatePowerlaw(self, n=100, directed=False, exponent=2.0):
        dl = nx.utils.create_degree_sequence(n, nx.utils.powerlaw_sequence,
                                             max_tries=50, exponent=exponent)
        self.generate(dl, directed)
        self.graph_type = "Powerlaw"

if __name__ == "__main__":
    """ Example code """
    if len(sys.argv) is not 5:
        print("syntax: python distribution outfile [n] [distr] [exponent]",
              file=sys.stderr)
        sys.exit(-1)
    outfile = sys.argv[1]
    n = int(sys.argv[2])
    diststr = sys.argv[3]
    exponent = float(sys.argv[4])
    print(n, diststr, exponent)
    directed = True
    graph = DegreeDistributiongraph()
    if diststr in ["pareto", "Pareto"]:
        graph.generatePareto(n, False, exponent)
    else:
        graph.generatePowerlaw(n, False, exponent)

    graph.graphml(outfile)
    graph.draw()
