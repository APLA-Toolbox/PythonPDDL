from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .dijkstra import DijkstraBestFirstSearch
from .a_star import AStarBestFirstSearch
from .heuristics import goal_count_heuristic, zero_heuristic
import coloredlogs
import logging
import julia
_ = julia.Julia(compiled_modules=False, debug=False)
from julia import PDDL
from time import time as now

logging.getLogger("julia").setLevel(logging.WARNING)


class AutomatedPlanner:
    def __init__(self, domain_path, problem_path, log_level="DEBUG"):
        # Planning Tool
        self.pddl = PDDL
        self.domain = self.pddl.load_domain(domain_path)
        self.problem = self.pddl.load_problem(problem_path)
        self.initial_state = self.pddl.initialize(self.problem)
        self.goals = self.__flatten_goal()
        self.available_heuristics = dict()
        self.available_heuristics["goal_count"] = goal_count_heuristic
        self.available_heuristics["zero"] = zero_heuristic

        # Logger
        self.__init_logger(log_level)
        self.logger = logging.getLogger("automated_planning")
        coloredlogs.install(level=log_level)
    
    def __init_logger(self, log_level):
        import os
        if not os.path.exists('logs'):
            os.makedirs('logs')
        logging.basicConfig(
            filename="logs/main.log",
            format="%(levelname)s:%(message)s",
            filemode="w",
            level=log_level,
        )  # Creates the log file

    def transition(self, state, action):
        return self.pddl.transition(self.domain, state, action, check=False)

    def available_actions(self, state):
        return self.pddl.available(state, self.domain)

    def satisfies(self, asserted_state, state):
        return self.pddl.satisfy(asserted_state, state, self.domain)[0]

    def state_has_term(self, state, term):
        if self.pddl.has_term_in_state(self.domain, state, term):
            return True
        return False

    def __flatten_goal(self):
        return self.pddl.flatten_goal(self.problem)

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
            self.logger.warning("Path is empty, can't operate...")
            return []
        actions = []
        for node in path:
            actions.append((node.parent_action, node.g_cost))

        cost = self.pddl.get_value(path[-1].state, "total-cost")
        if not cost:
            return actions
        return (actions, cost)

    def get_state_def_from_path(self, path):
        if not path:
            self.logger.warning("Path is empty, can't operate...")
            return []
        trimmed_path = []
        for node in path:
            trimmed_path.append(node.state)
        return trimmed_path

    def breadth_first_search(self, time_it=False):
        bfs = BreadthFirstSearch(self)
        last_node, total_time = bfs.search()
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        return path, None

    def depth_first_search(self, time_it=False):
        dfs = DepthFirstSearch(self)
        last_node, total_time = dfs.search()
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        return path, None

    def dijktra_best_first_search(self, time_it=False):
        dijkstra = DijkstraBestFirstSearch(self)
        last_node, total_time = dijkstra.search()
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        return path, None

    def astar_best_first_search(self, time_it=False, heuristic=goal_count_heuristic):
        astar = AStarBestFirstSearch(self, heuristic)
        last_node, total_time = astar.search()
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        return path, None
