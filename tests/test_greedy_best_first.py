# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.greedy_best_first import GreedyBestFirstSearch
from jupyddl.heuristics import BasicHeuristic


def test_greedy_best_first_basic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    gbfs = GreedyBestFirstSearch(apla, heuristic.compute)
    assert gbfs.init.h_cost == heuristic.compute(apla.initial_state)


def test_greedy_best_first_goal():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    gbfs = GreedyBestFirstSearch(apla, heuristic.compute)
    lastnode, _, _ = gbfs.search()
    assert lastnode and lastnode.parent


def test_greedy_best_first_path_length():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    path, _, _ = apla.greedy_best_first_search()
    assert len(path) > 0


def test_greedy_best_first_path_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    path, _, _ = apla.greedy_best_first_search()
    assert len(path) == 0


def test_greedy_best_first_path_no_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    p, t, c = apla.greedy_best_first_search(heuristic_key="idontexist")
    assert not p and not t and not c



def test_greedy_best_first_hmax():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = GreedyBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)


def test_greedy_best_first_hadd():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = GreedyBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)


def test_greedy_best_first_hmax_sensible_domain():
    apla = AutomatedPlanner(
        "pddl-examples/grid/domain.pddl", "pddl-examples/grid/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = GreedyBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)


def test_greedy_best_first_hadd_sensible_domain():
    apla = AutomatedPlanner(
        "pddl-examples/grid/domain.pddl", "pddl-examples/grid/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = GreedyBestFirstSearch(apla, heuristic.compute)
    assert astar.init.h_cost == heuristic.compute(apla.initial_state)
