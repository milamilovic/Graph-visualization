from django.apps import AppConfig

from use_cases.config import CoreConfig

from models.tree import Forest, TreeNode


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'
    loaders = []
    visualizers = []
    tree = None
    core_instance = None

    def ready(self):
        self.core_instance = CoreConfig()
        self.core_instance.ready()
        # self.loaders = core_instance.loader_instances
        # self.visualizers = core_instance.visualizer_instances

    def get_base_graph(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.base_graph

    def get_plugins(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.loader_instances, self.core_instance.visualizer_instances

    def get_current_visualizer(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.current_visualizer

    def load_tree(self):
        self.tree = Forest(None)
        for vertex in find_root_vertices(self.get_base_graph().find_subgraphs()):
            self.tree.roots.append(TreeNode(vertex, None, "vertex"))


def find_root_vertices(subgraphs):
    roots = []
    for graph in subgraphs:
        if graph.is_graph_directed():
            contour_nodes = graph.find_conture_nodes()
            hanging_nodes = graph.find_not_destination_nodes()
            roots += merge_lists_distinct(contour_nodes, hanging_nodes)

        else:
            if graph.has_cycle_undirected():
                if len(graph.nodes) > 0:
                    roots.append(graph.nodes[0])
            else:
                for node in graph.nodes:
                    if len(node.edges) <= 1:
                        roots.append(node)

    return roots


def merge_lists_distinct(first_list, second_list):
    for i in first_list:
        if i not in second_list:
            second_list.append(i)

    return second_list