"""Shared pytest fixtures and constants for the jupyddl test suite."""

from __future__ import annotations

import os

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(REPO_ROOT, "pddl-examples")

# Known optimal costs for the example instances (validated across BFS, Dijkstra
# and A* with an admissible heuristic).
OPTIMAL_COST = {
    "blocksworld": 2,
    "dinner": 1,
    "flip": 3,
    "pallet": 12,
    "switch": 3,
    "tsp": 15,
}

# Solvable instances without conditional effects (relaxation heuristics are
# admissible on these). ``flip`` is solvable but uses conditional effects.
STRIPS_SOLVABLE = ["blocksworld", "dinner", "pallet", "switch", "tsp"]
SOLVABLE = STRIPS_SOLVABLE + ["flip"]
UNSOLVABLE = ["vehicle"]  # broken example data (typos): goal unreachable
UNSUPPORTED = ["grid"]  # numeric fluents, out of scope


def paths(name: str):
    folder = os.path.join(EXAMPLES, name)
    return os.path.join(folder, "domain.pddl"), os.path.join(folder, "problem.pddl")


@pytest.fixture(scope="session")
def examples_available():
    if not os.path.isdir(EXAMPLES) or not os.listdir(EXAMPLES):
        pytest.skip("pddl-examples submodule not initialised")
    return EXAMPLES
