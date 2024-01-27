import pkg_resources


def load():
    visualizers = []
    for ep in pkg_resources.iter_entry_points(group='visualizer'):
        print(ep)
        p = ep.load()
        print("Loading plugin ...{} {}".format(ep.name, p))
        plugin = p()
        visualizers.append(plugin)
    """loaders = []
    for l in apps.get_app_config('core').loaders:
        loaders.append({"name": l.name(), "identifier": l.identifier()})"""
    return visualizers
