from __future__ import print_function
from collections import defaultdict

from graph_inference.sim.basesim import BaseSim

import random
import numpy as np
import networkx as nx


class SIRSim(BaseSim):
    """Base class for network inference simulations."""

    def __init__(self, graph_file, n_cascades=1, p_init=0.1):
        """Set up a SIR simulation class.
        """
        super(SIRSim, self).__init__(graph_file, n_cascades)

        # Use integer labels to index into the infection times vector.
        self.G = nx.convert_node_labels_to_integers(self.G)

        # Every node starts off susceptible.
        self.susceptible = set(self.G.nodes())
        self.infected = set()
        self.recovered = set()

        self.last_infected = set()

        # Mark the timesteps.
        self.t = 0

        # Array of infection times for each node.
        self.infection_times = np.ndarray(len(self.G))
        self.infection_times.fill(np.inf)

        self.p_init = p_init
        self.DEBUG = False
        self.initialize_graph()

    def reset(self):
        """
        Resets the simulation so we can run multiple cascades.
        """
        self.infected.clear()
        self.recovered.clear()
        self.last_infected.clear()
        self.t = 0
        self.infection_times.fill(np.inf)
        self.initialize_graph()

    def load_graph(self, graph_file):
        return nx.read_graphml(graph_file)

    def initialize_graph(self):
        """Prepare the graph for running cascades: edge weights and seed nodes.

        Sets up the graph with a uniform random (0, 1) edge weight for each edge
        (u, v) and seeds each node with probability mu.

        Note: only assigns a weight to an edge if it doesn't have one already.
        """
        for n, nbrdict in self.G.adjacency_iter():
            # Assign an edge weight to each edge.
            for nbr, eattr in nbrdict.iteritems():
                if 'weight' not in eattr:
                    eattr['weight'] = random.random()

            # Seed each node with probability p_init.
            if random.random() < self.p_init:
                self.infected.add(n)
                self.infection_times[n] = 0

    def compute_alpha(self):
        """
        Compute the value of the correlation decay coefficient of this graph.

        This is alpha such that for every node the sum of all probabilities
        of all incoming edges is at most 1 - alpha.

        :return: alpha
        :rtype: float
        """
        inc_weights = defaultdict(int)
        for (u, v) in self.G.out_edges_iter():
            inc_weights[v] += self.G[u][v]['weight']
        return 1 - max(inc_weights.values())

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
                # A recovered node cannot be infected again.
                if nbr in self.recovered:
                    break
                if random.random() < self.G[n][nbr]['weight']:
                    # self.dprint('Infected', nbr, 'at time:', self.t)
                    next_infected.add(nbr)
                    self.infection_times[nbr] = self.t
            # Each node is only active for one time step.
            self.recovered.add(n)

        self.dprint('recovered nodes:', self.recovered)
        self.dprint('next infected set:', next_infected)

        # self.last_infected = self.infected
        self.infected = next_infected
        # self.infected.update(next_infected)

    def stable(self):
        """Has the epidemic stabilized? """
        return len(self.infected) == 0

    def run(self):
        """Runs the simulation and returns the output (vector of times)

        :return: numpy array
        """
        all_cascades = []

        for _ in range(self.n_cascades):
            # Run the entire simulation once (one cascade).
            while not self.stable():
                self.step()

            # Store the results of simulation.
            all_cascades.append(self.infection_times.copy())

            # And prepare for another cascade.
            self.reset()

        return np.array(all_cascades)
