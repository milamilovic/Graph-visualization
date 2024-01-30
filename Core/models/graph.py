
class Graph:
    def __init__(self):
        self._id = id
        self._nodes = []

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

    def add_node(self, node):
        self.nodes.append(node)

    def contains_node(self, node):
        pass




