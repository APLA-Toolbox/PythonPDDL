# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.heuristics import DeleteRelaxationHeuristic


def test_astar_delete_relaxation():
    apla = AutomatedPlanner(
        "pddl-examples/tsp/domain.pddl", "pddl-examples/tsp/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    astar.search()
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)
