from __future__ import print_function

from graph_inference.sim.basesim import BaseSim
# from graph_inference.graphs import basegraph
from pdb import set_trace

import random

import numpy as np
import networkx as nx

class SISim(BaseSim):
    """
    SI simulation: individuals are either susceptible or infected with no chance
    of recovery. If an infected individual (a) [successfully] attempts to infect
    another infected individual (b) at time t, b's infection time will not
    change from what it was to t.

    The output is a vector of *first* infection time for each node, and infinity
    if a node was never infected.
    """

    def __init__(self, graph_file, n_cascades=1, mu=0.1):
        """Set up a
        """
        super(SISim, self).__init__(graph_file, n_cascades)

        # Use integer labels to index into the infection times vector.
        self.G = nx.convert_node_labels_to_integers(self.G)

        # Every node starts off susceptible.
        self.susceptible = set(self.G.nodes())
        self.infected = set()
        self.can_be_infected = set()

        # Mark the timesteps.
        self.t = 0

        # Array of infection times for each node.
        self.infection_times = np.ndarray(len(self.G))
        self.infection_times.fill(np.inf)

        self.mu = mu
        self.DEBUG = True

        self.initialize_graph()

    def reset(self):
        """
        Resets the simulation so we can run multiple cascades.
        """
        self.infected.clear()
        self.t = 0
        self.infection_times.fill(np.inf)
        self.initialize_graph()

    def load_graph(self, graph_file):
        return nx.read_graphml(graph_file)

    def initialize_graph(self):
        """Prepares the graph for running cascades.

        This consists of assigning edge weights if there are none already and
        seeding each node with the seed probability.
        """
        for n, nbrdict in self.G.adjacency_iter():
            # Assign an edge weight to each edge.
            for nbr, eattr in nbrdict.iteritems():
                if 'weight' not in eattr:
                    eattr['weight'] = random.random()

            # Seed each node with probability mu.
            if random.random() < self.mu:
                self.infected.add(n)
                self.infection_times[n] = 0

    def step(self):
        """Runs one step of the simulation.

        :return: Nothing
        """
        # Increment time first so that we record accurate first-infection times.
        self.t += 1
        next_infected = set()

        set_trace()
        for n in self.infected:
            for nbr in self.G[n]:
                # self.dprint('%d trying to infect %d at time %d' % (n, nbr, self.t))
                # Only try to infect if this neighbor is not already infected.
                if nbr not in self.infected:
                    if random.random() < self.G[n][nbr]['weight']:
                        # self.dprint('Infected', nbr, 'at time:', self.t)
                        next_infected.add(nbr)
                        self.infection_times[nbr] = self.t

        self.dprint('next infected set:', next_infected)
        self.last_infected.update(self.infected)
        self.infected.update(next_infected)

    def stable(self):
        """Has the epidemic stabilized? """
        self.dprint('Infected \ previous_infected:', self.infected.difference(self.last_infected))
        return self.last_infected == self.infected

    def run(self):
        """Runs the simulation and returns the output (vector of times)

        :return: numpy array
        """
        all_cascades = []

        for _ in range(self.n_cascades):
            while not self.stable():
                print('Infected: ', self.infected)
                self.step()

            all_cascades.append(self.infection_times.copy())

            self.reset()

        return np.array(all_cascades)
