# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.heuristics import DeleteRelaxationHeuristic, BasicHeuristic

def test_astar_basic():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)

def test_astar_delete_relaxation():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)

def test_astar_goal():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    path, _, _ = astar.search()
    assert heuristic.compute(path[-1].state) == 0


def test_astar_path_length():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    path, _, _ = apla.astar_best_first_search()
    assert len(path) > 0
