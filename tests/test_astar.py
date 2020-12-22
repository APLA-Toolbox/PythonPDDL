# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.automated_planner import AutomatedPlanner
from src.a_star import AStarBestFirstSearch


def test_astar_init():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    astar = AStarBestFirstSearch(apla, apla.available_heuristics["goal_count"])
    assert astar.init.h_cost == apla.available_heuristics["goal_count"](apla.initial_state, apla)

def test_astar_goal():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    path, _ = apla.astar_best_first_search()
    assert apla.available_heuristics["goal_count"](path[-1], apla) == 0

def test_astar_path_length():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    path, _ = apla.astar_best_first_search()
    assert len(path) > 0
