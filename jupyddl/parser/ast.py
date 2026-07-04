"""Structured AST for the supported subset of PDDL.

The subset covered: ``:strips``, ``:typing``, ``:negative-preconditions``,
``:equality``, ``:action-costs`` (via ``(increase (total-cost) k)``), and the
ADL constructs ``forall``/``when`` inside effects (needed by e.g. the *flip*
domain). Numeric fluents other than ``total-cost`` are intentionally not
modelled and are rejected by the parser with a clear error.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class PDDLError(Exception):
    """Base class for all parsing / modelling errors."""


class UnsupportedFeatureError(PDDLError):
    """Raised when a PDDL construct outside the supported subset is used."""


@dataclass(frozen=True)
class Atom:
    """A (possibly lifted) predicate application, e.g. ``(on ?x ?y)``.

    ``args`` holds terms as raw strings: variables keep their leading ``?``
    while constants/objects are stored verbatim.
    """

    predicate: str
    args: tuple[str, ...] = ()

    def __str__(self) -> str:
        if not self.args:
            return f"({self.predicate})"
        return f"({self.predicate} {' '.join(self.args)})"


@dataclass(frozen=True)
class Literal:
    """A positive or negative atom used in preconditions and goals."""

    atom: Atom
    positive: bool = True


@dataclass(frozen=True)
class EqualityConstraint:
    """An ``(= a b)`` (or its negation) constraint over terms."""

    left: str
    right: str
    positive: bool = True


@dataclass
class Condition:
    """A conjunction of literals plus (in)equality constraints.

    All supported preconditions/goals/effect-conditions are conjunctive; the
    parser flattens nested ``and`` and rejects unsupported connectives.
    """

    literals: list[Literal] = field(default_factory=list)
    equalities: list[EqualityConstraint] = field(default_factory=list)
    # Universally-quantified sub-conditions, expanded over objects at grounding
    # time. Each entry is (params, body) where params is [(var, type), ...].
    universals: list[tuple[list[tuple[str, str]], "Condition"]] = field(
        default_factory=list
    )


# --- Effects -----------------------------------------------------------------
# Effects are kept as a small tree; grounding expands ``forall`` and normalises
# everything into (condition -> add/delete) conditional effects.


@dataclass
class AddEffect:
    atom: Atom


@dataclass
class DelEffect:
    atom: Atom


@dataclass
class IncreaseCostEffect:
    amount: int


@dataclass
class ConjunctiveEffect:
    parts: list = field(default_factory=list)


@dataclass
class ForallEffect:
    params: list[tuple[str, str]]  # (variable, type)
    body: object


@dataclass
class WhenEffect:
    condition: Condition
    body: object


# --- Domain / problem --------------------------------------------------------


@dataclass
class Predicate:
    name: str
    params: list[tuple[str, str]]  # (variable, type)


@dataclass
class Action:
    name: str
    parameters: list[tuple[str, str]]  # (variable, type)
    precondition: Condition
    effect: object  # one of the *Effect nodes above


@dataclass
class Domain:
    name: str
    requirements: list[str]
    types: dict[str, str]  # child type -> parent type ("object" if none)
    constants: list[tuple[str, str]]  # (name, type)
    predicates: list[Predicate]
    actions: list[Action]
    functions: list[str] = field(default_factory=list)


@dataclass
class Problem:
    name: str
    domain_name: str
    objects: list[tuple[str, str]]  # (name, type)
    init: list[Atom]
    goal: Condition
    metric_minimize_cost: bool = False
