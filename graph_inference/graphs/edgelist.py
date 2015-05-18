from __future__ import print_function

from graph_inference.graphs.basegraph import BaseGraph


import networkx as nx
import sys


class EdgeListgraph(BaseGraph):
    """Generates a graphml file from an edge list graph

    Note that the default is a directed graph.
    """

    def __init__(self):
        super(EdgeListgraph, self).__init__()
        self.edge_weighted = False
        self.node_weighted = False
        self.graph_type = "Imported"
        self.directed = True

    def generate(self, filename, directed=True):
        f = open(filename, 'r')
        self.directed = directed
        self.G = nx.DiGraph() if directed else nx.Graph()
        self.G = nx.read_edgelist(f, create_using=self.G)

if __name__ == "__main__":
    """ Example code """
    if len(sys.argv) < 3 or len(sys.argv > 4):
        print("syntax: python edgelist infile outfile [directed = 1]",
              file=sys.stderr)
        sys.exit(-1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    directed = True
    if len(sys.argv) == 4:
        if sys.argv[3] in ["False", "F", "0", "f", "undirected", "Undirected"]:
            directed = False

    graph = EdgeListgraph()
    graph.generate(infile, directed)
    graph.graphml(outfile)
