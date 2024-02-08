import configparser
import importlib
import pickle

from services.data_source_api import GraphLoading
from services.visualiser_api import GraphVisualisation


class CoreConfig:
    loader_instances = []
    visualizer_instances = []
    workspace_instances = {}
    current_workspace = None
    base_graph = None
    current_graph = None
    current_visualizer = None
    config_file_path = 'config.pkl'


    def _init_(self):
        self.load_saved_instances()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CoreConfig, cls).__new__(cls)
        return cls.instance

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
                'workspace_instances': self.workspace_instances,
                'current_workspace': self.current_workspace
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
                self.workspace_instances = data.get('workspace_instances', {})
                self.current_workspace = data.get('current_workspace', None)

        except(EOFError):
            pass
        except (FileNotFoundError):
            pass

    def setGraph(self, graph_instance):
        self.base_graph = graph_instance
        self.save_instances()

    def set_current_visualizer(self, visualizer):
        self.current_visualizer = visualizer
        self.save_instances()

    def set_current_workspace(self, workspace):
        self.current_workspace = workspace
        self.save_instances()

    def set_workspace_graph(self, key, graph):
        for k in self.workspace_instances:
            if int(k) == int(key):
                self.workspace_instances[k] = graph
                break
        else:
            self.workspace_instances[key] = graph

        self.save_instances()

    def set_plugin(self, l, v):
        # loaded_plugins = load()
        #
        self.loader_instances = l
        print("Loader instances")
        print(self.loader_instances)
        self.visualizer_instances = v
        self.save_instances()

    def add_workspace(self, key, graph):
        self.workspace_instances[key] = graph
        print("WORKSPACE", self.workspace_instances)
        self.save_instances()
