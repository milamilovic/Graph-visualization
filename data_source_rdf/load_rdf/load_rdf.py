from services.data_source_api import GraphLoading


class RDFLoader(GraphLoading):
    def identifier(self):
        return 'rdf_loader'

    def name(self):
        return 'RDF loader'

    def load_graph(self, path: str) -> bool:
        pass