"""High-level API tests."""

from __future__ import annotations

from jupyddl import build_task, solve, validate_plan

from conftest import paths


def test_solve_end_to_end(examples_available):
    d, p = paths("tsp")
    result = solve(d, p, search="astar", heuristic="lmcut")
    assert result.solved
    assert result.cost == 15
    assert result.plan_names()[0].startswith("move(")


def test_validate_plan_rejects_broken_plan(examples_available):
    task = build_task(*paths("blocksworld"))
    result = solve(*paths("blocksworld"), search="bfs", heuristic=None)
    assert validate_plan(task, result.plan)
    # Dropping the first operator should make the plan invalid.
    assert not validate_plan(task, result.plan[1:])


def test_default_heuristic_for_informed_planner(examples_available):
    # gbfs requires a heuristic; solve_task should supply a default if omitted.
    from jupyddl import solve_task

    task = build_task(*paths("dinner"))
    result = solve_task(task, "gbfs")  # no heuristic given
    assert result.solved
