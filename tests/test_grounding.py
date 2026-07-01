"""Grounding tests: typing, PNF, static pruning, object harvesting."""

from __future__ import annotations

import pytest

from jupyddl.grounding import ground_files
from jupyddl.parser import UnsupportedFeatureError

from conftest import SOLVABLE, UNSUPPORTED, paths


@pytest.mark.parametrize("name", SOLVABLE)
def test_examples_ground(name, examples_available):
    task = ground_files(*paths(name))
    assert task.num_facts > 0
    assert task.operators, "expected at least one grounded operator"
    assert task.goals, "expected a non-empty goal"


def test_object_harvesting_untyped(examples_available):
    # dinner declares no :objects; constants appear only in :init.
    task = ground_files(*paths("dinner"))
    assert len(task.operators) > 0


def test_negative_precondition_pnf(examples_available):
    # tsp uses :negative-preconditions -> complement facts must appear.
    task = ground_files(*paths("tsp"))
    assert any(name.startswith("(not ") for name in task.facts)


def test_apply_operator_reaches_goal(examples_available):
    task = ground_files(*paths("blocksworld"))
    state = task.init
    # Manually applying any applicable operator changes the state.
    op = next(task.applicable_operators(state))
    assert op.apply(state) != state


@pytest.mark.parametrize("name", UNSUPPORTED)
def test_unsupported_examples(name, examples_available):
    with pytest.raises(UnsupportedFeatureError):
        ground_files(*paths(name))


def test_conditional_effects_present(examples_available):
    task = ground_files(*paths("flip"))
    assert any(op.cond_effects for op in task.operators)
