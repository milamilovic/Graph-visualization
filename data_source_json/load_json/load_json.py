from services.data_source_api import GraphLoading
import json

from models.edge import Edge
from models.graph import Graph
from models.node import Node


class JsonLoader(GraphLoading):

    def __init__(self):
        super().__init__()
        self._id_counter_node = 0
        self._id_counter_edge = 0
        self._graph = None

    def identifier(self):
        return 'json_loader'

    def name(self):
        return 'JSON loader'

    def load_graph(self, path: str) -> Graph:
        with open(path, encoding="utf-8") as file:
            data = self.load_file(file)
        return self.make_graph(data)

    def load_file(self, file):
        json_object = json.load(file)
        return json_object

    def make_graph(self, data):
        self._graph = Graph()
        self.create_nodes(data)
        self.create_edges(self._graph.nodes)
        return self._graph

    def create_nodes(self, data):
        for item in data:
            self.build_node(item)

    def build_node(self, item):
        build_node = Node(None)
        build_node.id = self.next_id_node()
        build_node.add_attribute("id", build_node.id)

        for key, value in item.items():
            build_node.add_attribute(key, value)
            if isinstance(value, dict):
                new_node = self.build_node(value)
                edge = Edge(self.next_id_edge(), build_node, new_node, key, False)
                build_node.add_edge(edge)
                self._graph.add_edge(edge)
            if isinstance(value, list) and isinstance(value[0], dict):
                for v in value:
                    new_node = self.build_node(v)
                    edge = Edge(self.next_id_edge(), build_node, new_node, key, False)
                    build_node.add_edge(edge)
                    self._graph.add_edge(edge)

        self.add_node(build_node)
        return build_node

    def create_edges(self, nodes):
        for i in range(len(nodes)):
            attributes_i = nodes[i].attributes
            for j in range(i + 1, len(nodes)):
                attributes_j = nodes[j].attributes
                common_attributes = set(attributes_i.keys()).intersection(attributes_j.keys())
                for attribute in common_attributes:
                    values_i = attributes_i[attribute]
                    values_j = attributes_j[attribute]

                    common_values = self.get_common_values(values_i, values_j)
                    if common_values:
                        edge = Edge(self.next_id_edge(), nodes[i], nodes[j], attribute, False)
                        nodes[i].add_edge(edge)
                        self._graph.add_edge(edge)

    def get_common_values(self, values_i, values_j):
        if isinstance(values_i, (set, list)) and isinstance(values_j, (set, list)):
            if isinstance(values_i[0], dict):
                return set()
            return set(values_i).intersection(set(values_j))
        else:
            if isinstance(values_i, dict):
                return set()
            if values_i == values_j:
                return {values_i}
        return set()

    def add_node(self, node):
        already_in_graph = self._graph.contains_node(node)
        if not already_in_graph:
            self._graph.add_node(node)

    def next_id_node(self):
        current_id = self._id_counter_node
        self._id_counter_node += 1
        return current_id

    def next_id_edge(self):
        current_id = self._id_counter_edge
        self._id_counter_edge += 1
        return current_id
