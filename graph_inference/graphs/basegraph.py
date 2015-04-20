import networkx as nx

class BaseGraph(object):
    """ Base graph structure

    Default assumes networkx libraries for generation and usage. If you
    plan on using other libraries, overwrite all of the functions you need

    """
    # The networkx graph this wraps around.
    G = None
    graph_type = None
    directed = False
    edge_weighted = False
    node_weighted = False

    def __init__(self):
        self.generate()

    def generate(self):
        """ Generates an empty networkx graph """
        self.G = nx.Graph()

    def graphml(self, path):
        """ Generates a graphml file for the graph

        Args:
            path: a path to the file you want to write to
        """

        nx.readwrite.write_graphml(self.G, path)

    def laplacian(self):
        """Returns the Laplacian matrix.

        The Laplacian matrix is defined as L = D - A where D contains the
        outbound degree of a node and A is -1 if there is an edge from i to j.

        Returns:
            SciPy sparse matrix
        """
        pass

    def nodes(self):
        """Returns a list of all nodes and their weights if applicable.

        This function returns a list of nodes if unweighted, or a list of node-
        weight pairs if weighted.

        :returns: BaseGraph
        """

        return self.G.nodes()

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
