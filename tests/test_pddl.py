# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def test_automated_planning_parsing():
    import src.pddl

    apla = src.pddl.AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    assert str(apla.problem) != "" and str(apla.domain) != ""


def test_automated_planning_states():
    import src.pddl

    apla = src.pddl.AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    assert str(apla.current_state) == str(apla.initial_state)


def test_automated_planning_state_assertion():
    import src.pddl

    apla = src.pddl.AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    assert apla.satisfies(apla.problem.goal, apla.initial_state, apla.domain) == False
