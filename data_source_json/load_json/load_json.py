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
        nodes = self.create_movie_nodes(data)
        self.connect_movies_with_same_actors(nodes)
        return self._graph

    def create_movie_nodes(self, data):
        nodes = []
        for item in data:
            if isinstance(item, dict):
                movie_node = Node(None)
                movie_node.id = self.next_id_node()
                movie_node.add_attribute("id", movie_node.id)

                for key, value in item.items():
                    movie_node.add_attribute(key, value)

                nodes.append(movie_node)
                self.add_node(movie_node)
        return nodes

    def connect_movies_with_same_actors(self, nodes):
        for i in range(len(nodes)):
            actors_i = set(nodes[i].attributes.get("actors", []))
            for j in range(i + 1, len(nodes)):
                actors_j = set(nodes[j].attributes.get("actors", []))
                common_actors = actors_i.intersection(actors_j)
                if common_actors:
                    edge = Edge(self.next_id_edge(), nodes[i], nodes[j], nodes[j].attributes["title"], True)
                    nodes[i].add_edge(edge)
                    self._graph.add_edge(edge)

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
