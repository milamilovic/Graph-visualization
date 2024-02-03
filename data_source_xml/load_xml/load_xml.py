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
            # planes_text = row_elem.find('planes').text
            # planes_text_cleaned = re.sub(r'(["\[\],])', '', planes_text)
            # planes_list = ast.literal_eval(planes_text_cleaned)
            data_row = {
                'airline_iata': row_elem.find('airline_iata').text,
                'airline_icao': row_elem.find('airline_icao').text,
                'departure_airport_iata': row_elem.find('departure_airport_iata').text,
                'departure_airport_icao': row_elem.find('departure_airport_icao').text,
                'arrival_airport_iata': row_elem.find('arrival_airport_iata').text,
                'arrival_airport_icao': row_elem.find('arrival_airport_icao').text,
                'codeshare': row_elem.find('codeshare').text.lower() == 'true',
                'transfers': int(row_elem.find('transfers').text)
                # 'planes': planes_list
            }
            data.append(data_row)
        print("ucitano letova: ")
        print(len(data))
        return data

    def make_graph(self, data):
        self._graph = g()
        nodes = self.create_airline_nodes(data)
        return self._graph

    def create_airline_nodes(self, data):
        nodes = []
        for item in data:
            airline_node = n(None)
            airline_node.id = self.get_next_node_id()

            for key, value in item.items():
                airline_node.add_attribute(key, value)

            nodes.append(airline_node)
            self.add_node(airline_node)
        return nodes

    def add_node(self, node):
        already_in_graph = self._graph.contains_node(node)
        if not already_in_graph:
            self._graph.add_node(node)

    def get_next_node_id(self):
        current_id = self.node_id
        self.node_id += 1
        return current_id