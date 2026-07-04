"""Parser and tokenizer tests."""

from __future__ import annotations

import pytest

from jupyddl.parser import (
    UnsupportedFeatureError,
    parse,
    parse_domain_file,
    parse_problem_file,
    tokenize,
)
from jupyddl.parser.ast import Domain, Problem

from conftest import paths

DOMAIN = """
(define (domain gripper)
  (:requirements :strips :typing :negative-preconditions)
  (:types room ball)
  (:predicates (at ?b - ball ?r - room) (free) (holding ?b - ball))
  (:action pick
    :parameters (?b - ball ?r - room)
    :precondition (and (at ?b ?r) (free) (not (holding ?b)))
    :effect (and (holding ?b) (not (free)) (not (at ?b ?r))))
)
"""

PROBLEM = """
(define (problem g1) (:domain gripper)
  (:objects b1 - ball rooma roomb - room)
  (:init (at b1 rooma) (free))
  (:goal (and (at b1 roomb))))
"""


def test_tokenize_handles_comments_and_nesting():
    tokens = tokenize("(define ; comment\n (domain d) (:predicates (p ?x)))")
    assert tokens[0] == "define"
    assert ["domain", "d"] in tokens


def test_tokenize_unbalanced_raises():
    from jupyddl.parser.ast import PDDLError

    with pytest.raises(PDDLError):
        tokenize("(define (domain d)")


def test_parse_domain_structure():
    dom = parse(DOMAIN)
    assert isinstance(dom, Domain)
    assert dom.name == "gripper"
    assert ":negative-preconditions" in dom.requirements
    assert dom.types == {"room": "object", "ball": "object"}
    action = {a.name: a for a in dom.actions}["pick"]
    # Positive and negative literals separated correctly.
    assert any(lit.positive for lit in action.precondition.literals)
    assert any(not lit.positive for lit in action.precondition.literals)


def test_parse_problem_structure():
    prob = parse(PROBLEM)
    assert isinstance(prob, Problem)
    assert prob.domain_name == "gripper"
    assert ("b1", "ball") in prob.objects
    assert len(prob.init) == 2


def test_quantified_goal_captured():
    dom, prob = paths("flip")
    problem = parse_problem_file(prob)
    assert problem.goal.universals, "forall goal should be captured as a universal"


def test_numeric_fluent_is_unsupported():
    dom, _ = paths("grid")
    with pytest.raises(UnsupportedFeatureError):
        parse_domain_file(dom)


def test_disjunction_unsupported():
    with pytest.raises(UnsupportedFeatureError):
        parse(
            "(define (domain d) (:predicates (p) (q))"
            " (:action a :precondition (or (p) (q)) :effect (p)))"
        )
