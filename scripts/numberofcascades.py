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
    n = 50
    graph = TreeGraph()
    graph.generate(n)
    graph.graphml(graphfile)
    print(graphfile, "created")
    G = graph.G

    n_cascades = 2000
    p_init = 0.05
    model = SIRSim(G, n_cascades, p_init)
    print("Starting simulation with ", n_cascades, " cascades")
    cascades = model.run()

    # G = nx.convert_node_labels_to_integers(G)
    edgelist = G.edges()
    unfound = [True] * len(edgelist)
    foundtimes = [np.inf] * len(edgelist)
    for i in range(n_cascades):
        solver = GreedySolver(cascades[:i + 1])
        inferred = solver.solve_graph()
        newedges = inferred.edges()
        for j in range(len(edgelist)):
            if unfound[j]:
                if edgelist[j] in newedges:
                    unfound[j] = False
                    foundtimes[j] = i + 1
        if not any(unfound):
            break

    print(sorted(edgelist))
    print(sorted(newedges))
    print(foundtimes)
    # Make plots, using the dot package to make trees look nice.

    fig = plt.figure(1)
    axes = fig.add_subplot(1, 1, 1, axisbg='#C8C8C8')
    pos = nx.graphviz_layout(G, prog='twopi')
    # pos = nx.graphviz_layout(analysis.G, prog='dot')
    dnode = nx.draw_networkx_nodes(G, pos, node_size=300,
                                   node_color='#FF6E1E')

    enode = nx.draw_networkx_edges(G, pos, edge_color=foundtimes,
                                   edge_cmap=plt.cm.Oranges, width=6,
                                   arrows=False, edge_vmin=1, edge_vmax=400)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=dict(zip(edgelist, foundtimes))
    )
    plt.colorbar(enode)
    plt.axis('off')
    plt.savefig("edge_colormap.pdf", facecolor='#C8C8C8')
    plt.title("Number of Cascades Needed to Learn Edge")
    plt.show()
