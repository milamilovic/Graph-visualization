

class Edge:

    def __init__(self, id,fromNode, toNode, name, is_directed):
        self._fromNode = fromNode
        self._toNode = toNode
        self._name = name
        self._id = id
        self._is_directed = is_directed

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id



    @property
    def fromNode(self):
        return self._fromNode

    @fromNode.setter
    def fromNode(self, fromNode):
        self._fromNode = fromNode

    @property
    def toNode(self):
        return self._toNode

    @toNode.setter
    def toNode(self, toNode):
        self._toNode = toNode

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def is_directed(self):
        return self._is_directed

    @is_directed.setter
    def is_directed(self, is_directed):
        self._is_directed = is_directed


    def endpoints(self):
        return self._fromNode, self._toNode

