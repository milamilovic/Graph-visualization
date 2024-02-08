from django.apps import AppConfig

from use_cases.config import CoreConfig


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'
    loaders = []
    visualizers = []
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

    def get_workspaces(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.workspace_instances
