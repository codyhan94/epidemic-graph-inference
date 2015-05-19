from __future__ import print_function

import sys
sys.path.append('.')

from argparse import ArgumentParser
from graph_inference.sim.sirsim import SIRSim
from graph_inference.solver.greedysolver import GreedySolver

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('graph', help='GraphML file containing the graph to '
                                      'run on.')
    parser.add_argument('-n', '--num-cascades',
                        help='Number of cascades to run, defaults to 1.',
                        type=int, default=1)
    parser.add_argument('-o', '--out-file',
                        help='File to write the output graph to. If not '
                             'specified no output will be generated.')
    args = parser.parse_args()

    graph = args.graph

    S = SIRSim(graph, n_cascades=args.num_cascades, p_init=0.05)
    cascades = S.run()

    solver = GreedySolver(cascades)
    res = solver.solve_graph(out_file=args.out_file)
