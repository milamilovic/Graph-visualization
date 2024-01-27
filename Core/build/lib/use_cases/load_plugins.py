import pkg_resources


def load():
    plugins = []
    for ep in pkg_resources.iter_entry_points(group='visualizer'):
        print(ep)
        p = ep.load()
        print("Loading plugin ...{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)

    for ep in pkg_resources.iter_entry_points(group='loader'):
        print(ep)
        p = ep.load()
        print("Loading plugin ...{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)

    return plugins
