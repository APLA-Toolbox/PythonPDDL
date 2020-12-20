# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def test_parsing():
    from src.automated_planning import AutomatedPlanning

    apla = AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    assert str(apla.problem) != "" and str(apla.domain) != ""


def test_available_actions():
    from src.automated_planning import AutomatedPlanning

    apla = AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    actions = apla.available_actions(apla.initial_state)
    assert(len(actions) > 0)

def test_execute_action():
    from src.automated_planning import AutomatedPlanning

    apla = AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    actions = apla.available_actions(apla.initial_state)
    new_state = apla.transition(apla.initial_state, actions[0])
    assert(str(new_state) != str(apla.initial_state))

def test_state_assertion():
    from src.automated_planning import AutomatedPlanning

    apla = AutomatedPlanning("data/domain.pddl", "data/problem.pddl")
    assert apla.satisfies(apla.problem.goal, apla.initial_state) == False
