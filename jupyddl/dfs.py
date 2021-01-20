from .node import Node
from datetime import datetime as timestamp
from time import time as now
from .metrics import Metrics


class DepthFirstSearch:
    def __init__(self, automated_planner):
        self.time_start = now()
        self.visited = []
        self.automated_planner = automated_planner
        self.init = Node(self.automated_planner.initial_state, automated_planner)
        self.stack = [self.init]
        self.metrics = Metrics()

    def search(self, node_bound=float("inf")):
        self.automated_planner.logger.debug(
            "Search started at: " + str(timestamp.now())
        )
        while self.stack:
            current_node = self.stack.pop()
            if current_node not in self.visited:
                self.visited.append(current_node)
                self.metrics.n_evaluated += 1
                if self.automated_planner.satisfies(
                    self.automated_planner.problem.goal, current_node.state
                ):
                    self.metrics.runtime = now() - self.time_start
                    self.automated_planner.logger.debug(
                        "Search finished at: " + str(timestamp.now())
                    )
                    self.metrics.total_cost = current_node.g_cost
                    return current_node, self.metrics

                if self.metrics.n_opened > node_bound:
                    break

                actions = self.automated_planner.available_actions(current_node.state)
                if not actions:
                    self.metrics.deadend_states += 1
                else:
                    self.metrics.n_expended += 1
                for act in actions:
                    child = Node(
                        state=self.automated_planner.transition(
                            current_node.state, act
                        ),
                        automated_planner=self.automated_planner,
                        parent_action=act,
                        parent=current_node,
                    )
                    self.metrics.n_generated += 1
                    if child in self.visited:
                        continue
                    self.metrics.n_opened += 1
                    self.stack.append(child)
        self.metrics.runtime = now() - self.time_start
        self.automated_planner.logger.warning("!!! No path found !!!")
        return None, self.metrics
