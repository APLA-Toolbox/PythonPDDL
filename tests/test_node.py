# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.node import Node


def test_node_equality_cost():
    apla = AutomatedPlanner(
        "pddl-examples/tsp/domain.pddl", "pddl-examples/tsp/problem.pddl"
    )
    actions = apla.available_actions(apla.initial_state)
    next_state = apla.transition(apla.initial_state, actions[0])
    next_node = Node(next_state, apla, heuristic_based=True)
    next_node_v2 = Node(next_state, apla)

    assertion = next_node_v2 < next_node
    assertion2 = next_node < next_node_v2

    assert assertion and assertion2


def test_node_equality_no_cost():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    actions = apla.available_actions(apla.initial_state)
    next_state = apla.transition(apla.initial_state, actions[0])
    next_node = Node(next_state, apla, heuristic_based=True)
    next_node_v2 = Node(next_state, apla)

    assertion = next_node_v2 < next_node
    assertion2 = next_node < next_node_v2

    assert assertion and assertion2
