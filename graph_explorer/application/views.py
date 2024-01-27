from django.shortcuts import render

from use_cases import load_plugins


# Create your views here.
def index(request):
    plugins = load_plugins.load()
    print(plugins)
    return render(request, "index.html",{})