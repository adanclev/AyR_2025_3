import random as rand
import copy
from node import Node
from config import N_SECTIONS, MAX_COST, MAX_PATHS, MAX_IT_SIN_MEJORA

def show_paths(caminos):
    for lista_nodos in enumerate(caminos):
        print("Camino " + str(lista_nodos[0] + 1) + " c/" + str(len(lista_nodos[1])))
        for nodo in lista_nodos[1]:
            print(nodo, end=" ")
        print()

def create_paths(n, max_paths, max_cost):
    sections = list()
    for _ in range(n):
        n_paths = rand.randint(1, max_paths)
        paths = [Node(rand.randint(1, max_cost)) for _ in range(n_paths)]
        sections.append(paths)

    return sections

def anyone_open(paths, idx=0):
    if not paths[idx].closed:
        return True

    if idx < len(paths)-1:
        return anyone_open(paths, idx + 1)

    return False

def get_min_cost(sections):
    min_cost = 0
    for section in sections:
        min_cost += min([path.cost for path in section])

    return min_cost

def get_min_cost_and_paths(sections):
    total_min_cost = 0
    min_cost_path_indices = []

    for section in sections:
        min_cost_path = min(section, key=lambda path: path.cost)
        total_min_cost += min_cost_path.cost
        print(min_cost_path)

        min_index = section.index(min_cost_path)
        min_cost_path_indices.append(min_index)

    return total_min_cost, min_cost_path_indices

if __name__ == '__main__':
    rand.seed(5) # 9

    sections_og = create_paths(n=N_SECTIONS, max_paths=MAX_PATHS, max_cost=MAX_COST)
    min_cost, min_paths = get_min_cost_and_paths(sections_og)
    print(min_cost, min_paths)

    it_sin_mejora = 0

    best_race = 9999
    smth = 0

    while it_sin_mejora < MAX_IT_SIN_MEJORA:
        smth += 1
        it = 0 # idx section
        current_total_cost = 0
        sections = copy.deepcopy(sections_og)
        previous_costs = [0 for _ in range(N_SECTIONS)]
        while it < N_SECTIONS:
            section = sections[it]
            random_idx = rand.randrange(len(section)) # idx path
            selected_path = section[random_idx]
            checked = anyone_open(section)
            while checked and selected_path.closed:
                selected_path = rand.choice(section)

            if not checked:
                for path in section:
                    path.toggle_closed_state()
                it = it - 1
                current_total_cost = previous_costs[it]
                continue

            selected_path.toggle_closed_state()
            current_total_cost += selected_path.get_cost()

            if current_total_cost <= best_race:
                previous_costs[it] = current_total_cost - selected_path.get_cost()
                it = it + 1
            else: current_total_cost -= selected_path.get_cost()

        if current_total_cost == best_race:
            it_sin_mejora += 1
        elif current_total_cost < best_race:
            best_race = current_total_cost
            it_sin_mejora = 0

    show_paths(sections_og)
    print(best_race)
    print(smth)
