import networkx


class neograph:
    graphtype = None
    directed = False
    edgeweighted = False
    nodeweigted = False

    def __init__(self):
        self.generate()

    def generate():
        pass

    def laplacian(self):
        """Returns the Laplacian matrix. 

            The Laplacian matrix is defined as L = D - A where D contains
            the outbound degree of a node and A is -1 if there is an edge
            from i to j
        """
        pass

    def nodes(self):
        """ Returns a list of all nodes and their weights if applicable.

            This function returns a list of nodes if unweighted, or a list of
            node-weight pairs if weighted
        """
        pass

    def adjacencymatrix(self):
        """ Returns an adjacency matrix

            Each (i,j) of the matrix is the weight of the edge if there is an
            edge between i and j, or the weight of the node if i=j, or 0 
            otherwise
        """
        pass

    def adjacencylist(self):
        """ Retuns an adjacency list, including edge weights if applicable

            Format is a list of (origin, destination, [weight]) pairs
        """
        pass

class GNPgraph(neograph):
    """docstring for GNPgraph"""
    def __init__(self, arg):
        super(GNPgraph, self).__init__()
        self.arg = arg
        