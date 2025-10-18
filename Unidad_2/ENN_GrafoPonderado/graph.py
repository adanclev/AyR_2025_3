import random as rand

class Node:
    def __init__(self, id):
        self.id = id
        self.adjacents = {} # { id: weight, ... }

    def add_adjacent(self, node_id, weight=1):
        self.adjacents[node_id] = weight

    def __repr__(self):
        return f"Node({self.id}, adjacents={self.adjacents})"

    def __str__(self):
        return f"Node {self.id} -> {self.adjacents}"

class Graph:
    def __init__(self, n_vertices, max_weight, prob_path):
        self.n = n_vertices
        self.max_weight = max_weight
        self.p = prob_path
        self.nodes = []
        #rand.seed(9)

    def create_graph(self):
        ids = [chr(65 + i) for i in range(self.n)]  # ['A', 'B', 'C', ...]
        self.nodes = [Node(id) for id in ids]

        for i in range(self.n):
            node = self.nodes[i]
            for j in range(self.n):
                adjacent_node = self.nodes[j]
                condition = i != j and not ids[i] in adjacent_node.adjacents

                if condition and rand.random() < self.p:
                    weight = rand.randint(1, self.max_weight)
                    node.add_adjacent(ids[j], weight)

                    adjacent_node.add_adjacent(ids[i], weight)

    def get_nodes(self):
        return self.nodes

    def get_node(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def __str__(self):
        return "\n".join(str(node) for node in self.nodes)


if __name__ == "__main__":
    g = Graph(n_vertices=5, max_weight=10, prob_path=0.4)
    g.create_graph()
    print(g)

    nodos = g.get_nodes()
    print(nodos)

    print(nodos[0].id, nodos[0].adjacents)

# Cantidad de nodos, c/nodo tendra: costo, id, adjacents
# Grafo: Matriz de adyacencia/costos