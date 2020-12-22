from .node import Node
from datetime import datetime as timestamp
from time import time as now


class DepthFirstSearch:
    def __init__(self, automated_planner):
        self.visited = []
        self.automated_planner = automated_planner
        self.init = Node(self.automated_planner.initial_state, automated_planner)
        self.stack = [self.init]

    def search(self):
        time_start = now()
        self.automated_planner.logger.debug(
            "Search started at: " + str(timestamp.now())
        )
        while self.stack:
            current_node = self.stack.pop(0)
            if current_node not in self.visited:
                self.visited.append(current_node)

                if self.automated_planner.satisfies(
                    self.automated_planner.problem.goal, current_node.state
                ):
                    computation_time = now() - time_start
                    self.automated_planner.logger.debug(
                        "Search finished at: " + str(timestamp.now())
                    )
                    return current_node, computation_time

                actions = self.automated_planner.available_actions(current_node.state)
                for act in actions:
                    child = Node(
                        state=self.automated_planner.transition(
                            current_node.state, act
                        ),
                        automated_planner=self.automated_planner,
                        parent_action=act,
                        parent=current_node,
                    )
                    if child in self.visited:
                        continue
                    self.stack.append(child)
        computation_time = now() - time_start
        self.automated_planner.logger.warning("!!! No path found !!!")
        return None, computation_time
