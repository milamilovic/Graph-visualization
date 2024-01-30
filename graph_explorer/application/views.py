from django.shortcuts import render

from use_cases import load_plugins


# Create your views here.
def index(request):
    visualisers, loaders = load_plugins.load()
    print("Visualisers", visualisers)
    print("Loaders", loaders)
    return render(request, "index.html",{'visualisers': visualisers, 'loaders': loaders})


def load_data_source(request):
    visualisers, loaders = load_plugins.load()

    if request.method == 'POST':
        selected_parser = request.POST.get('parser')
        print("Selected parser:", selected_parser)
        load_plugins.load_data_source(loaders, selected_parser)

    return render(request, "index.html",{'visualisers': visualisers, 'loaders': loaders})
