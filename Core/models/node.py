class Node:
    def __init__(self, id):
        self._attributes = {}
        self._id = id
        self._edges = []

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

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

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def add_edge(self, edge):
        self._edges.append(edge)


    def contains_edge(self, edge):
        return edge in self._edges
