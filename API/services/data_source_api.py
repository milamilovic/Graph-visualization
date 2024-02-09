from abc import abstractmethod

from services.service_base_api import ServiceBase

from models.graph import Graph


class GraphLoading(ServiceBase):
    @abstractmethod

    def load_graph(self, path: str)->Graph:
        pass
