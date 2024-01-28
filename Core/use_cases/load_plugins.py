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
