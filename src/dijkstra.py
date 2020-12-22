from .heuristics import zero_heuristic
from .node import Node
import logging
import math
from datetime import datetime as timestamp
from time import time as now


class DijkstraBestFirstSearch:
    def __init__(self, automated_planner):
        self.automated_planner = automated_planner
        self.init = Node(
            self.automated_planner.initial_state,
            automated_planner,
            is_closed=False,
            is_open=True,
            heuristic=zero_heuristic,
        )
        self.open_nodes_n = 1
        self.nodes = dict()
        self.nodes[self.__hash(self.init)] = self.init

    def __hash(self, node):
        sep = ", Dict{Symbol,Any}"
        string = str(node.state)
        return string.split(sep, 1)[0] + ")"

    def search(self):
        self.automated_planner.logger.debug(
            "Search started at: " + str(timestamp.now())
        )
        time_start = now()
        while self.open_nodes_n > 0:
            current_key = min(
                [n for n in self.nodes if self.nodes[n].is_open],
                key=(lambda k: self.nodes[k].f_cost),
            )
            current_node = self.nodes[current_key]

            if self.automated_planner.satisfies(
                self.automated_planner.problem.goal, current_node.state
            ):
                computation_time = now() - time_start
                self.automated_planner.logger.debug(
                    "Search finished at: " + str(timestamp.now())
                )
                return current_node, computation_time

            current_node.is_closed = True
            current_node.is_open = False
            self.open_nodes_n -= 1

            actions = self.automated_planner.available_actions(current_node.state)
            for act in actions:
                child = Node(
                    state=self.automated_planner.transition(current_node.state, act),
                    automated_planner=self.automated_planner,
                    parent_action=act,
                    parent=current_node,
                    heuristic=zero_heuristic,
                    is_closed=False,
                    is_open=True,
                )
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
        computation_time = now() - time_start
        self.automated_planner.logger.warning("!!! No path found !!!")
        return None, computation_time
