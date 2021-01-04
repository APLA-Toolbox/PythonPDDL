from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .dijkstra import DijkstraBestFirstSearch
from .a_star import AStarBestFirstSearch
from .heuristics import BasicHeuristic, DeleteRelaxationHeuristic
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
        self.domain_path = domain_path
        self.problem_path = problem_path
        self.domain = self.pddl.load_domain(domain_path)
        self.problem = self.pddl.load_problem(problem_path)
        self.initial_state = self.pddl.initialize(self.problem)
        self.goals = self.__flatten_goal()
        self.available_heuristics = [
            "basic/zero",
            "basic/goal_count",
            "delete_relaxation/h_add",
            "delete_relaxation/h_max",
        ]

        # Logger
        self.__init_logger(log_level)
        self.logger = logging.getLogger("automated_planning")
        coloredlogs.install(level=log_level)

        # Running external Julia functions once to create the routes
        self.__run_julia_once()

    def __run_julia_once(self):
        self.satisfies(self.problem.goal, self.initial_state)
        self.state_has_term(self.initial_state, self.goals[0])
        actions = self.available_actions(self.initial_state)
        self.transition(self.initial_state, actions[0])

    def __init_logger(self, log_level):
        import os

        if not os.path.exists("logs"):
            os.makedirs("logs")
        logging.basicConfig(
            filename="logs/main.log",
            format="%(levelname)s:%(message)s",
            filemode="w",
            level=log_level,
        )

    def display_available_heuristics(self):
        print(self.available_heuristics)

    def transition(self, state, action):
        return self.pddl.transition(self.domain, state, action, check=False)

    def available_actions(self, state):
        try:
            return self.pddl.available(state, self.domain)
        except (RuntimeError, TypeError, NameError):
            self.logger.warning("Runtime, Type or Name error occured when fetching available action from state" + str(state))
            return []

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

    def breadth_first_search(self):
        bfs = BreadthFirstSearch(self)
        last_node, total_time, opened_nodes = bfs.search()
        path = self.__retrace_path(last_node)

        return path, total_time, opened_nodes

    def depth_first_search(self):
        dfs = DepthFirstSearch(self)
        last_node, total_time, opened_nodes = dfs.search()
        path = self.__retrace_path(last_node)

        return path, total_time, opened_nodes

    def dijktra_best_first_search(self):
        dijkstra = DijkstraBestFirstSearch(self)
        last_node, total_time, opened_nodes = dijkstra.search()
        path = self.__retrace_path(last_node)

        return path, total_time, opened_nodes

    def astar_best_first_search(self, heuristic_key="basic/goal_count"):
        if "basic" in heuristic_key:
            heuristic = BasicHeuristic(self, heuristic_key)
        elif "delete_relaxation" in heuristic_key:
            heuristic = DeleteRelaxationHeuristic(self, heuristic_key)
        else:
            logging.fatal("Not yet implemented")
            return [], 0, 0
        astar = AStarBestFirstSearch(self, heuristic.compute)
        last_node, total_time, opened_nodes = astar.search()
        path = self.__retrace_path(last_node)

        return path, total_time, opened_nodes
