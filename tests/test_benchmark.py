"""Benchmark harness tests."""

from __future__ import annotations

import csv

from jupyddl.benchmark import (
    discover_instances,
    run_benchmark,
    summarize,
    to_csv,
)

from conftest import EXAMPLES


def test_discover_instances(examples_available):
    names = {inst.name for inst in discover_instances(EXAMPLES)}
    assert {"blocksworld", "dinner", "tsp"} <= names


def test_run_benchmark_and_csv(tmp_path, examples_available):
    instances = [
        i
        for i in discover_instances(EXAMPLES)
        if i.name in ("dinner", "tsp", "grid", "vehicle")
    ]
    configs = [("astar", "lmcut"), ("gbfs", "hff")]
    rows = run_benchmark(instances, configs)
    assert len(rows) == len(instances) * len(configs)

    by_key = {(r.instance, r.planner): r for r in rows}
    assert by_key[("tsp", "astar")].valid
    assert by_key[("tsp", "astar")].cost == 15
    # grid is unsupported -> recorded with an error, not solved.
    assert by_key[("grid", "astar")].error
    assert not by_key[("grid", "astar")].solved
    # vehicle is unsolvable -> solved False but no crash.
    assert not by_key[("vehicle", "astar")].solved

    out = tmp_path / "results.csv"
    to_csv(rows, str(out))
    with open(out, newline="", encoding="utf-8") as handle:
        loaded = list(csv.DictReader(handle))
    assert len(loaded) == len(rows)


def test_summarize_coverage(examples_available):
    instances = [i for i in discover_instances(EXAMPLES) if i.name == "tsp"]
    rows = run_benchmark(instances, [("bfs", None)])
    summary = summarize(rows)
    assert summary["bfs"]["coverage"] == 1
