from __future__ import print_function

"""This is a general file used to test the basic functionality of our system"""

from graph_inference.graphs.gnp import GNPgraph
from graph_inference.sim.sirsim import SIRSim
# dummy code below while Cody pushes his code
from graph_inference.solver.greedysolver import GreedySolver
from graph_inference.analysis.baseanalysis import BaseAnalysis

if __name__== "__main__":
    graph = GNPgraph()
    graph.generate(1000,.2,False)
    graphfile = "data/testin.graphml"
    graph.graphml(graphfile)

    model = SIRSim(graphfile, 10)
    infectiontimes = SIRSim.run()
    inference = GreedySolver(infectiontimes)
    inferredfile = "data/testout.graphml"
    inference.regenerategraph(inferredfile)
    
    analysis = BaseAnalysis(graphfile, inferredfile)
    print("missing edges:", analysis.edgeerror())
    print("extra edges:", analysis.edgeextra())
    print("edge number:", analysis.edgedifference())





