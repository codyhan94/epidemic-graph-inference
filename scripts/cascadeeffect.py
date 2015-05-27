"""This is a general file used to test the basic functionality of our system"""
from __future__ import print_function
from pdb import set_trace

import networkx as nx
import matplotlib.pyplot as plt
import math

import sys
import os
from argparse import ArgumentParser

sys.path.append(os.getcwd())

# CONSTANTS
GENERATOR = "TREE"  # or "GNP"
graphfile = "data/testin.graphml"
inferredfile = "data/testout.graphml"


from graph_inference.graphs.gnp import BaseGraph
from graph_inference.graphs.gnp import GNPgraph
from graph_inference.graphs.tree import TreeGraph
from graph_inference.graphs.edgelist import EdgeListGraph
from graph_inference.sim.sirsim import SIRSim
from graph_inference.solver.greedysolver import GreedySolver
from graph_inference.analysis.baseanalysis import BaseAnalysis


def circlepos(G, r0=10):
    pos = {}
    d = max(G.degree().values())
    n = G.number_of_nodes()
    for node in G.nodes():
        deg = 2 * math.pi * int(node) / n
        r = r0 * (1 - float(G.degree(node)) / d) + 1
        pos[node] = (r * math.sin(deg), r * math.cos(deg))
    return pos


if __name__ == "__main__":
    # Generate Graph
    parser = ArgumentParser()
    # parser.add_argument('graph_type', help='TREE, GNP, or EDGEGRAPH')
    # parser.add_argument('-f', 'filename', help='Filename of file to load',
    #                     type=str, default=None)
    # parser.add_argument('-o', 'outfile', help='File to write to at end',
    #                     type=str, default=None)
    # parser.add_argument('-n', 'nodes', help='number of nodes',
    #                     type=num, default=50)
    args = parser.parse_args()
    n = 50
    args.graph_type = "TREE"

    if args.graph_type is "TREE":
        graph = TreeGraph()
        graph.generate(n)
    elif args.graph_type is "EDGEGRAPH":
        if not args.f:
            print('no file specified')
            sys.exit()
        else:
            try:
                graph = EdgeListGraph()
                graph.generate(args.f)
            except:
                print("fatal error. Aborting")  # not so good but im tired
                sys.exit()
    else:
        graph = GNPgraph()
        graph.generate(n=n, p=.01, directed=True)
    graph.graphml(graphfile)
    print(graphfile, "created")

    n_cascades = 20
    p_init = 0.05
    correctedges = []
    missingedges = []
    extraedges = []
    ndifference = []
    dsequence = []
    ddifference = []
    model = SIRSim(graphfile, n_cascades, p_init)
    for i in range(10):
        model.reset()
        model.n_cascades = n_cascades
        cascades = model.run()

        solver = GreedySolver(cascades)
        inferred = solver.solve_graph(out_file=inferredfile)

        analysis = BaseAnalysis(graphfile, inferredfile)
        correctedges.append(analysis.edgeCorrect())
        missingedges.append(analysis.edgeError())
        extraedges.append(analysis.edgeExtra())
        ndifference.append(analysis.edgeDifference())
        dsequence.append(analysis.degreeSequence())
        ddifference.append(analysis.nodeDegreeDifference())
        n_cascades += 20

    # Make plots, using the dot package to make trees look nice.
    print(correctedges)
    print(missingedges)
    print(extraedges)
    print(ndifference)
    print(dsequence)
    print(ddifference)

    # Make plots, using the dot package to make trees look nice.
    plt.figure(1)
    plt.title('Original Graph')
    # pos = nx.graphviz_layout(analysis.G, prog='dot')
    pos = circlepos(analysis.G)
    nx.draw(analysis.G, pos, with_labels=True)

    plt.figure(2)
    plt.title('Analyzed Graph')
    label = "{} cascades with p_init = {}.".format(n_cascades, p_init)
    plt.figtext(0.3, 0.1, label)
    # pos = nx.graphviz_layout(analysis.H, prog='dot')
    pos = circlepos(analysis.G)
    nx.draw(analysis.H, pos, with_labels=True)
    plt.show()
