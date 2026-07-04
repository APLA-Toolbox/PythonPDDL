"""High-level convenience API: parse + ground + plan + validate."""

from __future__ import annotations

from .grounding import ground_files
from .heuristics import make_heuristic
from .search import make_planner
from .search.result import SearchResult
from .task import Task


def build_task(domain_path: str, problem_path: str) -> Task:
    """Parse and ground a domain/problem pair into a :class:`Task`."""
    return ground_files(domain_path, problem_path)


def solve_task(
    task: Task, search: str = "astar", heuristic=None, **planner_kwargs
) -> SearchResult:
    """Run ``search`` (optionally with ``heuristic``) on an already-ground task."""
    planner = make_planner(search, **planner_kwargs)
    heur = None
    name = heuristic if heuristic else ("hff" if planner.requires_heuristic else None)
    if name is not None:
        heur = make_heuristic(name, task)
    return planner.search(task, heur)


def solve(
    domain_path: str,
    problem_path: str,
    search: str = "astar",
    heuristic="lmcut",
    **planner_kwargs,
) -> SearchResult:
    """Parse, ground and solve a PDDL instance in one call."""
    task = build_task(domain_path, problem_path)
    return solve_task(task, search=search, heuristic=heuristic, **planner_kwargs)


def validate_plan(task: Task, plan) -> bool:
    """Return ``True`` iff applying ``plan`` from the initial state reaches the goal."""
    state = task.init
    for op in plan:
        if not op.applicable(state):
            return False
        state = op.apply(state)
    return task.goal_reached(state)
