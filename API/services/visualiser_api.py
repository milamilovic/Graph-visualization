from abc import abstractmethod

from services.service_base_api import ServiceBase


class GraphVisualisation(ServiceBase):
    @abstractmethod
    def visualize(self, graph, request):
        pass