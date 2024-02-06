
from models.graph import Graph


def check_value(param, operator, value):
    if operator == '==':
        result = value == param
    elif operator == '>':
        result = value > param
    elif operator == '>=':
        result = value >= param
    elif operator == '<':
        result = value < param
    elif operator == '<=':
        result = value <= param
    elif operator == '!=':
        result = value != param
    else:
        raise ValueError("Invalid operator")

    return result


def filter_graph(attribute, operator, value, nodes):
    graph = Graph()

    for node in nodes:
        attrs = node.attributes
        for key in attrs.keys():
            if key == attribute:
                if isinstance(attrs[key], int):
                    result = check_value(int(value), operator, int(attrs[key]))
                    if result:
                        graph.add_node(node)
                if isinstance(attrs[key], str):
                    result = check_value(str(value), operator, str(attrs[key]))
                    if result:
                        graph.add_node(node)

                final_result = True
                if isinstance(attrs[key], list):
                    contains_dict = any(isinstance(item, dict) for item in attrs[key])
                    if not contains_dict and key == attribute:
                        for item in attrs[key]:
                            if isinstance(item, int):
                                result = check_value(int(value), operator, int(item))
                                if not result:
                                    final_result = False
                            if isinstance(item, str):
                                result = check_value(str(value), operator, str(item))
                                if not result:
                                    final_result = False

                        if final_result:
                            graph.add_node(node)

    for node in graph.nodes:
        for edge in node.edges:
            if graph.contains_node(edge.toNode) and graph.contains_node(edge.fromNode):
                graph.add_edge(edge)

    return graph
