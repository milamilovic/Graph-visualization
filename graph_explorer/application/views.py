from django.shortcuts import render

from use_cases import load_plugins


# Create your views here.
def index(request):
    visualisers = load_plugins.load()
    print(visualisers)
    return render(request, "index.html",{})