from graph_inference.graphs.basegraph import BaseGraph

class GNPgraph(BaseGraph):
    """Generates a GNP graph."""

    def __init__(self, arg):
        super(GNPgraph, self).__init__()
        self.arg = arg
