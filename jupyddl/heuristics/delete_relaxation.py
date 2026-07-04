"""Delete-relaxation heuristics: h_max, h_add and the FF heuristic."""

from __future__ import annotations

import math
from collections import deque

from .base import Heuristic
from .relaxation import RelaxedTask, goal_value, propagate_costs


class HMaxHeuristic(Heuristic):
    """h_max: the most expensive relaxed goal fact. Admissible."""

    name = "hmax"
    admissible = True

    def __init__(self, task):
        super().__init__(task)
        self.rt = RelaxedTask(task)

    def __call__(self, state) -> float:
        cost, _ = propagate_costs(self.rt, state, additive=False)
        return goal_value(cost, self.rt.goal, additive=False)


class HAddHeuristic(Heuristic):
    """h_add: sum of relaxed goal-fact costs. Informative, not admissible."""

    name = "hadd"

    def __init__(self, task):
        super().__init__(task)
        self.rt = RelaxedTask(task)

    def __call__(self, state) -> float:
        cost, _ = propagate_costs(self.rt, state, additive=True)
        return goal_value(cost, self.rt.goal, additive=True)


class FFHeuristic(Heuristic):
    """FF heuristic: cost of a relaxed plan extracted from the h_add graph."""

    name = "hff"

    def __init__(self, task):
        super().__init__(task)
        self.rt = RelaxedTask(task)

    def __call__(self, state) -> float:
        cost, supporter = propagate_costs(self.rt, state, additive=True)
        if any(math.isinf(cost[g]) for g in self.rt.goal):
            return math.inf
        relaxed_plan: set = set()
        seen: set = set()
        queue = deque(self.rt.goal)
        while queue:
            fact = queue.popleft()
            if fact in state or fact in seen:
                continue
            seen.add(fact)
            op_idx = supporter[fact]
            if op_idx < 0:
                return math.inf
            if op_idx not in relaxed_plan:
                relaxed_plan.add(op_idx)
                for pre_fact in self.rt.ops[op_idx].pre:
                    if pre_fact not in state:
                        queue.append(pre_fact)
        return float(sum(self.rt.ops[i].cost for i in relaxed_plan))
