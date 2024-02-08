from use_cases.load_plugins import CoreConfig

from models.graph import Graph

cc = CoreConfig()


def add_workspace():
    counter = len(cc.workspace_instances)
    graph = Graph()
    cc.add_workspace(counter + 1, graph)


def set_current_workspace(workspace):
    cc.set_current_workspace(workspace)
