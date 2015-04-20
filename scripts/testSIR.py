from graph_inference.sim.sirsim import SIRSim

if __name__ == '__main__':
    S = SIRSim('graphs/gnp100-.4.graphml', n_cascades=1, mu=0.05)
