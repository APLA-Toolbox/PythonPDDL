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
    heuristic = hs.zero_heuristic(apla.initial_state, apla)
    assert heuristic == 0


def test_goal_count_heuristic():
    apla = AutomatedPlanner(
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
    )
    heuristic = hs.goal_count_heuristic(apla.initial_state, apla)
    assert heuristic == 1
