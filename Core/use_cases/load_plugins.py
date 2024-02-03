import os

import pkg_resources
from use_cases.config import CoreConfig

cc = CoreConfig()

def load():
    visualisers = []
    loaders = []
    # cc = CoreConfig()

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

    cc.set_plugin(loaders, visualisers)
    return visualisers, loaders



def load_data_source(loaders, visualizers, selected_data_source, selected_visualizer, path, request):
    graph = None
    # cc = CoreConfig()
    for l in loaders:
        print(selected_data_source)
        if l.identifier() == selected_data_source:
            graph = l.load_graph(path)
            cc.setGraph(graph)
            print(graph)
            print("LOAD",len(graph.nodes))

    visualize(visualizers, selected_visualizer, graph, request)

def visualize(visualisers, selected_visualizer, graph, request):
    for v in visualisers:
        if v.identifier() == selected_visualizer:
            path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "../../../../graph_explorer/application/templates", "mainView.html"))
            with open(path, 'w') as file:
                file.write(v.visualize(graph, request))

