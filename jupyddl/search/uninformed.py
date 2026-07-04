"""Uninformed planners: breadth-first, depth-first and iterative deepening."""

from __future__ import annotations

import time
from collections import deque

from .base import Planner
from .node import extract_plan, make_child, make_root
from .result import SearchResult, SearchStats


class BreadthFirstSearch(Planner):
    """FIFO breadth-first graph search. Optimal in number of actions."""

    name = "bfs"
    optimal = True  # for unit-cost / plan-length

    def search(self, task, heuristic=None) -> SearchResult:
        stats = SearchStats()
        start = time.perf_counter()
        root = make_root(task.init)
        if task.goal_reached(task.init):
            stats.runtime = time.perf_counter() - start
            return SearchResult(True, [], 0, stats)
        visited = {task.init}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            stats.expanded += 1
            for op in task.applicable_operators(node.state):
                succ = op.apply(node.state)
                stats.generated += 1
                if succ in visited:
                    continue
                child = make_child(node, op, succ, op.cost)
                if task.goal_reached(succ):
                    stats.runtime = time.perf_counter() - start
                    return SearchResult(True, extract_plan(child), child.g, stats)
                visited.add(succ)
                queue.append(child)
        stats.runtime = time.perf_counter() - start
        return SearchResult(False, None, None, stats)


class DepthFirstSearch(Planner):
    """LIFO depth-first graph search. Complete on finite spaces, not optimal."""

    name = "dfs"

    def search(self, task, heuristic=None) -> SearchResult:
        stats = SearchStats()
        start = time.perf_counter()
        root = make_root(task.init)
        visited = {task.init}
        stack = [root]
        while stack:
            node = stack.pop()
            if task.goal_reached(node.state):
                stats.runtime = time.perf_counter() - start
                return SearchResult(True, extract_plan(node), node.g, stats)
            stats.expanded += 1
            for op in task.applicable_operators(node.state):
                succ = op.apply(node.state)
                stats.generated += 1
                if succ in visited:
                    continue
                visited.add(succ)
                stack.append(make_child(node, op, succ, op.cost))
        stats.runtime = time.perf_counter() - start
        return SearchResult(False, None, None, stats)


class IterativeDeepeningSearch(Planner):
    """Iterative-deepening DFS. Optimal in plan length with low memory."""

    name = "iddfs"
    optimal = True

    def __init__(self, max_depth: int = 1000):
        self.max_depth = max_depth

    def search(self, task, heuristic=None) -> SearchResult:
        stats = SearchStats()
        start = time.perf_counter()
        for limit in range(self.max_depth + 1):
            found, cutoff = self._dls(
                task, make_root(task.init), limit, stats, {task.init}
            )
            if found is not None:
                stats.runtime = time.perf_counter() - start
                return SearchResult(True, extract_plan(found), found.g, stats)
            if not cutoff:  # search exhausted without hitting the depth limit
                break
        stats.runtime = time.perf_counter() - start
        return SearchResult(False, None, None, stats)

    def _dls(self, task, node, limit, stats, on_path):
        if task.goal_reached(node.state):
            return node, False
        if node.depth == limit:
            return None, True
        stats.expanded += 1
        cutoff = False
        for op in task.applicable_operators(node.state):
            succ = op.apply(node.state)
            stats.generated += 1
            if succ in on_path:
                continue
            child = make_child(node, op, succ, op.cost)
            on_path.add(succ)
            found, cut = self._dls(task, child, limit, stats, on_path)
            on_path.discard(succ)
            if found is not None:
                return found, False
            cutoff = cutoff or cut
        return None, cutoff
