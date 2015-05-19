"""This is a general file used to test the basic functionality of our system"""
from __future__ import print_function
from pdb import set_trace

import networkx as nx
import matplotlib.pyplot as plt
import math

import sys, os
sys.path.append(os.getcwd())

# CONSTANTS
GENERATOR = "TREE"  # or "GNP"
graphfile = "data/testin.graphml"
inferredfile = "data/testout.graphml"

from graph_inference.graphs.gnp import GNPgraph
from graph_inference.graphs.tree import TreeGraph
from graph_inference.sim.sirsim import SIRSim
# dummy code below while Cody pushes his code
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
    if GENERATOR is "TREE":
        graph = TreeGraph()
        graph.generate(15, .2)
    else:
        graph = GNPgraph()
        graph.generate(n=50, p=.01, directed=True)
    graph.graphml(graphfile)
    print(graphfile, "created")

    model = SIRSim(graphfile, n_cascades=20000, p_init=0.05)
    cascades = model.run()
    print()
    print("Done simulating! Now solving...")

    solver = GreedySolver(cascades)
    set_trace()
    solver.solve_graph(out_file=inferredfile)
    print()
    print("Solved graph saved to", inferredfile)

    print()
    print("Starting analysis...")
    analysis = BaseAnalysis(graphfile, inferredfile)
    print("correct edges", analysis.edgeCorrect())
    print("missing edges:", analysis.edgeError())
    print("extra edges:", analysis.edgeExtra())
    print("edge number:", analysis.edgeDifference())
    print("degree sequence", analysis.degreeSequence())
    print("degree difference", analysis.nodeDegreeDifference())

    # Make plots, using the dot package to make trees look nice.
    plt.figure(1)
    plt.title('original graph')
    pos = nx.graphviz_layout(analysis.G, prog='dot')
    # nx.draw(analysis.G, circlepos(analysis.G))
    nx.draw(analysis.G, pos, with_labels=True)
    plt.figure(2)
    plt.title('analyzed graph')
    pos = nx.graphviz_layout(analysis.H, prog='dot')
    # nx.draw(analysis.H, circlepos(analysis.G))
    nx.draw(analysis.H, pos, with_labels=True)
    plt.show()
