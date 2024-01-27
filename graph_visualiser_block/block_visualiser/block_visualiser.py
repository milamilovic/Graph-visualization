from services.visualiser_api import GraphVisualisation


class BlockVisualiser(GraphVisualisation):

    def identifier(self):
        return "block_visualiser"

    def name(self):
        return "Block view"

    def visualize(self, graph, request):
        pass