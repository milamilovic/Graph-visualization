import os
import re

from django.core.mail.backends import console
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.apps.registry import apps
from django.template.loader import render_to_string
from use_cases import load_plugins
from use_cases import filter
from use_cases import search as search_core
from use_cases import workspace as w
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
    workspaces = apps.get_app_config('application').get_workspaces()
    tree = apps.get_app_config("application").tree

    print("INDEX WORKSPACE", workspaces)
    print("Visualisers", visualisers)
    print("Loaders", loaders)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces, 'tree':tree})


def workspace(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    tree = apps.get_app_config("application").tree


    w.add_workspace()
    workspaces = apps.get_app_config('application').get_workspaces()

    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces, 'tree':tree})


def load_workspace(request):
    # load_plugins.load()
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]

    workspaces = apps.get_app_config('application').get_workspaces()
    current_visualizer = apps.get_app_config('application').get_current_visualizer()


    selected_workspace = request.POST.get('workspaces_select')
    print("OPTION", selected_workspace)
    w.set_current_workspace(selected_workspace)
    print("Graf", workspaces[int(selected_workspace)])
    tree = None

    if current_visualizer is not None:
        load_plugins.visualize(visualisers, current_visualizer, workspaces[int(selected_workspace)], request)
        apps.get_app_config('application').load_tree()
        tree = apps.get_app_config('application').tree

    if tree is None:
        return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces})

    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces,
                                          'tree': tree})




def load_data_source(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    workspaces = apps.get_app_config('application').get_workspaces()

    if request.method == 'POST':
        # selected_parser = request.POST.get('parser')
        # print("Selected parser:", selected_parser)
        # load_plugins.load_data_source(loaders, selected_parser)
        selected_parser = request.POST.get('parser')
        selected_visualizer = request.POST.get('visualizer')
        selected_file = request.POST.get('file')
        tree = None

        try:
            load_plugins.load_data_source(loaders, visualisers, selected_parser, selected_visualizer, selected_file,
                                          request)
            apps.get_app_config('application').load_tree()
            tree = apps.get_app_config('application').tree
        except:
            # bad formats
            pass
        # graph = apps.get_app_config('application').get_base_graph()
        # print(graph)
        # print("VIEWS", len(graph.nodes))

    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces, 'tree':tree})



def search(request):
    loaders = apps.get_app_config('application').get_plugins()[0]
    visualisers = apps.get_app_config('application').get_plugins()[1]
    base_graph = apps.get_app_config('application').get_base_graph()
    workspaces = apps.get_app_config('application').get_workspaces()

    current_visualizer = apps.get_app_config('application').get_current_visualizer()

    query = request.POST['search']

    nodes = base_graph.nodes

    graph = search_core.search_graph(query, nodes)

    load_plugins.visualize(visualisers, current_visualizer, graph, request)
    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces})



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
    workspaces = apps.get_app_config('application').get_workspaces()
    current_visualizer = apps.get_app_config('application').get_current_visualizer()

    query = request.POST['filter']

    try:
        query_split = split_query(query)
        attribute = query_split[0]
        operator = query_split[1]
        value = query_split[2]

        nodes = base_graph.nodes

        graph = filter.filter_graph(attribute, operator, value, nodes)

        load_plugins.visualize(visualisers, current_visualizer, graph, request)
    except:
        load_plugins.visualize(visualisers, current_visualizer, base_graph, request)

    return render(request, "index.html", {'visualisers': visualisers, 'loaders': loaders, 'workspaces': workspaces})



def load_relationships_of_vertex(request, id):
    tree = apps.get_app_config('application').tree
    if id == "favicon.ico":
        return
    id, option = id.split(";")

    if option == "select":
        if (id.isnumeric()):
            id = int(id)
        print(id)
        node = tree.find_node_by_vertex_id(id)
        node.open()
        node.open_parents()
        tree.last_opened = node.id
        tree_view_html = render_to_string(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "templates", "treeView.html")), {'tree': tree})

        return HttpResponse(tree_view_html)

    elif option == "open":
        node = tree.find_tree_node(int(id))
        if node.opened:
            if len(node.children) != 0:
                node.close()
            if node.parent:
                tree.last_opened = node.parent.id
        else:
            node.open()
            tree.last_opened = node.id

        tree_view_html = render_to_string(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "templates", "treeView.html")), {'tree': tree})

        return HttpResponse(tree_view_html)
    else:
        return redirect("index")

