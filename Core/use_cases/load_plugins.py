import os

import pkg_resources


def load():
    visualisers = []
    loaders = []

    for ep in pkg_resources.iter_entry_points(group='visualizer'):
        print(ep)
        p = ep.load()
        print("Loading plugin ...{} {}".format(ep.name, p))
        plugin = p()
        visualisers.append(plugin)

    for ep in pkg_resources.iter_entry_points(group='loader'):
        print(ep)
        p = ep.load()
        print("Loading plugin ...{} {}".format(ep.name, p))
        plugin = p()
        loaders.append(plugin)

    return visualisers, loaders


def load_data_source(loaders, visualizers, selected_data_source, selected_visualizer, request):
    for p in loaders:
        if p.identifier() == "json_loader":
            graph = p.load_graph("../data/json/movies.json")
            visualize(visualizers, selected_visualizer, graph, request)


def visualize(visualisers, selected_visualizer, graph, request):
    for v in visualisers:
        if v.identifier() == selected_visualizer:
            path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "../../../../graph_explorer/application/templates", "mainView.html"))
            with open(path, 'w') as file:
                file.write(v.visualize(graph, request))