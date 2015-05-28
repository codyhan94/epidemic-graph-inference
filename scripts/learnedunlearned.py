"""This is a general file used to test the basic functionality of our system"""
from __future__ import print_function
from pdb import set_trace

import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

import sys
import os

sys.path.append(os.getcwd())

# CONSTANTS
graphfile = "data/gnp.graphml"
inferredfile = "data/testout.graphml"


from graph_inference.graphs.gnp import BaseGraph
from graph_inference.graphs.gnp import GNPGraph
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
    n = 50
    graph = GNPGraph()
    graph.generate(n, 1.5/n)
    graph.graphml(graphfile)
    print(graphfile, "created")
    G = graph.G

    n_cascades = 500
    p_init = 0.05
    model = SIRSim(G, n_cascades, p_init)
    print("Starting simulation with ", n_cascades, " cascades")
    cascades = model.run()

    # G = nx.convert_node_labels_to_integers(G)
    edgelist = G.edges()
    solver = GreedySolver(cascades)
    inferred = solver.solve_graph()
    newedges = inferred.edges()

    print(sorted(edgelist))
    print(sorted(newedges))

    # Make plots, using the dot package to make trees look nice.

    fig = plt.figure(1)
    pos = nx.graphviz_layout(G, prog='neato')
    # pos = nx.graphviz_layout(G, prog='twopi')
    # pos = nx.graphviz_layout(analysis.G, prog='dot')
    old_edges = set(G.edges())
    new_edges = set(inferred.edges())
    notin = list(new_edges.difference(old_edges))
    inboth = list(old_edges.intersection(new_edges))

    dnode = nx.draw_networkx_nodes(G, pos, node_size=300,
                                   node_color='#FF6E1E')
    oedge = nx.draw_networkx_edges(G, pos, edge_color='#616265', width=6,
                                   arrows=False)
    nedge = nx.draw_networkx_edges(inferred, pos, edge_color='k', width=6,
                                   arrows=False, edgelist=notin)

    xedge = nx.draw_networkx_edges(inferred, pos, edgelist=inboth,
                                   edge_color='#FF6E1E', width=6, arrows=False)

    plt.title("Edge Prediction on a " + repr(graph) + " Using SIR with " +
              str(n_cascades) + " cascades")
    plt.axis('off')
    plt.legend((oedge, xedge, nedge),
               ('Original Edges',
                'Correctly Predicted Edges',
                'Incorrectly Predicted Edges'),
               loc=4)
    # plt.figure(2)
    # dnode = nx.draw_networkx_nodes(G, pos, node_size=300,
    #                                node_color='#FF6E1E')
    # oedge = nx.draw_networkx_edges(G, pos, edge_color='k', width=6,
    #                                arrows=False)
    # plt.figure(3)
    # dnode = nx.draw_networkx_nodes(G, pos, node_size=300,
    #                                node_color='#FF6E1E')
    # nedge = nx.draw_networkx_edges(inferred, pos, edge_color='Orange', width=6,
    #                                arrows=False)
    plt.savefig("edge_colormap.pdf", facecolor='#C8C8C8')
    plt.show()
