from .modules import loading_bar_handler
from .bfs import BreadthFirstSearch
from .dijkstra import DijkstraBestFirstSearch

loading_bar_handler(False)
import julia
_ = julia.Julia(compiled_modules=False)
loading_bar_handler(True)
from julia import PDDL
from time import time as now


class AutomatedPlanner:
    def __init__(self, domain_path, problem_path):
        self.pddl = PDDL
        self.domain = self.pddl.load_domain(domain_path)
        self.problem = self.pddl.load_problem(problem_path)
        self.initial_state = self.pddl.initialize(self.problem)

    def __execute_action(self, action, state):
        return self.pddl.execute(action, state)

    def transition(self, state, action):
        return self.pddl.transition(self.domain, state, action, check=False)

    def available_actions(self, state):
        return self.pddl.available(state, self.domain)

    def satisfies(self, asserted_state, state):
        return self.pddl.satisfy(asserted_state, state, self.domain)[0]

    def __retrace_path(self, node):
        if not node:
            return []
        path = []
        while node.parent:
            path.append(node)
            node = node.parent
        path.reverse()
        return path

    def get_actions_from_path(self, path):
        if not path:
            print("Path is empty, can't operate...")
            return []
        actions = []
        for node in path:
            actions.append((node.parent_action, node.g_cost))

        cost = self.pddl.get_value(path[-1].state, "total-cost")
        if not cost:
            return actions
        else:
            return (actions, cost)

    def get_state_def_from_path(self, path):
        if not path:
            print("Path is empty, can't operate...")
            return []
        trimmed_path = []
        for node in path:
            trimmed_path.append(node.state)
        return trimmed_path

    def breadth_first_search(self, time_it=False):
        if time_it:
            start_time = now()
        bfs = BreadthFirstSearch(self)
        last_node = bfs.search()
        if time_it:
            total_time = now() - start_time
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        else:
            return path, None

    def dijktra_best_first_search(self, time_it=False):
        if time_it:
            start_time = now()
        dijkstra = DijkstraBestFirstSearch(self)
        last_node = dijkstra.search()
        if time_it:
            total_time = now() - start_time
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        else:
            return path, None


if __name__ == "__main__":
    ap = AutomatedPlanner("..data/domain.pddl", "..data/problem.pddl")
