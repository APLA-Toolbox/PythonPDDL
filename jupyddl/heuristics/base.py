"""Heuristic base class."""

from __future__ import annotations


class Heuristic:
    """A heuristic bound to a task; call it on a state to get an estimate.

    Returning ``math.inf`` signals that the state is a (relaxed) dead end.
    """

    name: str = "heuristic"
    admissible: bool = False

    def __init__(self, task):
        self.task = task

    def __call__(self, state: frozenset) -> float:  # pragma: no cover
        raise NotImplementedError
