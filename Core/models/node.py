class Node:

    __slots__ = '_attributes', '_id', '_edges'
    def __init__(self, id):
        self._attributes = {}
        self._id = id
        self._edges = []

    def __str__(self):
        return '({0},{1},{2})'.format(self._attributes, self._id, self._edges)

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

    def tags(self):
        return set(self._attributes.keys())

    def get_values_for_tag(self, tag):
        return [self._attributes[tag]]

    def relations(self):
        relations = []
        for edge in self._edges:
            if edge.name not in relations:
                relations.append(edge.name)
        return relations

    def related_vertices(self, relation):
        vertices = []
        for edge in self._edges:
            if edge.name == relation:
                if edge.fromNode == self:
                    vertices.append(edge.toNode)
        return vertices