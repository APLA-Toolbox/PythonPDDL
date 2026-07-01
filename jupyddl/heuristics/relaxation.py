"""Delete-relaxation machinery shared by h_max, h_add, h_FF and LM-cut."""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass


@dataclass
class RelaxedOp:
    idx: int
    pre: frozenset
    add: frozenset
    cost: int


class RelaxedTask:
    """Delete-relaxed view of a task: unary-ish operators + goal.

    Conditional effects are already expanded into separate relaxed operators by
    :meth:`jupyddl.task.Task.relaxed_operators`.
    """

    def __init__(self, task):
        self.num_facts = task.num_facts
        self.goal = task.goals
        self.ops = [
            RelaxedOp(i, pre, add, cost)
            for i, (pre, add, cost) in enumerate(task.relaxed_operators())
        ]
        # Index: fact -> operators that have it as a precondition.
        self.consumers: list[list[int]] = [[] for _ in range(self.num_facts)]
        self.no_pre: list[int] = []
        for op in self.ops:
            if op.pre:
                for f in op.pre:
                    self.consumers[f].append(op.idx)
            else:
                self.no_pre.append(op.idx)


def propagate_costs(rt: RelaxedTask, state, additive: bool):
    """Generalised Dijkstra computing h_max (``additive=False``) or h_add costs.

    Returns ``(cost, supporter)`` where ``cost[f]`` is the estimated cost to
    achieve fact ``f`` and ``supporter[f]`` is the operator index that achieved
    it (used for FF's relaxed-plan extraction).
    """
    inf = math.inf
    cost = [inf] * rt.num_facts
    supporter = [-1] * rt.num_facts
    counter = [len(op.pre) for op in rt.ops]
    pq: list = []

    for f in state:
        if cost[f] != 0:
            cost[f] = 0
            heapq.heappush(pq, (0, f))

    def op_value(op: RelaxedOp) -> float:
        if not op.pre:
            return op.cost
        pre_costs = [cost[p] for p in op.pre]
        agg = sum(pre_costs) if additive else max(pre_costs)
        return op.cost + agg

    def apply_op(op: RelaxedOp):
        value = op_value(op)
        if math.isinf(value):
            return
        for f in op.add:
            if value < cost[f]:
                cost[f] = value
                supporter[f] = op.idx
                heapq.heappush(pq, (value, f))

    for idx in rt.no_pre:
        apply_op(rt.ops[idx])

    while pq:
        c, f = heapq.heappop(pq)
        if c > cost[f]:
            continue
        for op_idx in rt.consumers[f]:
            counter[op_idx] -= 1
            if counter[op_idx] == 0:
                apply_op(rt.ops[op_idx])
    return cost, supporter


def goal_value(cost, goal, additive: bool) -> float:
    if not goal:
        return 0.0
    values = [cost[g] for g in goal]
    if any(math.isinf(v) for v in values):
        return math.inf
    return float(sum(values) if additive else max(values))
