import re

from django.shortcuts import render
from django.apps.registry import apps
from use_cases import load_plugins
from models.graph import Graph
from models.node import Node
from models.edge import Edge


# Create your views here.
def index(request):
    load_plugins.load()
    # loaders = apps.get_app_config('application').loaders
    # visualisers = apps.get_app_config('application').visualizers

    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    print("Visualisers", visualisers)
    print("Loaders", loaders)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})


def load_data_source(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]

    if request.method == 'POST':
        # selected_parser = request.POST.get('parser')
        # print("Selected parser:", selected_parser)
        # load_plugins.load_data_source(loaders, selected_parser)
        selected_parser = request.POST.get('parser')
        selected_visualizer = request.POST.get('visualizer')
        selected_file = request.POST.get('file')
        load_plugins.load_data_source(loaders, visualisers, selected_parser, selected_visualizer, selected_file,
                                      request)
        graph = apps.get_app_config('application').get_base_graph()
        print(graph)
        print("VIEWS", len(graph.nodes))
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})


def search(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    base_graph = apps.get_app_config('application').get_base_graph()
    current_visualizer = apps.get_app_config('application').get_current_visualizer()

    query = request.POST['search']

    nodes = base_graph.nodes
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

    load_plugins.visualize(visualisers, current_visualizer, graph, request)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})


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


def split_query(query):
    operators_pattern = re.compile(r'==|>|>=|<|<=|!=')

    operators = operators_pattern.findall(query)
    substrings = operators_pattern.split(query)

    result = []
    for i in range(len(substrings) - 1):
        result.append(substrings[i])
        result.append(operators[i])

    result.append(substrings[-1])

    return result


def filter(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    base_graph = apps.get_app_config('application').get_base_graph()
    current_visualizer = apps.get_app_config('application').get_current_visualizer()

    query = request.POST['filter']

    query_split = split_query(query)
    attribute = query_split[0]
    operator = query_split[1]
    value = query_split[2]

    nodes = base_graph.nodes
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

    load_plugins.visualize(visualisers, current_visualizer, graph, request)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})
