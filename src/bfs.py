from .node import Node
import logging


class BreadthFirstSearch:
    def __init__(self, automated_planner):
        self.visited = []
        self.automated_planner = automated_planner
        self.init = Node(self.automated_planner.initial_state, automated_planner)
        self.queue = [self.init]

    def search(self):
        while self.queue:
            current_node = self.queue.pop(0)
            if current_node not in self.visited:
                self.visited.append(current_node)

                if self.automated_planner.satisfies(
                    self.automated_planner.problem.goal, current_node.state
                ):
                    return current_node

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
                    self.queue.append(child)
        logging.warning("!!! No path found !!!")
        return None
