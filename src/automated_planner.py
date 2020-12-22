from .modules import loading_bar_handler
from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .dijkstra import DijkstraBestFirstSearch
import logging

UI = False

if UI:
    loading_bar_handler(False)
import julia

_ = julia.Julia(compiled_modules=False)

if UI:
    loading_bar_handler(True)

from julia import PDDL
from time import time as now


class AutomatedPlanner:
    def __init__(self, domain_path, problem_path):
        self.pddl = PDDL
        self.domain = self.pddl.load_domain(domain_path)
        self.problem = self.pddl.load_problem(problem_path)
        self.initial_state = self.pddl.initialize(self.problem)
        self.goals = self.__flatten_goal()

    """
    Transition from one state to the next using an action
    """
    def transition(self, state, action):
        return self.pddl.transition(self.domain, state, action, check=False)

    """
    Returns all available actions from the given state 
    """
    def available_actions(self, state):
        return self.pddl.available(state, self.domain)

    """ 
    Check if a vector of terms is satisfied by the given state
    """
    def satisfies(self, asserted_state, state):
        return self.pddl.satisfy(asserted_state, state, self.domain)[0]

    """
    Check if the term is satisfied by the state
    To do: compare if it's faster to compute the check on a vector of terms in julia or python 
    """
    def state_has_term(self, state, term):
        if self.pddl.has_term_in_state(self.domain, state, term):
            return True
        else:
            return False

    """
    Flatten the goal to a vector of terms
    To do: check if we can iterate over the jl vector 
    """
    def __flatten_goal(self):
        return self.pddl.flatten_goal(self.problem)

    """
    Retrieves the linked list path 
    """
    def __retrace_path(self, node):
        if not node:
            return []
        path = []
        while node.parent:
            path.append(node)
            node = node.parent
        path.reverse()
        return path

    """
    Returns all the actions operated to reach the goal 
    """
    def get_actions_from_path(self, path):
        if not path:
            logging.warning("Path is empty, can't operate...")
            return []
        actions = []
        for node in path:
            actions.append((node.parent_action, node.g_cost))

        cost = self.pddl.get_value(path[-1].state, "total-cost")
        if not cost:
            return actions
        else:
            return (actions, cost)

    """
    Returns all the states that should be opened from start to goal 
    """
    def get_state_def_from_path(self, path):
        if not path:
            logging.warning("Path is empty, can't operate...")
            return []
        trimmed_path = []
        for node in path:
            trimmed_path.append(node.state)
        return trimmed_path

    """
    Runs the BFS algorithm on the loaded domain/problem 
    """
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

    """
    Runs the DFS algorithm on the domain/problem 
    """
    def depth_first_search(self, time_it=False):
        if time_it:
            start_time = now()
        dfs = DepthFirstSearch(self)
        last_node = dfs.search()
        if time_it:
            total_time = now() - start_time
        path = self.__retrace_path(last_node)
        if time_it:
            return path, total_time
        else:
            return path, None

    """
    Runs the Dijkstra algorithm on the domain/problem 
    """
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
