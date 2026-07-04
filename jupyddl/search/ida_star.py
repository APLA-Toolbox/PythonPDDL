"""Iterative-deepening A* (IDA*): optimal, memory-light informed search."""

from __future__ import annotations

import math
import time

from .base import Planner
from .node import extract_plan, make_child, make_root
from .result import SearchResult, SearchStats


class IDAStarSearch(Planner):
    """IDA*: depth-first search bounded by an increasing ``f = g + h`` threshold.

    Cost-optimal with an admissible heuristic and uses memory linear in the
    solution depth.
    """

    name = "idastar"
    requires_heuristic = True
    optimal = True

    def search(self, task, heuristic=None) -> SearchResult:
        stats = SearchStats()
        start = time.perf_counter()
        hcache: dict = {}

        def h_of(state):
            v = hcache.get(state)
            if v is None:
                v = heuristic(state)
                hcache[state] = v
                stats.evaluated += 1
            return v

        threshold = h_of(task.init)
        root = make_root(task.init)
        while not math.isinf(threshold):
            found, nxt = self._dfs(task, root, threshold, h_of, stats, {task.init})
            if found is not None:
                stats.runtime = time.perf_counter() - start
                return SearchResult(True, extract_plan(found), found.g, stats)
            threshold = nxt
        stats.runtime = time.perf_counter() - start
        return SearchResult(False, None, None, stats)

    def _dfs(self, task, node, threshold, h_of, stats, on_path):
        f = node.g + h_of(node.state)
        if f > threshold:
            return None, f
        if task.goal_reached(node.state):
            return node, threshold
        stats.expanded += 1
        minimum = math.inf
        for op in task.applicable_operators(node.state):
            succ = op.apply(node.state)
            stats.generated += 1
            if succ in on_path:
                continue
            child = make_child(node, op, succ, op.cost)
            on_path.add(succ)
            found, nxt = self._dfs(task, child, threshold, h_of, stats, on_path)
            on_path.discard(succ)
            if found is not None:
                return found, threshold
            minimum = min(minimum, nxt)
        return None, minimum
