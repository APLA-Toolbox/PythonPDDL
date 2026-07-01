"""Grounded STRIPS(+conditional-effects) task representation.

A :class:`Task` is a fully grounded planning problem where every fact is an
integer id (for fast set operations). Negative preconditions/goals are compiled
away into *positive normal form* by the grounder, so preconditions and goals are
purely positive sets of fact ids. Conditional effects are retained explicitly so
ADL domains such as *flip* can be solved.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CondEffect:
    """A conditional effect: when ``condition`` holds, apply add/delete."""

    condition: frozenset
    add: frozenset
    delete: frozenset


@dataclass(frozen=True)
class Operator:
    """A grounded action over integer fact ids."""

    name: str
    precond: frozenset
    add: frozenset
    delete: frozenset
    cond_effects: tuple = ()
    cost: int = 1

    def applicable(self, state: frozenset) -> bool:
        return self.precond <= state

    def apply(self, state: frozenset) -> frozenset:
        """Return the successor state (conditions evaluated in ``state``)."""
        dels = set(self.delete)
        adds = set(self.add)
        for ce in self.cond_effects:
            if ce.condition <= state:
                dels |= ce.delete
                adds |= ce.add
        # Adds take precedence over deletes (standard STRIPS semantics).
        return frozenset((state - dels) | adds)


@dataclass
class Task:
    """A grounded planning task."""

    name: str
    facts: tuple  # id -> human-readable fact string
    init: frozenset
    goals: frozenset
    operators: tuple
    metric_cost: bool = False

    @property
    def num_facts(self) -> int:
        return len(self.facts)

    def goal_reached(self, state: frozenset) -> bool:
        return self.goals <= state

    def applicable_operators(self, state: frozenset):
        for op in self.operators:
            if op.precond <= state:
                yield op

    def fact_name(self, fact_id: int) -> str:
        return self.facts[fact_id]

    def state_str(self, state: frozenset) -> str:
        return "{" + ", ".join(sorted(self.facts[f] for f in state)) + "}"

    def relaxed_operators(self):
        """Delete-relaxation operator view used by relaxation heuristics.

        Every conditional effect becomes its own relaxed operator whose
        precondition is the action precondition conjoined with the effect
        condition. This is the standard, sound treatment of conditional effects
        under delete relaxation. Returns a list of ``(precond, add, cost)``.
        """
        relaxed = []
        for op in self.operators:
            if op.add:
                relaxed.append((op.precond, op.add, op.cost))
            for ce in op.cond_effects:
                if ce.add:
                    relaxed.append((op.precond | ce.condition, ce.add, op.cost))
            if not op.add and not op.cond_effects:
                # Keep operators with only delete effects visible (no-op in the
                # relaxation) so nothing downstream assumes non-empty adds.
                relaxed.append((op.precond, frozenset(), op.cost))
        return relaxed
