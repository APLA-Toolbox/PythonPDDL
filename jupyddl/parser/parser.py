"""Recursive-descent PDDL parser producing :mod:`jupyddl.parser.ast` objects."""

from __future__ import annotations

from .ast import (
    Action,
    AddEffect,
    Atom,
    Condition,
    ConjunctiveEffect,
    DelEffect,
    Domain,
    EqualityConstraint,
    ForallEffect,
    IncreaseCostEffect,
    Literal,
    PDDLError,
    Predicate,
    Problem,
    UnsupportedFeatureError,
    WhenEffect,
)
from .tokenizer import tokenize

_CONNECTIVES = {"and", "or", "not", "imply", "forall", "exists", "when", "="}


def _parse_typed_list(items: list) -> list[tuple[str, str]]:
    """Parse ``?x ?y - type a b`` into ``[(name, type), ...]`` (default type ``object``)."""
    result: list[tuple[str, str]] = []
    pending: list[str] = []
    i = 0
    while i < len(items):
        tok = items[i]
        if tok == "-":
            typ = items[i + 1]
            if isinstance(typ, list):
                raise UnsupportedFeatureError("'either' types are not supported")
            for name in pending:
                result.append((name, typ))
            pending = []
            i += 2
        else:
            if isinstance(tok, list):
                raise PDDLError(f"Unexpected nested list in typed list: {tok}")
            pending.append(tok)
            i += 1
    result.extend((name, "object") for name in pending)
    return result


def _parse_atom(expr: list) -> Atom:
    if not expr or isinstance(expr[0], list):
        raise PDDLError(f"Malformed atom: {expr}")
    for arg in expr[1:]:
        if isinstance(arg, list):
            raise UnsupportedFeatureError(
                f"nested/numeric term in atom is not supported: {expr}"
            )
    return Atom(expr[0], tuple(expr[1:]))


def _flatten_condition(expr, cond: Condition, positive: bool) -> None:
    if not isinstance(expr, list):
        raise PDDLError(f"Malformed condition: {expr}")
    if not expr:  # empty () means "true"
        return
    head = expr[0]
    if head == "and":
        for sub in expr[1:]:
            _flatten_condition(sub, cond, positive)
    elif head == "not":
        if len(expr) != 2:
            raise PDDLError(f"'not' takes exactly one argument: {expr}")
        _flatten_condition(expr[1], cond, not positive)
    elif head == "=":
        cond.equalities.append(EqualityConstraint(expr[1], expr[2], positive))
    elif head == "forall":
        if not positive:
            raise UnsupportedFeatureError("negated 'forall' is not supported")
        cond.universals.append((_parse_typed_list(expr[1]), parse_condition(expr[2])))
    elif head in _CONNECTIVES:
        raise UnsupportedFeatureError(f"'{head}' is not supported in conditions")
    else:
        cond.literals.append(Literal(_parse_atom(expr), positive))


def parse_condition(expr) -> Condition:
    cond = Condition()
    _flatten_condition(expr, cond, True)
    return cond


def parse_effect(expr):
    if not isinstance(expr, list):
        raise PDDLError(f"Malformed effect: {expr}")
    if not expr:
        return ConjunctiveEffect([])
    head = expr[0]
    if head == "and":
        return ConjunctiveEffect([parse_effect(sub) for sub in expr[1:]])
    if head == "not":
        return DelEffect(_parse_atom(expr[1]))
    if head == "forall":
        return ForallEffect(_parse_typed_list(expr[1]), parse_effect(expr[2]))
    if head == "when":
        return WhenEffect(parse_condition(expr[1]), parse_effect(expr[2]))
    if head == "increase":
        fn = expr[1]
        fname = fn[0] if isinstance(fn, list) else fn
        if fname != "total-cost":
            raise UnsupportedFeatureError(
                "numeric fluents other than total-cost are not supported"
            )
        return IncreaseCostEffect(int(expr[2]))
    if head in _CONNECTIVES:
        raise UnsupportedFeatureError(f"'{head}' is not supported in effects")
    return AddEffect(_parse_atom(expr))


def _section_key(section) -> str:
    return section[0] if section and isinstance(section[0], str) else ""


def parse_domain(tokens: list) -> Domain:
    if _section_key(tokens) != "define":
        raise PDDLError("Domain file must start with (define ...)")

    name = ""
    requirements: list[str] = []
    types: dict[str, str] = {}
    constants: list[tuple[str, str]] = []
    predicates: list[Predicate] = []
    functions: list[str] = []
    actions: list[Action] = []

    for section in tokens[1:]:
        key = _section_key(section)
        if key == "domain":
            name = section[1]
        elif key == ":requirements":
            requirements = list(section[1:])
        elif key == ":types":
            for child, parent in _parse_typed_list(section[1:]):
                # In a :types list, "child - parent" reads name=child, type=parent.
                types[child] = parent
        elif key == ":constants":
            constants = _parse_typed_list(section[1:])
        elif key == ":predicates":
            for pred in section[1:]:
                predicates.append(Predicate(pred[0], _parse_typed_list(pred[1:])))
        elif key == ":functions":
            for fn in section[1:]:
                if isinstance(fn, list) and fn and fn[0] != "-":
                    functions.append(fn[0])
        elif key == ":action":
            actions.append(_parse_action(section))
        elif key in (":durative-action", ":derived"):
            raise UnsupportedFeatureError(f"'{key}' is not supported")
    return Domain(name, requirements, types, constants, predicates, actions, functions)


def _parse_action(section: list) -> Action:
    name = section[1]
    parameters: list[tuple[str, str]] = []
    precondition = Condition()
    effect = ConjunctiveEffect([])
    i = 2
    while i < len(section):
        tag = section[i]
        val = section[i + 1]
        if tag == ":parameters":
            parameters = _parse_typed_list(val)
        elif tag == ":precondition":
            precondition = parse_condition(val)
        elif tag == ":effect":
            effect = parse_effect(val)
        i += 2
    return Action(name, parameters, precondition, effect)


def parse_problem(tokens: list) -> Problem:
    if _section_key(tokens) != "define":
        raise PDDLError("Problem file must start with (define ...)")

    name = ""
    domain_name = ""
    objects: list[tuple[str, str]] = []
    init: list[Atom] = []
    goal = Condition()
    metric = False

    for section in tokens[1:]:
        key = _section_key(section)
        if key == "problem":
            name = section[1]
        elif key == ":domain":
            domain_name = section[1]
        elif key == ":objects":
            objects = _parse_typed_list(section[1:])
        elif key == ":init":
            for fact in section[1:]:
                if not fact:
                    continue
                if fact[0] == "=":
                    # Only (= (total-cost) 0) style initialisation is accepted.
                    continue
                init.append(_parse_atom(fact))
        elif key == ":goal":
            goal = parse_condition(section[1])
        elif key == ":metric":
            metric = True
    return Problem(name, domain_name, objects, init, goal, metric)


def parse(text: str):
    """Parse PDDL text into a :class:`Domain` or :class:`Problem`."""
    tokens = tokenize(text)
    for section in tokens[1:]:
        key = _section_key(section)
        if key == "domain":
            return parse_domain(tokens)
        if key == "problem":
            return parse_problem(tokens)
    raise PDDLError("Could not determine whether input is a domain or a problem")


def parse_domain_file(path: str) -> Domain:
    with open(path, "r", encoding="utf-8") as handle:
        return parse_domain(tokenize(handle.read()))


def parse_problem_file(path: str) -> Problem:
    with open(path, "r", encoding="utf-8") as handle:
        return parse_problem(tokenize(handle.read()))
