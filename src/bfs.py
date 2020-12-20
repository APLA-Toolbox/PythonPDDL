from .node import Node

class BreadthFirstSearch():
    def __init__(self, automated_planer):
        self.visited = []
        self.automated_planer = automated_planer
        self.init = Node(self.automated_planer.initial_state, automated_planer)
        self.queue = [self.init]
    
    def search(self):
        while self.queue:
            current_node = self.queue.pop(0)
            if current_node not in self.visited:
                self.visited.append(current_node)

                if self.automated_planer.satisfies(self.automated_planer.problem.goal, current_node.state):
                    return current_node
                
                actions = self.automated_planer.available_actions(current_node.state)
                for act in actions:
                    child = Node(state=self.automated_planer.transition(current_node.state, act), automated_planer=self.automated_planer, parent_action=act, parent=current_node)
                    if child in self.visited:
                        continue
                    self.queue.append(child)
        print("!!! No path found !!!")
        return None
