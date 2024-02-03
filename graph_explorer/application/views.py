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
    return render(request, "index.html",{'visualisers': visualisers, 'loaders': loaders})


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
        load_plugins.load_data_source(loaders, visualisers, selected_parser, selected_visualizer, selected_file, request)
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
                if attrs[key] == query or (str(query) in str(attrs[key])):
                    graph.add_node(node)
            elif isinstance(attrs[key], list):
                contains_dict = any(isinstance(item, dict) for item in attrs[key])
                if not contains_dict and any(item == query or str(item) == str(query) for item in attrs[key]):
                    graph.add_node(node)

    for node in graph.nodes:
        for edge in node.edges:
            if graph.contains_node(edge.toNode) and graph.contains_node(edge.fromNode):
                graph.add_edge(edge)

    load_plugins.visualize(visualisers, current_visualizer, graph, request)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})
