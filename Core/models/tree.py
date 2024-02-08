class NodeIdGenerator:

    def __init__(self):
        self.__current_id = 0

    def next(self):
        self.__current_id += 1
        return self.__current_id - 1

    def reset(self):
        self.__current_id = 0


nodeId = NodeIdGenerator()

class Vertex:
    __slots__ = '_attributes', '_id', '_edges'

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

    def degree(self):
        return len(self._edges)

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def add_edge(self, e):
        already_existing = self.contains_edge(e)
        if already_existing:
            self._edges[self._edges.index(already_existing)] = e
        else:
            self._edges.append(e)

    def contains_edge(self, e):
        for vertex in self._edges:
            if e == vertex:
                return vertex
        return None

    def relations(self):
        relations = []
        for edge in self._edges:
            if edge.relation_name in relations:
                continue
            relations.append(edge.relation_name)
        return relations

    def related_vertices(self, relation):
        vertices = []
        for edge in self._edges:
            if edge.relation_name == relation:
                if edge.source == self:
                    vertices.append(edge.destination)
        return vertices

    def is_related(self, vertex):
        for edge in self.edges:
            if edge.source == self:
                if edge.destination == vertex:
                    return True
            elif edge.destination == self:
                if edge.source == vertex:
                    return True
        return False

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other) -> bool:
        if self._id == other.id:
            return True
        if "id" in self._attributes and "id" in other.attributes:
            if self._attributes["id"] == other.attributes["id"]:
                return True
            return False

        if self._attributes != other.attributes:
            return False

        if len(self._edges) != len(other.edges):
            return False

        # TODO: how to compare sources without recursion error?
        # for edge in self._edges:
        #     for e in other.edges:
        #         if edge == e:
        #             break
        #     else:
        #         return False

        return True



class TreeNode(object):
    __slots__ = '_opened', '_object', '_object_type', '_children', '_id', '_parent'

    def __init__(self, object, parent, type):
        self._opened = False
        self._object = object
        self._object_type = type
        self._id = nodeId.next()
        self._children = []
        self._parent = parent


    @property
    def id(self):
        return self._id

    @property
    def opened(self):
        return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    def open(self):
        self._opened = True
        if len(self._children) <= 0:
            if self._object_type == "vertex":
                self.add_children(self._object.relations())
            else:
                self.add_children(self._parent.object.related_vertices(self._object))

    def load_children(self):
        if len(self._children) <= 0:
            if self._object_type == "vertex":
                self.add_children(self._object.relations())
            else:
                self.add_children(self._parent.object.related_vertices(self._object))

    def open_parents(self):
        self.open()
        if self._parent:
            self._parent.open_parents()

    def close(self):
        self._opened = False
        # for child in self._children:
        #     child.opened = False

    @property
    def object(self):
        return self._object

    @property
    def object_type(self):
        return self._object_type

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def find_node(self, id):
        if id == self._id:
            return self
        else:
            for child in self._children:
                found_node = child.find_node(id)
                if found_node:
                    return found_node

    def add_children(self, children_objects):
        for child in children_objects:
            if self._object_type == "vertex":
                child_type = "edge"
                child_node = TreeNode(child, self, child_type)
                # child_node.opened = True
                self._children.append(child_node)
            else:
                child_type = "vertex"
                # for related in self.parent.object.related_vertices(self.object):
                child_node = TreeNode(child, self, child_type)
                self._children.append(child_node)


class Forest(object):
    __slots__ = '_roots', '_last_opened'

    def __init__(self, roots=None):
        nodeId.reset()
        self._roots = roots
        if self._roots is None:
            self._roots = []
        print("ROOTS", self._roots)
        self._last_opened = 0

    def empty(self):
        self.roots = []
        self._last_opened = 0
        nodeId.reset()

    @property
    def roots(self):
        return self._roots

    @roots.setter
    def roots(self, roots):
        self._roots = roots

    @property
    def last_opened(self):
        return self._last_opened

    @last_opened.setter
    def last_opened(self, last_opened):
        self._last_opened = last_opened

    def find_tree_node(self, id):
        for root_node in self._roots:
            found_node = root_node.find_node(id)
            if found_node:
                return found_node

    def find_node_by_vertex_id(self, id, nodes=None):
        if not nodes:
            nodes = self._roots
        new_nodes = []
        for node in nodes:
            if node.object_type != "edge" and node.object.id == id:
                return node
            node.load_children()
            new_nodes += node.children
        if not new_nodes:
            return None
        return self.find_node_by_vertex_id(id, new_nodes)