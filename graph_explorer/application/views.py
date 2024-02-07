import re

from django.shortcuts import render
from django.apps.registry import apps
from use_cases import load_plugins
from use_cases import filter
from use_cases import search as search_core
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
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})


def search(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    base_graph = apps.get_app_config('application').get_base_graph()
    current_visualizer = apps.get_app_config('application').get_current_visualizer()

    query = request.POST['search']

    nodes = base_graph.nodes

    graph = search_core.search_graph(query, nodes)

    load_plugins.visualize(visualisers, current_visualizer, graph, request)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})


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


def filter_graph(request):
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

    graph = filter.filter_graph(attribute, operator, value, nodes)

    load_plugins.visualize(visualisers, current_visualizer, graph, request)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders})
