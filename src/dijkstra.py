from .node import Node
import math

class DijkstraBestFirstSearch():
    def __init__(self, automated_planning, pddl):
        self.automated_planning = automated_planning
        self.init = Node(self.automated_planning.initial_state, pddl, is_closed=False, is_open=True)
        self.goal = Node(self.automated_planning.problem.goal, pddl, is_closed=False, is_open=False, g_cost=math.inf)
        self.PDDL = pddl
        self.open_nodes_n = 1
        self.nodes = dict()
        self.nodes[self.init.uuid] = self.init

    def search(self):
        while self.open_nodes_n > 0:
            current_key = min([n for n in self.nodes if self.nodes[n].is_open], key=(lambda  k: self.nodes[k].f_cost))
            current_state = self.nodes[current_key]

            if self.automated_planning.satisfies(self.automated_planning.problem.goal, current_state.description):
                    return current_state
        print("-/!\- No path found -/!\-")
        return []
