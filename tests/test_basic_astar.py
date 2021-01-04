# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.heuristics import BasicHeuristic


def test_astar_basic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)


def test_astar_goal():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    lastnode, _, _ = astar.search()
    assert lastnode and lastnode.parent


def test_astar_path_length():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    path, _, _ = apla.astar_best_first_search()
    assert len(path) > 0


def test_astar_path_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    path, _, _ = apla.astar_best_first_search()
    assert len(path) == 0


def test_astar_path_no_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    p, t, c = apla.astar_best_first_search(heuristic_key="idontexist")
    assert not p and not t and not c
