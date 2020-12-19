from .modules import loading_bar_handler
from .state import State

UI = False

if UI:
    loading_bar_handler(False)
import julia

_ = julia.Julia(compiled_modules=False)

if UI:
    loading_bar_handler(True)

from julia import PDDL


class AutomatedPlanning:
    def __init__(self, domain_path, problem_path):
        self.domain = PDDL.load_domain(domain_path)
        self.problem = PDDL.load_problem(problem_path)
        self.initial_state = PDDL.initialize(self.problem)

    def __execute_action(self, action, state):
        return PDDL.execute(action, state)

    def transition(self, state, action):
        return PDDL.transition(self.domain, state, action, check=False)
        
    def available_actions(self, state):
        return PDDL.available(state, self.domain)

    def satisfies(self, asserted_state, state):
        return PDDL.satisfy(asserted_state, state, self.domain)[0]

    def __retrace_path(self, state):
        path = []
        while state.parent:
            path.append(state)
            state = state.parent
        path.reverse()
        return path

    def get_actions_from_path(self, path):
        actions = []
        for state in path:
            actions.append(state.parent_action)
        return actions

    def get_state_def_from_path(self, path):
        trimmed_path = []
        for state in path:
            trimmed_path.append(state.description)
        return trimmed_path

    def breadth_first_search(self):
        visited = []
        init = State(self.initial_state)
        queue = [init]
        while queue:
            current_state = queue.pop(0)
            if current_state not in visited:
                visited.append(current_state)

                if self.satisfies(self.problem.goal, current_state.description):
                    path = self.__retrace_path(current_state)
                    return path
                
                actions = self.available_actions(current_state.description)
                for act in actions:
                    child = State(self.transition(current_state.description, act), act, current_state)
                    if child in visited:
                        continue
                    queue.append(child)

        print("-/!\- No path found -/!\-")
        return []

if __name__ == "__main__":
    ap = AutomatedPlanning("..data/domain.pddl", "..data/problem.pddl")
