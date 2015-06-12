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

import numpy as np


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
    parser.add_argument('graph_type', help='TREE, GNP, or EDGEGRAPH')
    parser.add_argument('-f', '--filename', help='Filename of file to load',
                        type=str, default=None)
    parser.add_argument('-o', '--outfile', help='File to write to at end',
                        type=str, default=None)
    parser.add_argument('-n', '--nodes', help='number of nodes',
                        type=int, default=50)
    args = parser.parse_args()

    n = args.nodes

    graph = None

    if args.graph_type == "TREE":
        graph = TreeGraph()
        graph.generate(n)
    elif args.graph_type == "EDGEGRAPH":
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

    min_cascades = 50
    stride = 50
    max_cascades = 1000
    p_init = 0.05

    n_cascade_lst = np.arange(min_cascades, max_cascades, stride)

    correctedges = []
    missingedges = []
    extraedges = []
    ndifference = []
    dsequence = []
    ddifference = []
    model = SIRSim(graphfile, min_cascades, p_init)
    analysis = BaseAnalysis(graphfile, None)
    for n_cascades in n_cascade_lst:
        model.n_cascades = n_cascades
        print("Starting simulation with ", n_cascades, " cascades")
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []

        for j in range(10):
            cascades = model.run()

            solver = GreedySolver(cascades)
            inferred = solver.solve_graph()

            a.append(analysis.edgeCorrect(H=inferred))
            b.append(analysis.edgeError(H=inferred))
            c.append(analysis.edgeExtra(H=inferred))
            d.append(analysis.edgeDifference(H=inferred))
            e.append(analysis.degreeSequence(H=inferred))
            f.append(analysis.nodeDegreeDifference(H=inferred))

        correctedges.append(float(np.mean(a)))
        missingedges.append(float(np.mean(b)))
        extraedges.append(float(np.mean(c)))
        ndifference.append(float(np.mean(d)))
        dsequence.append(np.mean(e))
        ddifference.append(np.mean(f))
        n_cascades += stride

    # Make plots, using the dot package to make trees look nice.
    print("Number of Correct Edges: ", correctedges)
    print("Number of Incorrect Edges: ", missingedges)
    print("Extraneous edges: ", extraedges)
    print("Difference in edge number: ", ndifference)
    print("Degree Sequence: ", dsequence)
    print("Degree difference: ", ddifference)

    # Make plots, using the dot package to make trees look nice.
    plotit = True
    if plotit:
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
        nx.draw(inferred, pos, with_labels=True)

        correct_ratios = np.array(correctedges) / graph.n

        plt.figure(3)
        plt.title('Percentage of original edges inferred versus number of '
                  'cascades')
        plt.plot(n_cascade_lst, correct_ratios, ls='-', marker='o')
        plt.title("Cascades needed for successful graph recovery (trees)")
        plt.xlabel("Number of cascades")
        plt.ylabel("Percentage of edges recovered")
        plt.savefig("tree-recovery-percentages.pdf")
        plt.show()
