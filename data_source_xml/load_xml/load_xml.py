from services.data_source_api import GraphLoading

from Core.models.graph import Graph


class XmlLoader(GraphLoading):
    def identifier(self):
        return 'xml_loader'

    def name(self):
        return 'XML loader'

    def load_graph(self, path: str) -> Graph:
        pass