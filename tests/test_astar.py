# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.a_star import AStarBestFirstSearch


def test_astar_init():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    astar = AStarBestFirstSearch(apla, apla.available_heuristics["goal_count"])
    assert astar.init.h_cost == apla.available_heuristics["goal_count"](
        apla.initial_state, apla
    )


def test_astar_goal():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    path, _, _ = apla.astar_best_first_search()
    assert apla.available_heuristics["goal_count"](path[-1].state, apla) == 0


def test_astar_path_length():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    path, _, _ = apla.astar_best_first_search()
    assert len(path) > 0
