"""CLI tests for the ``solve`` and ``benchmark`` subcommands."""

from __future__ import annotations

from jupyddl.cli import main

from conftest import EXAMPLES, paths


def test_cli_solve_success(capsys, examples_available):
    d, p = paths("tsp")
    rc = main(["solve", d, p, "-s", "astar", "-H", "lmcut"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "cost 15" in out
    assert "Valid: True" in out


def test_cli_solve_no_plan(capsys, examples_available):
    d, p = paths("vehicle")  # broken data -> unsolvable
    rc = main(["solve", d, p, "-s", "bfs", "-H", "none"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "No plan found" in out


def test_cli_benchmark(capsys, tmp_path, examples_available):
    csv_path = tmp_path / "out.csv"
    rc = main(
        [
            "benchmark",
            EXAMPLES,
            "--planners",
            "bfs,astar,gbfs",
            "--heuristic",
            "hff",
            "--csv",
            str(csv_path),
        ]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert "coverage" in out
    assert csv_path.exists()


def test_cli_solve_weighted_astar(capsys, examples_available):
    d, p = paths("pallet")
    rc = main(["solve", d, p, "-s", "wastar", "-H", "hff", "-w", "3"])
    assert rc == 0
    assert "Valid: True" in capsys.readouterr().out
