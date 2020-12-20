from .node import Node
import math
from .heuristics import zero_heuristic

class DijkstraBestFirstSearch():
    def __init__(self, automated_planer):
        self.automated_planer = automated_planer
        self.init = Node(self.automated_planer.initial_state, automated_planer, is_closed=False, is_open=True)
        self.open_nodes_n = 1
        self.nodes = dict()
        self.nodes[self.__hash(self.init)] = self.init

    def __hash(self, node):
        sep = ", Dict{Symbol,Any}"
        string = str(node.state)
        return string.split(sep, 1)[0] + ")"

    def search(self):
        while self.open_nodes_n > 0:
            current_key = min([n for n in self.nodes if self.nodes[n].is_open], key=(lambda  k: self.nodes[k].f_cost))
            current_node = self.nodes[current_key]

            if self.automated_planer.satisfies(self.automated_planer.problem.goal, current_node.state):
                    return current_node

            current_node.is_closed = True
            current_node.is_open = False
            self.open_nodes_n -= 1
            
            actions = self.automated_planer.available_actions(current_node.state)
            for act in actions:
                child = Node(state=self.automated_planer.transition(current_node.state, act), automated_planer=self.automated_planer, parent_action=act, parent=current_node, heuristic=zero_heuristic, is_closed=False, is_open=True)
                child_hash = self.__hash(child)
                if child_hash in self.nodes:
                    if self.nodes[child_hash].is_closed:
                        continue
                    if not self.nodes[child_hash].is_open:
                        self.nodes[child_hash] = child
                        self.open_nodes_n += 1
                    else:
                        if child.g_cost < self.nodes[child_hash].g_cost:
                            self.nodes[child_hash] = child
                            self.open_nodes_n += 1

                else:
                    self.nodes[child_hash] = child
                    self.open_nodes_n += 1
        print("!!! No path found !!!")
        return None
