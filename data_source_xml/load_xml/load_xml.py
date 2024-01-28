from services.data_source_api import GraphLoading


class XmlLoader(GraphLoading):
    def identifier(self):
        return 'xml_loader'

    def name(self):
        return 'XML loader'

    def load_graph(self, path: str) -> bool:
        pass