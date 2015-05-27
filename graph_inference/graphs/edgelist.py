from __future__ import print_function

from graph_inference.graphs.basegraph import BaseGraph


import networkx as nx
import sys


class EdgeListGraph(BaseGraph):
    """Generates a graphml file from an edge list graph

    Note that the default is a directed graph.
    """

    def __init__(self, *args):
        super(EdgeListGraph, self).__init__()
        self.edge_weighted = False
        self.node_weighted = False
        self.graph_type = "Imported"
        self.directed = True
        if len(args) == 1 and isinstance(args[0], str):
            self.generate(args[0])
        elif len(args) == 2 and isinstance(args[0], str):
            self.generate(args[0], args[1])

    def generate(self, filename, directed=True):
        f = open(filename, 'r')
        self.filename = filename
        self.directed = directed
        self.G = nx.DiGraph() if directed else nx.Graph()
        self.G = nx.read_edgelist(f, create_using=self.G)

    def MST(self, weight="weight"):
        self.G = nx.minimum_spanning_tree(self.G, weight)

    def description(self):
        """ Generates a description of the graph """
        return "Graph from " + self.filename

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

    graph = EdgeListGraph()
    graph.generate(infile, directed)
    graph.graphml(outfile)
