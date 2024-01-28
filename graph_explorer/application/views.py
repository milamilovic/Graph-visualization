from django.shortcuts import render

from use_cases import load_plugins


# Create your views here.
def index(request):
    visualisers, loaders = load_plugins.load()
    print("Visualisers", visualisers)
    print("Loaders", loaders)
    return render(request, "index.html",{'visualisers': visualisers, 'loaders': loaders})