import copy

from deepdiff import DeepDiff


class Graph:
    def __init__(self):
        self._id = 0
        self._nodes = []
        self._edges = []
        self.visited = []

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
        # if node in self._nodes:
        #     return
        self._nodes.append(node)

    def add_edge(self, edge):
        self._edges.append(edge)

    def contains_node(self, node):
       for n in self._nodes:
          if not DeepDiff(n.attributes, node.attributes):
             return True
       return False

    def get_node(self, id):
        for node in self._nodes:
            if node.attributes["id"] == id:
                return node

    def has_edge_between_nodes(self, node1, node2):
        for edge in self._edges:
            if edge.fromNode == node1 and edge.toNode == node2:
                return True
        return False

    def find_subgraphs(self, nodes=None, graphs=None):
        if not nodes:
            nodes = []
        if not graphs:
            graphs = []
        changes = True
        if not nodes:
            nodes = copy.deepcopy(self._nodes)

        connected = {}
        for node in nodes:
            if len(connected) == 0:
                connected[node] = True
            else:
                connected[node] = False

        if list(connected.values()) == [True * len(nodes)]:
            subgraph = Graph()
            subgraph.nodes = list(connected.keys())
            graphs.append(subgraph)
            return graphs

        while changes:
            changes = False
            for v in nodes:
                if connected[v]:
                    if self.check_as_true(v.edges, connected):
                        changes = True
                else:
                    if self.check_if_true(v, connected):
                        connected[v] = True
                        if self.check_as_true(v.edges, connected):
                            changes = True

        if list(connected.values()) == [True for i in range(len(connected.values()))]:
            subgraph = Graph()
            subgraph.nodes = list(connected.keys())
            graphs.append(subgraph)
            return graphs

        removed = self.remove_connected_nodes(nodes, connected)
        subgraph = Graph()
        subgraph.nodes = removed
        graphs.append(subgraph)
        return self.find_subgraphs(nodes, graphs)

    def check_if_true(self, node, connected):
        for edge in node.edges:
            if connected[edge.fromNode]:
                return True
            elif connected[edge.toNode]:
                return True
        return False

    def check_as_true(self, edges, connected):
        changes = False
        for edge in edges:
            if connected[edge.fromNode] is False:
                changes = True
            elif connected[edge.toNode] is False:
                changes = True
            connected[edge.fromNode] = True
            connected[edge.toNode] = True

        return changes

    def remove_connected_nodes(self, nodes, connected):
        removed = []
        for v in connected.keys():
            if connected[v]:
                nodes.remove(v)
                removed.append(v)

        return removed

    def is_graph_directed(self):
        if len(self._edges) > 0:
            return list(self._edges)[0].is_directed

    def find_conture_nodes(self):
        contour_nodes = set()
        for edge in self._edges:
            contour_nodes.add(edge.fromNode)
            contour_nodes.add(edge.toNode)
        return contour_nodes

    def has_cycle_directed(self, node):
        visited = set()
        path = []

        def dfs(current, parent):
            if current in path:
                if path[0] not in contour_nodes:
                    contour_nodes.append(path[0])
                return
            if current in visited:
                return
            path.append(current)
            visited.add(current)
            for edge in self._edges:
                if edge.fromNode == current:
                    dfs(edge.toNode, current)
            path.pop()

        contour_nodes = []
        dfs(node, None)
        return contour_nodes

    def find_not_destination_nodes(self):
        destinations = set(edge.toNode for edge in self._edges)
        roots = [node for node in self._nodes if node not in destinations]
        return roots

    def has_cycle_undirected(self):
        visited = set()
        for node in self._nodes:
            if node not in visited:
                if self._has_cycle_undirected_helper(node, visited, None):
                    return True
        return False

    def _has_cycle_undirected_helper(self, current, visited, parent):
        visited.add(current)
        for edge in current.edges:
            neighbor = edge.toNode if edge.fromNode == current else edge.fromNode
            if neighbor != parent:
                if neighbor in visited or self._has_cycle_undirected_helper(neighbor, visited, current):
                    return True
        return False

    def depth_first_search(self, current, parent):
        self.visited.append(current)
        for vertex in self._nodes:
            if current.is_related(vertex):
                if parent and vertex == parent:
                    continue
                if vertex in self.visited:
                    if vertex != self.visited[-1]:
                        return True
                elif self.depth_first_search(vertex, current):
                    return True
        return False
