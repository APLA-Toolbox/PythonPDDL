from .node import Node
import logging
import math
from time import time as now
from datetime import datetime as timestamp
from .metrics import Metrics


class AStarBestFirstSearch:
    def __init__(self, automated_planner, heuristic_function):
        self.time_start = now()
        self.automated_planner = automated_planner
        self.metrics = Metrics()
        self.init = Node(
            self.automated_planner.initial_state,
            automated_planner,
            is_closed=False,
            is_open=True,
            heuristic=heuristic_function,
            heuristic_based=True,
            metric=self.metrics,
        )
        self.heuristic_function = heuristic_function
        self.open_nodes_n = 1
        self.nodes = dict()
        self.nodes[self.__hash(self.init)] = self.init

    def __hash(self, node):
        sep = ", Dict{Symbol,Any}"
        string = str(node.state)
        return string.split(sep, 1)[0] + ")"

    def search(self, node_bound=float("inf")):
        self.automated_planner.logger.debug(
            "Search started at: " + str(timestamp.now())
        )
        while self.open_nodes_n > 0:
            current_key = min(
                [n for n in self.nodes if self.nodes[n].is_open],
                key=(lambda k: self.nodes[k].f_cost),
            )
            current_node = self.nodes[current_key]

            self.metrics.n_evaluated += 1
            if self.automated_planner.satisfies(
                self.automated_planner.problem.goal, current_node.state
            ):
                self.metrics.runtime = now() - self.time_start
                self.automated_planner.logger.debug(
                    "Search finished at: " + str(timestamp.now())
                )
                return current_node, self.metrics

            current_node.is_closed = True
            current_node.is_open = False
            self.open_nodes_n -= 1

            if self.metrics.n_opened > node_bound:
                break

            actions = self.automated_planner.available_actions(current_node.state)
            if actions:
                self.metrics.n_expended += 1
            else:
                self.metrics.deadend_states += 1
            for act in actions:
                child = Node(
                    state=self.automated_planner.transition(current_node.state, act),
                    automated_planner=self.automated_planner,
                    parent_action=act,
                    parent=current_node,
                    heuristic=self.heuristic_function,
                    is_closed=False,
                    is_open=True,
                    heuristic_based=True,
                    metric=self.metrics,
                )
                self.metrics.n_generated += 1
                child_hash = self.__hash(child)
                if child_hash in self.nodes:
                    if self.nodes[child_hash].is_closed:
                        continue
                    if not self.nodes[child_hash].is_open:
                        self.nodes[child_hash] = child
                        self.open_nodes_n += 1
                        self.metrics.n_opened += 1
                    else:
                        if child.g_cost < self.nodes[child_hash].g_cost:
                            self.nodes[child_hash] = child
                            self.open_nodes_n += 1
                            self.metrics.n_opened += 1
                            self.metrics.n_reopened += 1

                else:
                    self.nodes[child_hash] = child
                    self.open_nodes_n += 1
                    self.metrics.n_opened += 1
        self.metrics.runtime = now() - self.time_start
        self.automated_planner.logger.warning("!!! No path found !!!")
        return None, self.metrics
