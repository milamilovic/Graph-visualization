from abc import abstractmethod, ABC


class GraphVisualisation(ABC):
    @abstractmethod
    def visualize(self, graph, request):
        pass