from PyQt5.QtCore import QThread, pyqtSignal
from config import N_SECTIONS, MAX_COST, MAX_PATHS, STATES, MAX_IT_SIN_MEJORA, INTERVAL
from node import Node
import time
import random as rand
import copy

class SapoThread(QThread):
    Signal = pyqtSignal(list, tuple)
    # [[(cost, state), ...], ...], (best, current)

    def __init__(self, n_sections=N_SECTIONS, max_paths=MAX_PATHS, max_cost=MAX_COST):
        super().__init__()
        self.running = True
        self.n_sections = n_sections
        self.max_paths = max_paths
        self.max_cost = max_cost

    def run(self):
        sections_og = self.create_paths()
        min_cost, min_paths = self.get_min_cost_and_paths(sections_og)
        print("====================================")
        print(f"Mejor Costo: {min_cost}")
        print("Caminos Óptimos:")
        for index, camino in enumerate(min_paths):
            print(str(index+1) +  ". " + str(camino))
        print("====================================")

        it_sin_mejora = 0
        best_race = 9999

        while self.running and it_sin_mejora < MAX_IT_SIN_MEJORA:
            it = 0
            offset = 1
            current_total_cost = 0
            sections = copy.deepcopy(sections_og)

            self.update_graph(sections, best=best_race, current=current_total_cost)
            time.sleep(INTERVAL)

            previous_costs = [(0, 0) for _ in range(N_SECTIONS)] # [(prev cost, last path), ...]
            while it < N_SECTIONS:
                section = sections[it]
                random_idx = rand.randrange(len(section)) # pos path
                selected_path = section[random_idx]
                checked = self.anyone_open(section)
                while checked and selected_path.closed:
                    random_idx = rand.randrange(len(section))
                    selected_path = section[random_idx]

                if not checked:
                    for path in section:
                        path.toggle_closed_state()
                    it = it - 1
                    offset = offset - 1
                    self.update_graph(sections,
                                      idx_section=it+offset,
                                      idx_path=previous_costs[it][1],
                                      best=best_race,
                                      current=current_total_cost
                                      )
                    time.sleep(INTERVAL)
                    self.update_graph(sections,
                                      idx_section=it+offset-1,
                                      best=best_race,
                                      current=current_total_cost
                                      )
                    current_total_cost = previous_costs[it][0]
                    time.sleep(INTERVAL)
                    continue

                selected_path.toggle_closed_state()
                current_total_cost += selected_path.cost

                self.update_graph(sections,
                                  idx_section=it+offset,
                                  idx_path=random_idx,
                                  best=best_race,
                                  current=current_total_cost
                                  )

                time.sleep(INTERVAL)

                if current_total_cost <= best_race:
                    previous_costs[it] = (current_total_cost - selected_path.cost, random_idx)
                    it = it + 1
                    offset = offset + 1
                    self.update_graph(sections,
                                      idx_section=it+offset-1,
                                      best=best_race,
                                      current=current_total_cost
                                      )
                else:
                    current_total_cost -= selected_path.cost
                    self.update_graph(sections,
                                      idx_section=it+offset-1,
                                      best=best_race,
                                      current=current_total_cost
                                      )

                time.sleep(INTERVAL)

            if current_total_cost == best_race:
                it_sin_mejora += 1
            elif current_total_cost < best_race:
                best_race = current_total_cost
                it_sin_mejora = 0

        print(f"Mejor Costo encontrado: {best_race}")
        print("Caminos tomados:")
        #print(previous_costs)
        for index, camino in enumerate(previous_costs):
            print(str(index + 1) + ". " + str(sections_og[index][camino[1]]))
        print("====================================")
        self.stop()

    def stop(self):
        self.running = False
        self.wait()  # Espera a que el hilo termine

    def create_paths(self):
        sections = list()
        for _ in range(self.n_sections):
            n_paths = rand.randint(1, self.max_paths)
            paths = [Node(rand.randint(1, self.max_cost)) for _ in range(n_paths)]
            sections.append(paths)

        return sections

    def anyone_open(self, paths, idx=0):
        if not paths[idx].closed:
            return True

        if idx < len(paths) - 1:
            return self.anyone_open(paths, idx + 1)

        return False

    def get_min_cost(self, sections):
        min_cost = 0
        for section in sections:
            min_cost += min([path.cost for path in section])

        return min_cost

    def get_min_cost_and_paths(self, sections):
        total_min_cost = 0
        min_cost_path_indices = []

        for section in sections:
            min_cost_path = min(section, key=lambda path: path.cost)
            total_min_cost += min_cost_path.cost
            #print(min_cost_path)

            #min_index = section.index(min_cost_path)
            min_cost_path_indices.append(min_cost_path)

        return total_min_cost, min_cost_path_indices

    def create_graph_levels(self, sections, idx_section, idx_path):
        graph_levels = list()
        for section in sections:
            graph_levels.append([(0 ,STATES.get("AVAILABLE", 0))])  # Inicio / descanso [(cost, state), ...]
            graph_levels.append([(path.cost, STATES.get("BLOCKED", 0) if path.closed else STATES.get("AVAILABLE",0))
                          for path in section])

        graph_levels.append([(0 ,STATES.get("AVAILABLE", 0))])  # Meta [(cost, state), ...]

        cost, _ = graph_levels[idx_section][idx_path]
        graph_levels[idx_section][idx_path] = (cost, STATES.get("SELECTED", 0))

        return graph_levels

    def update_graph(self, sections, idx_section=0, idx_path=0, best=9999, current=0):
        new_list = self.create_graph_levels(sections, idx_section, idx_path)
        self.Signal.emit(new_list, (best, current))

    def timeout(self):
        pass

# Necesito
# idx de [section, path] para saber la posición del sapo

# cuando regresa despues de una seccion completa no se ve bien, se coloca en el nuevo camino que tomo de repente