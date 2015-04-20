from __future__ import print_function

from graph_inference.sim.basesim import BaseSim
# from graph_inference.graphs import basegraph

import random
import sys

import numpy as np
import networkx as nx

class SISim(BaseSim):
    """Base class for network inference simulations."""

    def __init__(self, graph_file, n_cascades=1, mu=0.1):
        """Set up a
        """
        # Read in the graph from the GraphML file.
        self.G = nx.read_graphml(graph_file)

        # Use integer labels to index into the infection times vector.
        self.G = nx.convert_node_labels_to_integers(self.G)

        # Every node starts off susceptible.
        self.susceptible = set(self.G.nodes())
        self.infected = set()
        self.last_infected = set()
        self.n_cascades = n_cascades

        # Mark the timesteps.
        self.t = 0

        # Array of infection times for each node.
        self.infection_times = np.ndarray(len(self.G))
        self.infection_times.fill(np.inf)

        self.mu = mu
        self.initialize_graph()

        self.DEBUG = True
        pass

    def dprint(self, *args):
        if self.DEBUG:
            print('DEBUG: ', *args, file=sys.stderr)

    def initialize_graph(self):
        """Set up the graph, using random edge weights for now. """
        for n, nbrdict in self.G.adjacency_iter():
            # Assign an edge weight to each edge.
            for nbr, eattr in nbrdict.iteritems():
                if 'weight' not in eattr:
                    eattr['weight'] = random.random()

            # Seed each node with probability mu.
            if random.random() < self.mu:
                self.infected.add(n)
                self.infection_times[n] = 0
        return

    def step(self):
        """Runs one step of the simulation.

        :return: Nothing
        """
        # Increment time first so that we record accurate first-infection times.
        self.t += 1
        next_infected = set()

        for n in self.infected:
            for nbr in self.G[n]:
                # self.dprint('%d trying to infect %d at time %d' % (n, nbr, self.t))
                if random.random() < self.G[n][nbr]['weight']:
                    # self.dprint('Infected', nbr, 'at time:', self.t)
                    next_infected.add(nbr)
                    self.infection_times[nbr] = self.t

        self.dprint('next infected set:', next_infected)
        self.last_infected = self.infected
        self.infected.update(next_infected)

    def stable(self):
        """Has the epidemic stabilized? """
        self.dprint('Infected \ previous_infected:', self.infected.difference(self.last_infected))
        return self.last_infected == self.infected

    def run(self):
        """Runs the simulation and returns the output (vector of times)

        :return: numpy array
        """
        while not self.stable():
            print('Infected: ', self.infected)
            self.step()
        return
