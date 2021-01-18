# -*- coding: utf-8 -*-

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner


def test_parsing():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    assert str(apla.problem) != "" and str(apla.domain) != ""


def test_available_actions():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    actions = apla.available_actions(apla.initial_state)
    assert len(actions) > 0


def test_execute_action():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    actions = apla.available_actions(apla.initial_state)
    new_state = apla.transition(apla.initial_state, actions[0])
    assert str(new_state) != str(apla.initial_state)


def test_state_has_term():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    is_goal = apla.state_has_term(apla.initial_state, apla.goals[0])
    assert not is_goal


def test_state_assertion():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    assert not apla.satisfies(apla.problem.goal, apla.initial_state)


def test_bfs():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    path, metrics = apla.breadth_first_search()
    plan = apla.get_actions_from_path(path)
    plan_state = apla.get_state_def_from_path(path)
    assert plan and plan_state and metrics.n_opened > 0


def test_dfs():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    path, metrics = apla.depth_first_search()
    plan = apla.get_actions_from_path(path)
    plan_state = apla.get_state_def_from_path(path)
    assert plan and plan_state and metrics.n_opened > 0


def test_dij():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    path, metrics = apla.dijktra_best_first_search()
    plan = apla.get_actions_from_path(path)
    plan_state = apla.get_state_def_from_path(path)
    assert plan and plan_state and metrics.n_opened > 0


def test_astar():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    path, metrics = apla.astar_best_first_search()
    plan = apla.get_actions_from_path(path)
    plan_state = apla.get_state_def_from_path(path)
    assert plan and plan_state and metrics.n_opened > 0
