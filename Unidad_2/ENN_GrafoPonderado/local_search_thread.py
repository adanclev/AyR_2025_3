import time

from PyQt5.QtCore import QThread, pyqtSignal
from config import MAX_IT, MAX_WEIGHT, PROB_PATH, N_NODES, NODE_TYPE
from graph import Graph
import random as rand

class LSThread(QThread):
    # [('A', 'start'), ('B', 'end'), ...], (NodoId, node_type)
    # [('A', 'B', 12), ('A', 'F', 3), ...], Edges(Nodo1, Nodo2, peso, selected)
    Graph = pyqtSignal(list, list, int, str)

    def __init__(self, max_it=MAX_IT, n=N_NODES, max_weight=MAX_WEIGHT, p=PROB_PATH):
        super().__init__()
        self.running = True
        self.n = n
        self. max_weight = max_weight
        self.p = p
        self.max_it = max_it

    def update_view(self, nodes, edges=None, best_weight=9999, best_path=""):
        self.Graph.emit(nodes, edges, best_weight, best_path)

    def run(self):
        it = 0
        graph = Graph(self.n, self.max_weight, self.p)
        graph.create_graph()
        print(graph, end='\n\n')

        start_node, end_node = self.select_start_end_nodes(graph)
        print("Nodo inicio: " + str(start_node))
        print("Nodo fin: " + str(end_node))

        _nodes = self.get_nodes_from_graph(graph, start_node, end_node)
        edges = self.get_edges(graph)
        self.update_view(_nodes, edges)

        path = self.initial_path(graph.nodes, start_node, end_node)
        temp_weight = self.evaluation(path)
        best_weight = 9999 if temp_weight is None else temp_weight
        best_path = None if temp_weight is None else path

        print(f"Solución inicial (Costo: {best_weight}):")
        print(" -> ".join([n.id for n in path]), end='\n')

        time.sleep(1)

        while self.running and it < self.max_it:
            it += 1
            path = self.neighborhood(graph.nodes, path)
            temp_weight = self.evaluation(path)

            if temp_weight is not None and temp_weight < best_weight:
                best_path = path
                best_weight = temp_weight
                print(f"Iteración {it}: Mejora encontrada. Nuevo mejor peso: {best_weight}")

        if best_path is not None:
            print(f"\nMejor camino encontrado (Costo: {best_weight}):")
            str_path = " -> ".join([n.id for n in best_path])
            edges = self.get_edges(graph, best_path)

            print(str_path)
        else:
            str_path = "No se encontró un camino válido"
            print("\nNo se pudo encontrar un camino válido.")
        self.update_view(_nodes, edges, best_weight, str_path)
        self.stop()

    def stop(self):
        self.running = False
        self.wait()

    def get_edges(self, graph, path=None):
        if path is not None:
            path_edges = set()
            for i in range(len(path) - 1):
                # sorted para que sea no dirigido
                path_edges.add(tuple(sorted([path[i].id, path[i + 1].id])))

        edges = []
        seen = set()  # Para grafo no dirigido

        for node in graph.nodes:
            for neighbor, weight in node.adjacents.items():
                key = tuple(sorted([node.id, neighbor]))
                if key not in seen:
                    seen.add(key)
                    selected = False if path is None else key in path_edges
                    edges.append((node.id, neighbor, weight, selected))

        return edges

    def get_nodes_from_graph(self, graph, start_node, end_node):
        nodes = list()
        for node in graph.nodes:
            if node.id == start_node.id:
                nodes.append((node.id, NODE_TYPE["START"]))
            elif node.id == end_node.id:
                nodes.append((node.id, NODE_TYPE["END"]))
            else:
                nodes.append((node.id, NODE_TYPE["REGULAR"]))

        return nodes

    def initial_path(self, nodes, start, end):  # ([Node, ...], Node, Node)
        solution = nodes.copy()
        solution.remove(start)
        solution.remove(end)
        n = rand.randint(0, len(solution))
        if n == 0:
            return [start, end]
        middle_path = rand.sample(solution, n)
        return [start] + middle_path + [end]

    def select_start_end_nodes(self, graph):
        n = len(graph.nodes)
        start_node = rand.randrange(n)  # returns integer
        end_node = rand.randrange(n)
        while end_node == start_node:
            end_node = rand.randrange(n)

        return graph.nodes[start_node], graph.nodes[end_node]

    def evaluation(self, solution):
        weight = 0
        for i in range(len(solution)-1):
            node = solution[i]

            adjacent_node = solution[i + 1].id
            if adjacent_node in node.adjacents:
                weight += node.adjacents.get(adjacent_node)
            else:
                return None

        return weight

    def neighborhood(self, nodes, current_path):
        # Cambiar un path por otro
        # Tomar uno random de middle path y cambiarlo por uno que no este en el current path
        if len(current_path) <= 2:
            return current_path
        middle_path = current_path[1:-1]
        set_current_path = set(current_path)
        random_path_idx = rand.randrange(len(middle_path))
        set_current_path.remove(middle_path[random_path_idx])

        new_path = rand.choice(nodes)
        while new_path in set_current_path:
            new_path = rand.choice(nodes)

        middle_path[random_path_idx] = new_path
        return [current_path[0]] + middle_path + [current_path[-1]]