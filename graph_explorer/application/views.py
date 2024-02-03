from django.shortcuts import render
from django.apps.registry import apps
from use_cases import load_plugins


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
    # visualisers = apps.get_app_config('application').visualizers

    if request.method == 'POST':
        # selected_parser = request.POST.get('parser')
        # print("Selected parser:", selected_parser)
        # load_plugins.load_data_source(loaders, selected_parser)
        selected_parser = request.POST.get('parser')
        selected_visualizer = request.POST.get('visualizer')
        selected_file = request.POST.get('file')
        print("\n\n\n\n\n\n\n\n\n")
        print("Selected parser:", selected_parser)
        print("Selected visualizer:", selected_visualizer)
        print("Selected file:", selected_file)
        load_plugins.load_data_source(loaders, visualisers, selected_parser, selected_visualizer, selected_file)
        # apps.get_app_config('core').base_graph = graph
        print("BASE GRAPHHHHH")
        graph = apps.get_app_config('application').get_base_graph()
        print("VIEWS", len(graph.nodes))
    return render(request, "index.html",{'visualisers': visualisers, 'loaders': loaders})
