
from models.graph import Graph


def search_graph(query, nodes):
    graph = Graph()

    for node in nodes:
        attrs = node.attributes
        for key in attrs.keys():
            if isinstance(attrs[key], (int, str)):
                if key == query or (str(query).lower() in str(attrs[key]).lower()):
                    graph.add_node(node)
            elif isinstance(attrs[key], list):
                contains_dict = any(isinstance(item, dict) for item in attrs[key])
                if not contains_dict and any(key == query or str(query).lower() in str(item).lower() for item in attrs[key]):
                    graph.add_node(node)
                if contains_dict:
                    if key == query:
                        graph.add_node(node)

    for node in graph.nodes:
        for edge in node.edges:
            if graph.contains_node(edge.toNode) and graph.contains_node(edge.fromNode):
                graph.add_edge(edge)

    return graph