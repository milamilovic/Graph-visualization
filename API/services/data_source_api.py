from abc import ABC, abstractmethod


class GraphLoading(ABC):
    @abstractmethod
    def load_graph(self, path: str) -> bool:
        pass
