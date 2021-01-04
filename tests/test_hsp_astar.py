# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.heuristics import DeleteRelaxationHeuristic

# def test_astar_hmax():
#     apla = AutomatedPlanner(
#         "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
#     )
#     heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
#     astar = AStarBestFirstSearch(apla, heuristic.compute)
#     assert astar.init.h_cost == heuristic.compute(apla.initial_state)


# def test_astar_hadd():
#     apla = AutomatedPlanner(
#         "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
#     )
#     heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
#     astar = AStarBestFirstSearch(apla, heuristic.compute)
#     assert astar.init.h_cost == heuristic.compute(apla.initial_state)

def test_astar_hmax_sensible_domain():
    apla = AutomatedPlanner(
        "pddl-examples/grid/domain.pddl", "pddl-examples/grid/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)


def test_astar_hadd_sensible_domain():
    apla = AutomatedPlanner(
        "pddl-examples/grid/domain.pddl", "pddl-examples/grid/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)
