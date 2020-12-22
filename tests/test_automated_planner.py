# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.automated_planner import AutomatedPlanner


def test_parsing():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    assert str(apla.problem) != "" and str(apla.domain) != ""


def test_available_actions():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    actions = apla.available_actions(apla.initial_state)
    assert len(actions) > 0


def test_execute_action():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    actions = apla.available_actions(apla.initial_state)
    new_state = apla.transition(apla.initial_state, actions[0])
    assert str(new_state) != str(apla.initial_state)


def test_state_has_term():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    is_goal = apla.state_has_term(apla.initial_state, apla.goals[0])
    assert is_goal == False


def test_state_assertion():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    assert apla.satisfies(apla.problem.goal, apla.initial_state) == False
