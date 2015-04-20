import networkx

class BaseGraph(object):
    graph_type = None
    directed = False
    edge_weighted = False
    node_weighted = False

    def __init__(self):
        self.generate()

    def generate():
        pass

    def laplacian(self):
        """Returns the Laplacian matrix.

        The Laplacian matrix is defined as L = D - A where D contains the
        outbound degree of a node and A is -1 if there is an edge from i to j.

        :returns: Nothing.
        """
        pass

    def nodes(self):
        """Returns a list of all nodes and their weights if applicable.

        This function returns a list of nodes if unweighted, or a list of node-
        weight pairs if weighted.

        :returns: BaseGraph
        """
        pass

    def adjacencyMatrix(self):
        """
        Returns an adjacency matrix

        Each (i,j) of the matrix is the weight of the edge if there is an edge
        between i and j, or the weight of the node if i=j, or 0 otherwise.
        """
        pass

    def adjacencyList(self):
        """Returns an adjacency list, including edge weights if applicable

        Format is a list of (origin, destination, [weight]) pairs.
        """
        pass
