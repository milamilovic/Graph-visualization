import configparser
import importlib
import pickle

from services.data_source_api import GraphLoading
from services.visualiser_api import GraphVisualisation

from models.tree import Forest, TreeNode


class CoreConfig:
    loader_instances = []
    visualizer_instances = []
    base_graph = None
    current_graph = None
    current_visualizer = None
    tree = None
    config_file_path = 'config.pkl'

    def _init_(self):
        self.load_saved_instances()

    def ready(self):

        self.loader_instances = [GraphLoading]
        self.visualizer_instances = [GraphVisualisation]

        # loaded_plugins = load()
        #
        # self.loader_instances = loaded_plugins[1]
        # print("Loader instances")
        # print(self.loader_instances)
        # self.visualizer_instances = loaded_plugins[0]
        #
        # self.save_instances()

    def save_instances(self):
        with open(self.config_file_path, 'wb+') as file:
            data = {
                'loader_instances': self.loader_instances,
                'visualizer_instances': self.visualizer_instances,
                'base_graph': self.base_graph,
                'current_visualizer': self.current_visualizer,
                "tree": self.tree
            }
            pickle.dump(data, file)

    def load_saved_instances(self):
        try:
            with open(self.config_file_path, 'rb+') as file:
                data = pickle.load(file)

                self.loader_instances = data.get('loader_instances', [])
                self.visualizer_instances = data.get('visualizer_instances', [])
                self.base_graph = data.get('base_graph', None)
                self.current_visualizer = data.get('current_visualizer', None)
                self.tree = data.get('tree', None)
        except(EOFError):
            pass
        except (FileNotFoundError):
            self.loader_instances = []
            self.visualizer_instances = []

    def setGraph(self, graph_instance):
        self.base_graph = graph_instance
        self.save_instances()

    def set_current_visualizer(self, visualizer):
        self.current_visualizer = visualizer
        self.save_instances()

    def set_plugin(self, l, v):
        # loaded_plugins = load()
        #
        self.loader_instances = l
        print("Loader instances")
        print(self.loader_instances)
        self.visualizer_instances = v
        #
        self.save_instances()

    def load_tree(self):
        self.tree = Forest(None)
        for vertex in find_root_vertices(self.current_graph.find_subgraphs()):
            self.tree.roots.append(TreeNode(vertex, None, "vertex"))


def find_root_vertices(subgraphs):
    roots = []
    for graph in subgraphs:
        if graph.is_graph_directed():
            contour_nodes = graph.find_conture_nodes()
            hanging_nodes = graph.find_not_destination_vertices()
            roots += merge_lists_distinct(contour_nodes, hanging_nodes)
        else:
            if graph.has_cycle_undirected():
                if len(graph.vertices) > 0:
                    roots.append(graph.vertices[0])
            else:
                for v in graph.vertices:
                    if v.degree() <= 1:
                        roots.append(v)
    return roots


def merge_lists_distinct(first_list, second_list):
    for i in first_list:
        if i not in second_list:
            second_list.append(i)
    return second_list
