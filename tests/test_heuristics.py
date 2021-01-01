# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
import jupyddl.heuristics as hs

"""
Testing the heuristics in different situations
To do:
    - Run search algorithms and test value of h when at goal
"""


def test_zero_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = hs.BasicHeuristic(apla, "basic/zero")
    h = heuristic.compute(apla.initial_state)
    assert h == 0


def test_goal_count_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = hs.BasicHeuristic(apla, "basic/goal_count")
    h = heuristic.compute(apla.initial_state)
    assert h != 0


def test_delete_relaxation_add_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/tsp/domain.pddl", "pddl-examples/tsp/problem.pddl"
    )
    heuristic = hs.DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    h = heuristic.compute(apla.initial_state)
    assert h != 0
