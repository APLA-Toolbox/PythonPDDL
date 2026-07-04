"""Heuristic tests: admissibility, dominance, goal/dead-end behaviour."""

from __future__ import annotations

import math

import pytest

from jupyddl.api import build_task
from jupyddl.heuristics import HEURISTICS, make_heuristic

from conftest import OPTIMAL_COST, STRIPS_SOLVABLE, paths

ADMISSIBLE = ["blind", "hmax", "h1", "h2", "lmcut"]


@pytest.mark.parametrize("name", STRIPS_SOLVABLE)
@pytest.mark.parametrize("hname", ADMISSIBLE)
def test_admissible_heuristics_never_overestimate(name, hname, examples_available):
    task = build_task(*paths(name))
    value = make_heuristic(hname, task)(task.init)
    assert value <= OPTIMAL_COST[name] + 1e-9, f"{hname} on {name}: {value}"


@pytest.mark.parametrize("name", STRIPS_SOLVABLE)
def test_h1_equals_hmax(name, examples_available):
    task = build_task(*paths(name))
    assert (
        abs(
            make_heuristic("h1", task)(task.init)
            - make_heuristic("hmax", task)(task.init)
        )
        < 1e-9
    )


@pytest.mark.parametrize("name", STRIPS_SOLVABLE)
def test_lmcut_dominates_hmax(name, examples_available):
    task = build_task(*paths(name))
    lmcut = make_heuristic("lmcut", task)(task.init)
    hmax = make_heuristic("hmax", task)(task.init)
    assert lmcut >= hmax - 1e-9


@pytest.mark.parametrize("hname", sorted(HEURISTICS))
def test_zero_in_goal_state(hname, examples_available):
    task = build_task(*paths("blocksworld"))
    heuristic = make_heuristic(hname, task)
    goal_state = task.init | task.goals  # relaxed goal-satisfying state
    assert task.goal_reached(goal_state)
    assert heuristic(goal_state) == 0


def test_deadend_detected_as_infinite(examples_available):
    # The broken vehicle instance has an unreachable goal fact.
    task = build_task(*paths("vehicle"))
    assert math.isinf(make_heuristic("hmax", task)(task.init))
    assert math.isinf(make_heuristic("lmcut", task)(task.init))


def test_goalcount_counts_open_goals(examples_available):
    task = build_task(*paths("pallet"))
    gc = make_heuristic("goalcount", task)
    assert gc(task.init) == len(task.goals - task.init)
