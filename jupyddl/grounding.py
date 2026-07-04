"""Grounding: turn a parsed :class:`Domain` + :class:`Problem` into a
grounded :class:`~jupyddl.task.Task`.

Pipeline:

1. Build the ``type -> objects`` table (with type-hierarchy closure).
2. Instantiate every action over all type-consistent parameter tuples,
   expanding ``forall``/``when`` effects and universally-quantified goals.
3. Detect static predicates (never added/deleted) and use the initial state to
   prune infeasible action instances and simplify preconditions/conditions.
4. Compile negative preconditions/goals into *positive normal form* by
   introducing complement facts ``(not ...)`` and maintaining them on every
   operator that touches the underlying atom.
5. Encode everything as integer fact ids.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import product

from .parser.ast import (
    AddEffect,
    Atom,
    ConjunctiveEffect,
    DelEffect,
    Domain,
    ForallEffect,
    IncreaseCostEffect,
    Problem,
    WhenEffect,
)
from .parser.parser import parse_domain_file, parse_problem_file
from .task import CondEffect, Operator, Task


def _ground_atom(atom: Atom, subst: dict) -> Atom:
    return Atom(atom.predicate, tuple(subst.get(a, a) for a in atom.args))


def _build_type_objects(domain: Domain, problem: Problem):
    """Map every type to the set of objects that inhabit it (hierarchy-aware)."""
    parent = dict(domain.types)

    def ancestors(typ: str):
        chain = [typ]
        seen = {typ}
        cur = typ
        while cur in parent and parent[cur] not in (None, "object", cur):
            cur = parent[cur]
            if cur in seen:
                break
            seen.add(cur)
            chain.append(cur)
        return chain

    type_objects: dict[str, set] = defaultdict(set)
    declared: set = set()
    for name, typ in list(domain.constants) + list(problem.objects):
        declared.add(name)
        for anc in ancestors(typ):
            type_objects[anc].add(name)
        type_objects["object"].add(name)

    # Robustness: some (toy) problems omit the :objects section and only mention
    # constants in :init/:goal. Treat any such undeclared constant as an object
    # of the root type so untyped domains still ground.
    for name in _harvest_constants(problem):
        if name not in declared:
            type_objects["object"].add(name)

    for typ in set(list(parent) + list(parent.values())):
        type_objects.setdefault(typ, set())
    return {typ: tuple(sorted(objs)) for typ, objs in type_objects.items()}


def _harvest_constants(problem: Problem) -> set:
    found: set = set()
    for atom in problem.init:
        found.update(a for a in atom.args if not a.startswith("?"))

    def scan(cond):
        for lit in cond.literals:
            found.update(a for a in lit.atom.args if not a.startswith("?"))
        for _, body in cond.universals:
            scan(body)

    scan(problem.goal)
    return found


def _instantiate_condition(cond, subst, type_objects):
    """Return ``(positive_atoms, negative_atoms)`` or ``None`` if infeasible."""
    pos: set = set()
    neg: set = set()
    for eq in cond.equalities:
        left = subst.get(eq.left, eq.left)
        right = subst.get(eq.right, eq.right)
        if (left == right) != eq.positive:
            return None
    for lit in cond.literals:
        atom = _ground_atom(lit.atom, subst)
        (pos if lit.positive else neg).add(atom)
    for params, body in cond.universals:
        pools = [type_objects.get(t, ()) for (_, t) in params]
        for combo in product(*pools):
            sub = dict(subst)
            for (var, _), obj in zip(params, combo):
                sub[var] = obj
            result = _instantiate_condition(body, sub, type_objects)
            if result is None:
                return None
            pos |= result[0]
            neg |= result[1]
    return pos, neg


@dataclass
class _RawOp:
    name: str
    pre_pos: set
    pre_neg: set
    add: set
    delete: set
    cond: list  # list of (cpos, cneg, cadd, cdel) atom-sets
    cost: int


def _collect_effect(eff, subst, type_objects, cpos, cneg, acc):
    if isinstance(eff, ConjunctiveEffect):
        for part in eff.parts:
            _collect_effect(part, subst, type_objects, cpos, cneg, acc)
    elif isinstance(eff, AddEffect):
        atom = _ground_atom(eff.atom, subst)
        if cpos or cneg:
            acc["cond"].append((frozenset(cpos), frozenset(cneg), {atom}, set()))
        else:
            acc["add"].add(atom)
    elif isinstance(eff, DelEffect):
        atom = _ground_atom(eff.atom, subst)
        if cpos or cneg:
            acc["cond"].append((frozenset(cpos), frozenset(cneg), set(), {atom}))
        else:
            acc["delete"].add(atom)
    elif isinstance(eff, IncreaseCostEffect):
        acc["cost"] += eff.amount
        acc["has_cost"] = True
    elif isinstance(eff, ForallEffect):
        pools = [type_objects.get(t, ()) for (_, t) in eff.params]
        for combo in product(*pools):
            sub = dict(subst)
            for (var, _), obj in zip(eff.params, combo):
                sub[var] = obj
            _collect_effect(eff.body, sub, type_objects, cpos, cneg, acc)
    elif isinstance(eff, WhenEffect):
        result = _instantiate_condition(eff.condition, subst, type_objects)
        if result is None:  # condition unsatisfiable for this instance
            return
        wpos, wneg = result
        _collect_effect(eff.body, subst, type_objects, cpos | wpos, cneg | wneg, acc)


def _effect_predicates(domain: Domain) -> set:
    preds: set = set()

    def walk(eff):
        if isinstance(eff, ConjunctiveEffect):
            for part in eff.parts:
                walk(part)
        elif isinstance(eff, (AddEffect, DelEffect)):
            preds.add(eff.atom.predicate)
        elif isinstance(eff, (ForallEffect, WhenEffect)):
            walk(eff.body)

    for action in domain.actions:
        walk(action.effect)
    return preds


def _ground_raw_operators(domain, problem, type_objects) -> list:
    raw = []
    for action in domain.actions:
        pools = [type_objects.get(t, ()) for (_, t) in action.parameters]
        for combo in product(*pools):
            subst = {var: obj for (var, _), obj in zip(action.parameters, combo)}
            pre = _instantiate_condition(action.precondition, subst, type_objects)
            if pre is None:
                continue
            acc = {
                "add": set(),
                "delete": set(),
                "cond": [],
                "cost": 0,
                "has_cost": False,
            }
            _collect_effect(action.effect, subst, type_objects, set(), set(), acc)
            args = ",".join(combo)
            name = f"{action.name}({args})" if combo else action.name
            cost = acc["cost"] if acc["has_cost"] else 1
            raw.append(
                _RawOp(
                    name, pre[0], pre[1], acc["add"], acc["delete"], acc["cond"], cost
                )
            )
    return raw


@dataclass
class _Encoder:
    fact_ids: dict = field(default_factory=dict)
    comp_ids: dict = field(default_factory=dict)
    names: list = field(default_factory=list)

    def fact(self, atom: Atom) -> int:
        if atom not in self.fact_ids:
            self.fact_ids[atom] = len(self.names)
            self.names.append(str(atom))
        return self.fact_ids[atom]

    def comp(self, atom: Atom) -> int:
        if atom not in self.comp_ids:
            self.comp_ids[atom] = len(self.names)
            self.names.append(f"(not {atom})")
        return self.comp_ids[atom]


def ground(domain: Domain, problem: Problem) -> Task:
    """Ground ``domain`` + ``problem`` into a :class:`Task`."""
    type_objects = _build_type_objects(domain, problem)
    init_atoms = set(problem.init)
    static_preds = {p.name for p in domain.predicates} - _effect_predicates(domain)

    def is_static(atom: Atom) -> bool:
        return atom.predicate in static_preds

    raw_ops = _ground_raw_operators(domain, problem, type_objects)

    enc = _Encoder()
    # Collect fluent atoms whose complement is referenced (need PNF facts).
    tracked_neg: set = set()

    # --- resolve static literals, drop infeasible operators ------------------
    resolved = []
    for op in raw_ops:
        feasible = True
        pre_pos_fluent, pre_neg_fluent = set(), set()
        for atom in op.pre_pos:
            if is_static(atom):
                if atom not in init_atoms:
                    feasible = False
                    break
            else:
                pre_pos_fluent.add(atom)
        if not feasible:
            continue
        for atom in op.pre_neg:
            if is_static(atom):
                if atom in init_atoms:
                    feasible = False
                    break
            else:
                pre_neg_fluent.add(atom)
                tracked_neg.add(atom)
        if not feasible:
            continue

        add = set(op.add)
        delete = set(op.delete)
        cond = []
        for cpos, cneg, cadd, cdel in op.cond:
            triggers = True
            cpos_f, cneg_f = set(), set()
            for atom in cpos:
                if is_static(atom):
                    if atom not in init_atoms:
                        triggers = False
                        break
                else:
                    cpos_f.add(atom)
            if not triggers:
                continue
            for atom in cneg:
                if is_static(atom):
                    if atom in init_atoms:
                        triggers = False
                        break
                else:
                    cneg_f.add(atom)
                    tracked_neg.add(atom)
            if not triggers:
                continue
            if not cpos_f and not cneg_f:
                add |= cadd
                delete |= cdel
            else:
                cond.append((cpos_f, cneg_f, cadd, cdel))
        resolved.append(
            (op.name, pre_pos_fluent, pre_neg_fluent, add, delete, cond, op.cost)
        )

    # --- goal ----------------------------------------------------------------
    goal_res = _instantiate_condition(problem.goal, {}, type_objects)
    if goal_res is None:
        raise ValueError("Goal condition is self-contradictory")
    goal_pos, goal_neg = goal_res
    unsolvable = False
    goal_pos_fluent, goal_neg_fluent = set(), set()
    for atom in goal_pos:
        if is_static(atom):
            if atom not in init_atoms:
                unsolvable = True
        else:
            goal_pos_fluent.add(atom)
    for atom in goal_neg:
        if is_static(atom):
            if atom in init_atoms:
                unsolvable = True
        else:
            goal_neg_fluent.add(atom)
            tracked_neg.add(atom)

    # --- encode facts --------------------------------------------------------
    init_ids = {enc.fact(a) for a in init_atoms if not is_static(a)}
    for atom in tracked_neg:
        cid = enc.comp(atom)
        if atom not in init_atoms:
            init_ids.add(cid)

    def encode_add_del(add_atoms, del_atoms):
        add_ids = {enc.fact(a) for a in add_atoms}
        del_ids = {enc.fact(a) for a in del_atoms}
        for a in add_atoms:
            if a in tracked_neg:
                del_ids.add(enc.comp(a))
        for a in del_atoms:
            if a in tracked_neg:
                add_ids.add(enc.comp(a))
        return frozenset(add_ids), frozenset(del_ids)

    operators = []
    for name, pp, pn, add, delete, cond, cost in resolved:
        precond = {enc.fact(a) for a in pp} | {enc.comp(a) for a in pn}
        add_ids, del_ids = encode_add_del(add, delete)
        cond_effects = []
        for cpos_f, cneg_f, cadd, cdel in cond:
            cond_ids = {enc.fact(a) for a in cpos_f} | {enc.comp(a) for a in cneg_f}
            cadd_ids, cdel_ids = encode_add_del(cadd, cdel)
            if cadd_ids or cdel_ids:
                cond_effects.append(CondEffect(frozenset(cond_ids), cadd_ids, cdel_ids))
        operators.append(
            Operator(
                name, frozenset(precond), add_ids, del_ids, tuple(cond_effects), cost
            )
        )

    goals = {enc.fact(a) for a in goal_pos_fluent} | {
        enc.comp(a) for a in goal_neg_fluent
    }
    if unsolvable:
        sentinel = len(enc.names)
        enc.names.append("(unsolvable)")
        goals.add(sentinel)  # never produced by any operator

    return Task(
        name=problem.name or domain.name,
        facts=tuple(enc.names),
        init=frozenset(init_ids),
        goals=frozenset(goals),
        operators=tuple(operators),
        metric_cost=problem.metric_minimize_cost,
    )


def ground_files(domain_path: str, problem_path: str) -> Task:
    """Convenience: parse both files and ground them into a :class:`Task`."""
    return ground(parse_domain_file(domain_path), parse_problem_file(problem_path))
