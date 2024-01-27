from services.visualiser_api import GraphVisualisation


class SimpleVisualiser(GraphVisualisation):

    def identifier(self):
        return 'simple_visualiser'

    def name(self):
        return 'Simple view'

    def visualize(self, graph, request):
        pass