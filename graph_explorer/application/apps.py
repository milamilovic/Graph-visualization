from django.apps import AppConfig

from use_cases.config import CoreConfig

from models.tree import Forest, TreeNode


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'
    loaders = []
    visualizers = []
    tree = None
    core_instance = None

    def ready(self):
        self.core_instance = CoreConfig()
        self.core_instance.ready()
        # self.loaders = core_instance.loader_instances
        # self.visualizers = core_instance.visualizer_instances

    def get_base_graph(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.base_graph

    def get_plugins(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.loader_instances, self.core_instance.visualizer_instances

    def get_current_visualizer(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.current_visualizer

    def get_workspaces(self):
        self.core_instance.load_saved_instances()
        return self.core_instance.workspace_instances

    def load_tree(self):
        # Inicijalizacija novog stabla
        self.tree = Forest(None)

        # Pronalaženje korena za svaki podgraf u glavnom grafu
        for vertex in find_root_vertices(self.get_base_graph().find_subgraphs()):
            # Kreiranje novog čvora stabla sa trenutnim čvorom kao korenom
            self.tree.roots.append(TreeNode(vertex, None, "vertex"))

# Funkcija koja pronalazi korene (čvorove bez roditelja) u podgrafovima
def find_root_vertices(subgraphs):
    roots = []  # Lista za skladištenje korena

    # Iteracija kroz sve podgrafove
    for graph in subgraphs:
        # Provera da li je graf usmeren
        if graph.is_graph_directed():
            # Pronalaženje čvorova konture i čvorova koji nisu odredišni
            contour_nodes = graph.find_conture_nodes()
            hanging_nodes = graph.find_not_destination_nodes()
            # Spajanje listi čvorova, bez ponavljanja istih čvorova
            roots += merge_lists_distinct(contour_nodes, hanging_nodes)
        else:
            # Ako graf nije usmeren
            if graph.has_cycle_undirected():  # Provera da li graf ima ciklus
                # Ako ima ciklus, dodajemo prvi čvor kao koren
                if len(graph.nodes) > 0:
                    roots.append(graph.nodes[0])
            else:
                # Ako nema ciklusa, dodajemo čvorove sa najviše jednom granom kao korene
                for node in graph.nodes:
                    if len(node.edges) <= 1:
                        roots.append(node)

    return roots

# Funkcija koja spaja dve liste, zadržavajući samo jedinstvene elemente
def merge_lists_distinct(first_list, second_list):
    for i in first_list:
        if i not in second_list:
            second_list.append(i)  # Dodavanje elementa ako nije već u listi

    return second_list  # Vraćanje spajane list


