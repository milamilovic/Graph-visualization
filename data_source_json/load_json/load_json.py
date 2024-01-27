from services.data_source_api import GraphLoading


class JsonLoader(GraphLoading):
    def identifier(self):
        return 'json_loader'

    def name(self):
        return 'JSON loader'

    def load_graph(self, path: str) -> bool:
        pass