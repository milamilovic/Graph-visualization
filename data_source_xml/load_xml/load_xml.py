from services.data_source_api import GraphLoading
import xml.etree.ElementTree as ET

# import ast
# import re

from models.node import Node as n
from models.edge import Edge as e
from models.graph import Graph as g


class XmlLoader(GraphLoading):
    def __init__(self):
        self.node_id = 0
        self.edge_id = 0
        self._graph = None

    def identifier(self):
        return 'xml_loader'

    def name(self):
        return 'XML loader'

    def load_graph(self, path: str) -> g:
        with open(path, encoding="utf-8") as file:
            data = self.load_file(file)
        return self.make_graph(data)

    def load_file(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        data = []
        for row_elem in root.findall('.//row'):
            data_row = {}
            for field in row_elem:
                data_row[field.tag] = field.text
            data.append(data_row)
        print("ucitano cvorova: ")
        print(len(data))
        return data

    def make_graph(self, data):
        self._graph = g()
        nodes = self.create_nodes(data)
        self.create_edges(nodes)
        return self._graph

    def create_nodes(self, data):
        nodes = []
        for item in data:
            node = n(None)
            node.id = self.get_next_node_id()
            for key, value in item.items():
                node.add_attribute(key, value)
            nodes.append(node)
            self.add_node(node)
        return nodes

    def add_node(self, node):
        already_in_graph = self._graph.contains_node(node)
        if not already_in_graph:
            self._graph.add_node(node)

    def get_next_node_id(self):
        current_id = self.node_id
        self.node_id += 1
        return current_id

    def get_next_edge_id(self):
        current_id = self.edge_id
        self.edge_id += 1
        return current_id

    def get_common_values(self, values_i, values_j):
        if isinstance(values_i, (set, list)) and isinstance(values_j, (set, list)):
            return set(values_i).intersection(set(values_j))
        else:
            if values_i == values_j:
                return {values_i}
        return set()

    def create_edges(self, nodes):
        for i, node_i in enumerate(nodes):
            for j, node_j in enumerate(nodes[i + 1:], start=i + 1):
                common_tags = set(node_i.tags()).intersection(node_j.tags())
                for tag in common_tags:
                    values_i = node_i.get_values_for_tag(tag)
                    values_j = node_j.get_values_for_tag(tag)
                    common_values = self.get_common_values(values_i, values_j)
                    if common_values:
                        if not self._graph.has_edge_between_nodes(node_i, node_j):
                            edge = e(self.get_next_edge_id(), node_i, node_j, tag, False)
                            node_i.add_edge(edge)
                            self._graph.add_edge(edge)
