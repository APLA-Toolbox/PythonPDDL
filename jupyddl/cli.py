"""Command-line interface: ``jupyddl solve`` and ``jupyddl benchmark``."""

from __future__ import annotations

import argparse
import sys

from .api import build_task, solve_task, validate_plan
from .benchmark import (
    discover_instances,
    plot_summary,
    run_benchmark,
    summarize,
    to_csv,
)
from .heuristics import HEURISTICS
from .search import PLANNERS


def _add_solve(sub):
    p = sub.add_parser("solve", help="solve a single PDDL instance")
    p.add_argument("domain")
    p.add_argument("problem")
    p.add_argument("-s", "--search", default="astar", choices=sorted(PLANNERS))
    p.add_argument(
        "-H", "--heuristic", default="lmcut", choices=sorted(HEURISTICS) + ["none"]
    )
    p.add_argument(
        "-w", "--weight", type=float, default=2.0, help="weight for weighted A*"
    )
    p.set_defaults(func=_cmd_solve)


def _add_benchmark(sub):
    p = sub.add_parser("benchmark", help="compare planners over a folder of instances")
    p.add_argument("root", help="folder containing <name>/domain.pddl + problem.pddl")
    p.add_argument("--planners", default="bfs,dijkstra,astar,gbfs,wastar,ehc")
    p.add_argument("--heuristic", default="hff", help="heuristic for informed planners")
    p.add_argument("--csv", default=None, help="write per-run results to this CSV")
    p.add_argument("--plot", default=None, help="write a comparison bar chart (PNG)")
    p.add_argument("--metric", default="expanded")
    p.set_defaults(func=_cmd_benchmark)


def _cmd_solve(args) -> int:
    task = build_task(args.domain, args.problem)
    heuristic = None if args.heuristic == "none" else args.heuristic
    kwargs = {"weight": args.weight} if args.search == "wastar" else {}
    result = solve_task(task, args.search, heuristic, **kwargs)
    if not result.solved:
        print("No plan found.")
        _print_stats(result)
        return 1
    valid = validate_plan(task, result.plan)
    print(f"Plan ({result.plan_length} steps, cost {result.cost}):")
    for i, op in enumerate(result.plan):
        print(f"  {i + 1:3d}. {op.name}")
    print(f"Valid: {valid}")
    _print_stats(result)
    return 0 if valid else 2


def _cmd_benchmark(args) -> int:
    instances = discover_instances(args.root)
    if not instances:
        print(f"No instances found under {args.root}", file=sys.stderr)
        return 1
    configs = []
    informed = {"gbfs", "astar", "wastar", "idastar", "ehc"}
    for planner in args.planners.split(","):
        planner = planner.strip()
        configs.append((planner, args.heuristic if planner in informed else None))

    rows = run_benchmark(instances, configs)
    _print_summary(summarize(rows))
    if args.csv:
        to_csv(rows, args.csv)
        print(f"\nWrote per-run results to {args.csv}")
    if args.plot:
        plot_summary(rows, args.plot, metric=args.metric)
        print(f"Wrote plot to {args.plot}")
    return 0


def _print_stats(result) -> None:
    s = result.stats
    print(
        f"Stats: expanded={s.expanded} generated={s.generated} "
        f"evaluated={s.evaluated} reopened={s.reopened} "
        f"deadends={s.deadends} runtime={s.runtime:.4f}s"
    )


def _print_summary(summary) -> None:
    print(f"{'config':<20}{'coverage':>12}{'expanded':>12}{'runtime(s)':>12}")
    print("-" * 56)
    for key, agg in summary.items():
        cov = f"{agg['coverage']}/{agg['instances']}"
        print(f"{key:<20}{cov:>12}{agg['expanded']:>12}{agg['runtime']:>12.3f}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="jupyddl",
        description="Pure-Python PDDL planning framework.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    _add_solve(sub)
    _add_benchmark(sub)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
