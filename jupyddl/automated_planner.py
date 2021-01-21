from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .dijkstra import DijkstraBestFirstSearch
from .a_star import AStarBestFirstSearch
from .greedy_best_first import GreedyBestFirstSearch
from .metrics import Metrics
from .heuristics import (
    BasicHeuristic,
    DeleteRelaxationHeuristic,
    RelaxedCriticalPathHeuristic,
    CriticalPathHeuristic,
)
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
            "relaxed_critical_path/1",
            "relaxed_critical_path/2",
            "relaxed_critical_path/3",
            "critical_path/1",
            "critical_path/2",
            "critical_path/3",
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
        if actions:
            self.transition(self.initial_state, actions[0])
            return
        logging.warning(
            "No actions from initial state, a path probably (definitely) won't be found"
        )

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
            self.logger.warning(
                "Runtime, Type or Name error occured when fetching available action from state"
                + str(state)
            )
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
            if not node.parent_action:
                break
            act = str(node.parent_action).replace("<PyCall.jlwrap ", "")
            cost = "total-cost = " + str(node.g_cost)
            actions.append((act, cost))

        return actions

    def __stringify_state(self, state):
        state_str = str(state).replace("<PyCall.jlwrap PDDL.State(", "")
        state_str = state_str.replace("Set(Julog.Term[", "")
        state_str = state_str.replace("])", "")
        state_str = state_str.replace(
            'Dict{Symbol,Any}(Symbol("total-cost") =>', "total-cost ="
        )
        state_str = state_str.replace("))>", "")
        return state_str

    def get_state_def_from_path(self, path):
        if not path:
            self.logger.warning("Path is empty, can't operate...")
            return []
        trimmed_path = []
        for node in path:
            state = self.__stringify_state(node.state)
            trimmed_path.append(state)
        return trimmed_path

    def breadth_first_search(self, node_bound=float("inf")):
        bfs = BreadthFirstSearch(self)
        last_node, metrics = bfs.search(node_bound=node_bound)
        path = self.__retrace_path(last_node)

        return path, metrics

    def depth_first_search(self, node_bound=float("inf")):
        dfs = DepthFirstSearch(self)
        last_node, metrics = dfs.search(node_bound=node_bound)
        path = self.__retrace_path(last_node)

        return path, metrics

    def dijktra_best_first_search(self, node_bound=float("inf")):
        dijkstra = DijkstraBestFirstSearch(self)
        last_node, metrics = dijkstra.search(node_bound=node_bound)
        path = self.__retrace_path(last_node)

        return path, metrics

    def astar_best_first_search(
        self, node_bound=float("inf"), heuristic_key="basic/goal_count"
    ):
        if "basic" in heuristic_key:
            heuristic = BasicHeuristic(self, heuristic_key)
        elif "delete_relaxation" in heuristic_key:
            heuristic = DeleteRelaxationHeuristic(self, heuristic_key)
        elif "relaxed_critical_path" in heuristic_key:
            heuristic = RelaxedCriticalPathHeuristic(self, int(heuristic_key[-1]))
        elif "critical_path" in heuristic_key:
            heuristic = CriticalPathHeuristic(self, int(heuristic_key[-1]))
        else:
            logging.fatal("Not yet implemented")
            return [], Metrics()
        astar = AStarBestFirstSearch(self, heuristic.compute)
        last_node, metrics = astar.search(node_bound=node_bound)
        path = self.__retrace_path(last_node)

        return path, metrics

    def greedy_best_first_search(
        self, node_bound=float("inf"), heuristic_key="basic/goal_count"
    ):
        if "basic" in heuristic_key:
            if "zero" in heuristic_key:
                self.logger.warning(
                    "Forced heuristic to goal_count. Zero isn't a proper heuristic for Greedy Best First."
                )
            heuristic = BasicHeuristic(self, "basic/goal_count")
        elif "delete_relaxation" in heuristic_key:
            heuristic = DeleteRelaxationHeuristic(self, heuristic_key)
        elif "relaxed_critical_path" in heuristic_key:
            logging.warning("Relaxed Critical Path is deficient for H^2 and H^3")
            heuristic = RelaxedCriticalPathHeuristic(self, int(heuristic_key[-1]))
        elif "critical_path" in heuristic_key:
            heuristic = CriticalPathHeuristic(self, int(heuristic_key[-1]))
        else:
            logging.fatal("Not yet implemented")
            return [], Metrics()
        greedy = GreedyBestFirstSearch(self, heuristic.compute)
        last_node, metrics = greedy.search(node_bound=node_bound)
        path = self.__retrace_path(last_node)

        return path, metrics
