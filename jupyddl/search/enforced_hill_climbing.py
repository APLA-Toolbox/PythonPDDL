"""Enforced Hill Climbing (EHC), the search that made the FF planner famous.

From each state it runs a breadth-first probe until it reaches a state with a
strictly better heuristic value, then commits to that path and repeats. It is a
fast satisficing strategy (not complete, not optimal); pair it with an
informative heuristic such as FF.
"""

from __future__ import annotations

import time
from collections import deque

from .base import Planner
from .result import SearchResult, SearchStats


class EnforcedHillClimbing(Planner):
    name = "ehc"
    requires_heuristic = True

    def search(self, task, heuristic=None) -> SearchResult:
        stats = SearchStats()
        start = time.perf_counter()
        current = task.init
        current_h = heuristic(current)
        stats.evaluated += 1
        plan: list = []
        cost = 0
        while not task.goal_reached(current):
            state, ops, path_cost, new_h = self._probe(
                task, current, current_h, heuristic, stats
            )
            if state is None:  # no strictly-improving state reachable
                stats.runtime = time.perf_counter() - start
                return SearchResult(False, None, None, stats)
            plan.extend(ops)
            cost += path_cost
            current = state
            current_h = new_h
        stats.runtime = time.perf_counter() - start
        return SearchResult(True, plan, cost, stats)

    def _probe(self, task, start, target_h, heuristic, stats):
        """BFS from ``start`` for a state with ``h < target_h`` (or the goal)."""
        visited = {start}
        queue = deque([(start, [], 0)])
        while queue:
            state, ops, cost = queue.popleft()
            stats.expanded += 1
            for op in task.applicable_operators(state):
                succ = op.apply(state)
                stats.generated += 1
                if succ in visited:
                    continue
                visited.add(succ)
                new_ops = ops + [op]
                new_cost = cost + op.cost
                if task.goal_reached(succ):
                    return succ, new_ops, new_cost, 0
                value = heuristic(succ)
                stats.evaluated += 1
                if value < target_h:
                    return succ, new_ops, new_cost, value
                queue.append((succ, new_ops, new_cost))
        return None, None, None, None
