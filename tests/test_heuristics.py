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
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    heuristic = hs.BasicHeuristic(apla, "zero")
    h = heuristic.compute(apla.initial_state)
    assert h == 0


def test_goal_count_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    heuristic = hs.BasicHeuristic(apla, "goal_count")
    h = heuristic.compute(apla.initial_state)
    assert h == 0
