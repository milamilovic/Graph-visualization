from services.data_source_api import GraphLoading
from models import graph as g
from models import node as n
from models import edge as e
from rdflib import Graph


class RDFLoader(GraphLoading):
    def __init__(self) -> None:
        self.graph = None
        self.exist = 0
        self.node_id = 0
        self.edge_id = 0

    def identifier(self):
        return 'rdf_loader'

    def name(self):
        return 'RDF loader'

    def load_data(self, path):
        rdf_graph = Graph()
        rdf_graph.parse(path)
        # for s, p, o in g:
        #     print(s, p, o)
        return rdf_graph

    def create_node(self, node):
        for existing_node in self.graph.nodes:
            if existing_node.attributes['name'] == node:
                # print("jednako")
                self.exist += 1
                return existing_node

        # print("ovde ipak")
        self.node_id += 1
        new_node = n.Node(self.node_id)
        new_node.attributes['name'] = node
        self.graph.add_node(new_node)
        return new_node

    def create_edge(self, edge, from_node, to_node):
        name = edge.split("/")[-1]
        # print(name)
        self.edge_id += 1
        new_edge = e.Edge(self.edge_id, from_node, to_node, name, True)
        from_node.add_edge(new_edge)
        to_node.add_edge(new_edge)
        self.graph.add_edge(new_edge)

    def make_graph(self, data):
        for line in data:
            (s, p, o) = line
            from_node = self.create_node(s)
            to_node = self.create_node(o)
            self.create_edge(p, from_node, to_node)

    def load_graph(self, path: str) -> Graph:
        self.graph = g.Graph()
        data = self.load_data(path)
        self.make_graph(data)
        return self.graph

    def graph(self):
        return self.graph