from .node import Node

class BreadthFirstSearch():
    def __init__(self, automated_planning):
        self.visited = []
        self.automated_planning = automated_planning
        self.init = Node(self.automated_planning.initial_state, automated_planning)
        self.queue = [self.init]
    
    def search(self):
        while self.queue:
            current_node = self.queue.pop(0)
            if current_node not in self.visited:
                self.visited.append(current_node)

                if self.automated_planning.satisfies(self.automated_planning.problem.goal, current_node.state):
                    return current_node
                
                actions = self.automated_planning.available_actions(current_node.state)
                for act in actions:
                    child = Node(state=self.automated_planning.transition(current_node.state, act), automated_planning=self.automated_planning, parent_action=act, parent=current_node)
                    if child in self.visited:
                        continue
                    self.queue.append(child)
        print("-/!\- No path found -/!\-")
        return None
