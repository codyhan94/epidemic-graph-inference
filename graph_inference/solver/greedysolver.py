from pdb import set_trace
from graph_inference.solver.basesolver import BaseSolver

from collections import Counter

import numpy as np
import networkx as nx


class GreedySolver(BaseSolver):
    """A simple greedy algorithm for determining parental neighborhoods.

    The algorithm comes from Netrapalli's paper.
    """

    def __init__(self, cascades):
        """
        Sets up an instance of the greedy solver with a list of cascades.

        :param cascades: numpy array of cascades
        :return: None
        """
        super(GreedySolver, self).__init__(cascades)

        # Use this boolean array to "remove" cascades by indexing the main
        # cascades array with it.
        self.remaining_cascades = np.ndarray(len(cascades), dtype=np.bool)
        self.remaining_cascades.fill(True)

    def solve_node(self, node):
        """
        Computes the parental neighborhood for a particular node.

        :param node: integer index of node
        :return: numpy array of indices corresponding to nodes
        """
        parents = []
        self.remaining_cascades.fill(True)
        potential_parents = Counter()

        # set_trace()
        while any(self.remaining_cascades):
            # Store the cascades that contain a node infected one timestep
            # before our chosen node this iteration - they will be removed
            # from the remaining cascades.
            accounted_cascades = []

            for i, alive in enumerate(self.remaining_cascades):
                if not alive:
                    continue
                cascade = self.cascades[i]

                # This was a seed node or was never infected; can't have anyone
                # else infect it.
                if cascade[node] == 0 or np.isinf(cascade[node]):
                    accounted_cascades.append(i)
                    continue

                # Nodes infected one timestep before me could have infected me.
                possible_infectors = np.where(
                    (cascade == cascade[node] - 1) &
                    (np.isfinite(cascade[node])))[0]

                # These cascades are going to be removed for the next iteration
                # if np.any(possible_infectors):
                if len(possible_infectors) > 0:
                    accounted_cascades.append(i)
                    potential_parents.update(possible_infectors)

            # Add node that was infected one timestep before me in the
            # largest number of observed cascades to my parent neighborhood.
            if potential_parents:
                parent = potential_parents.most_common(1)[0][0]
                parents.append(parent)

            # Remove all cascades where node j was infected one step before me.
            self.remaining_cascades[accounted_cascades] = False
            potential_parents.clear()

        return parents

    def solve_graph(self, out_file=None):
        """
        Applies the greedy algorithm to each node in the graph.

        Produces a solution that can optionally be written out to a file. If
        no file is specified, then it returns a networkx DiGraph.

        :return: nx.DiGraph or Nothing
        """
        G = {}
        # Solve for each node one at a time for now.
        for node in range(len(self.cascades[0, ])):
            G[node] = self.solve_node(node)

        # Create the DiGraph object to either return or write to a file.
        nx_graph = nx.DiGraph(G)
        # Reverse the graph in-place to get the edges from parental
        # neighborhoods.
        # NOTE: setting copy=False in this function is NOT sufficient!
        nx_graph = nx_graph.reverse()
        if out_file:
            nx.write_graphml(nx_graph, path=out_file)
            return
        return nx_graph
