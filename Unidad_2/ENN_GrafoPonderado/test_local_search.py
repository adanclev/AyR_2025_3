from graph import Graph
import random as rand

def initial_path(nodes, start, end): # ([Node, ...], Node, Node)
    solution = nodes.copy()
    solution.remove(start)
    solution.remove(end)
    n = rand.randint(0, len(solution))
    if n == 0:
        return [start, end]
    middle_path = rand.sample(solution, n)
    return [start] + middle_path + [end]

def initial(nodes, start_node):
    keys = list(start_node.adjacents.keys())
    chosen_node_id = rand.choice(keys)
    chosen_node = nodes.get_node(chosen_node_id)
    return [start_node] + [chosen_node]

def select_start_end_nodes(graph):
    n = len(graph.nodes)
    start_node = rand.randrange(n)  # returns integer
    end_node = rand.randrange(n)
    while end_node == start_node:
        end_node = rand.randrange(n)

    return graph.nodes[start_node], graph.nodes[end_node]

def evaluation(solution):
    weight = 0
    for i in range(len(solution)-1):
        node = solution[i]

        adjacent_node = solution[i+1].id
        if adjacent_node in node.adjacents:
            weight += node.adjacents.get(adjacent_node)
        else:
            return None

    return weight

def neighborhood(nodes, current_path):
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

def vecindario2(current_path):
    """
    Genera todos los caminos vecinos posibles usando el operador de Intercambio 2-Opt.
    Asume que el camino tiene al menos 4 nodos (start, medio, medio, end).
    """

    # La parte que no cambia son los nodos inicial y final.
    # El 2-Opt se aplica a los nodos intermedios.
    middle_path = current_path[1:-1]
    n = len(middle_path)

    # Necesitamos al menos dos nodos intermedios para un swap o 2-opt
    if n < 2:
        return []

    new_middle_path = middle_path[:]
    idx1 = rand.randint(0, n - 1)
    idx2 = rand.randint(0, n - 1)
    while idx1 == idx2:
        idx2 = rand.randint(0, n - 1)

    temp = new_middle_path[idx1]
    new_middle_path[idx1] = new_middle_path[idx2]
    new_middle_path[idx2] = temp

    return [current_path[0]] + new_middle_path + [current_path[-1]]

if __name__ == "__main__":
    max_it = 50
    it = 0
    graph = Graph(6, 15, 0.4)
    graph.create_graph()
    print(graph, end='\n\n')

    start_node, end_node = select_start_end_nodes(graph)
    print("Nodo inicio: " + str(start_node))
    print("Nodo fin: " + str(end_node))

    path = initial_path(graph.nodes, start_node, end_node)
    temp_weight = evaluation(path)
    best_weight = 9999 if temp_weight is None else temp_weight
    best_path = None if temp_weight is None else path

    print(f"\nSolución inicial (Costo: {best_weight}):")
    print(" -> ".join([n.id for n in path]), end='\n\n')

    while it < max_it:
        it += 1
        path = neighborhood(graph.nodes, path)
        temp_weight = evaluation(path)

        if temp_weight is not None and temp_weight < best_weight:
            best_path = path
            best_weight = temp_weight
            print(f"Iteración {it}: Mejora encontrada. Nuevo mejor peso: {best_weight}")

    if best_path:
        print(f"\nMejor camino encontrado (Costo: {best_weight}):")
        print(" -> ".join([n.id for n in best_path]))
    else:
        print("\nNo se pudo encontrar un camino válido.")

