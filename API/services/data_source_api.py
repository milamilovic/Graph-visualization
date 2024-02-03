from abc import abstractmethod

from services.service_base_api import ServiceBase


class GraphLoading(ServiceBase):
    @abstractmethod
    def load_graph(self, path: str):
        pass
