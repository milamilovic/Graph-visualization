from deepdiff import DeepDiff


class Graph:
    def __init__(self):
        self._id = 0
        self._nodes = []
        self._edges = []

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    def add_node(self, node):
        self._nodes.append(node)

    def add_edge(self, edge):
        self._edges.append(edge)

    def contains_node(self, node):
        for n in self._nodes:
            if not DeepDiff(n.attributes, node.attributes):
                return True
        return False
