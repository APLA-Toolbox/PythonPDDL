<div align="center">

# jupyddl — Python PDDL

✨ A dependency-free, pure-Python PDDL planning framework: parser, grounder,
classical-to-SOTA planners, heuristics and a benchmarking harness. ✨

</div>

<div align="center">

![tests](https://github.com/APLA-Toolbox/PythonPDDL/workflows/tests/badge.svg?branch=main)
![build](https://github.com/APLA-Toolbox/PythonPDDL/workflows/build/badge.svg?branch=main)
[![GitHub license](https://img.shields.io/github/license/Apla-Toolbox/PythonPDDL.svg)](./LICENSE)

</div>

`jupyddl` used to be a thin wrapper around the Julia `PDDL.jl` parser. It has been
**rewritten from scratch as a pure-Python framework** — no Julia, no native
dependencies, just the standard library — so it is trivial to install, embed and
build on top of for research and teaching.

## Features 🌱

- 🧩 **Hand-written PDDL parser** and grounder (typing, negative preconditions,
  equality, action costs, and `forall`/`when` conditional effects).
- 🔎 **Uninformed planners**: BFS, DFS, Iterative Deepening.
- 🧭 **Informed planners**: Dijkstra (uniform cost), Greedy Best-First, A*,
  Weighted A*, IDA*, and Enforced Hill Climbing (FF-style).
- 📊 **Heuristics from classical to SOTA**: blind, goal-count, `h_max`, `h_add`,
  FF (`h_ff`), critical-path `h^m` (`h1`/`h2`), and **LM-cut**.
- ⚖️ **Benchmarking harness** for comparative analysis with CSV export and plots.
- 🧱 **Extensible by design**: planners and heuristics live behind simple
  registries; add your own in a few lines.
- ✅ **Zero runtime dependencies** and a comprehensive test suite.

## Install 💾

Requires Python ≥ 3.9. Using [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv venv
uv pip install -e ".[dev,viz]"   # 'viz' pulls matplotlib for benchmark plots
```

or with plain pip:

```bash
python -m pip install -e ".[dev,viz]"
```

## Command line ⚔️

```bash
# Solve a single instance
jupyddl solve pddl-examples/tsp/domain.pddl pddl-examples/tsp/problem.pddl \
    --search astar --heuristic lmcut

# Compare planners over a folder of <name>/{domain,problem}.pddl instances
jupyddl benchmark pddl-examples \
    --planners bfs,dijkstra,astar,gbfs,ehc --heuristic hff \
    --csv results.csv --plot comparison.png
```

## Library usage 📑

```python
from jupyddl import solve, build_task, solve_task, validate_plan

# One-shot solve
result = solve("pddl-examples/tsp/domain.pddl",
               "pddl-examples/tsp/problem.pddl",
               search="astar", heuristic="lmcut")
print(result.solved, result.cost, result.plan_names())

# Ground once, try several configurations
task = build_task("pddl-examples/blocksworld/domain.pddl",
                  "pddl-examples/blocksworld/problem.pddl")
for cfg in [("astar", "lmcut"), ("gbfs", "hff"), ("bfs", None)]:
    r = solve_task(task, cfg[0], cfg[1])
    assert validate_plan(task, r.plan)
    print(cfg, r.cost, r.stats.expanded, "expanded")
```

## Available planners & heuristics

| Planners | Heuristics |
|---|---|
| `bfs`, `dfs`, `iddfs`, `dijkstra`, `gbfs`, `astar`, `wastar`, `idastar`, `ehc` | `blind`, `goalcount`, `hmax`, `hadd`, `hff`, `h1`, `h2`/`hm`, `lmcut` |

`A*`/`IDA*` are cost-optimal with an admissible heuristic (`blind`, `hmax`,
`h1`/`h2`, `lmcut`); `dijkstra` and `bfs` are optimal without a heuristic.

## Supported PDDL subset

STRIPS, `:typing` (with hierarchy), `:negative-preconditions`, `:equality`,
`:action-costs` (`(increase (total-cost) k)`), universally-quantified goals, and
`forall`/`when` conditional effects. Numeric fluents beyond `total-cost` and
`:durative-action`s are out of scope and rejected with a clear error.

> **Note:** on domains with conditional effects (e.g. `flip`), the delete-relaxation
> heuristics (`hadd`, `hff`, `lmcut`, `h^m`) are *satisficing* only — admissibility
> is not guaranteed. Use `bfs`, `dijkstra`, or `astar`/`idastar` with `blind` for
> guaranteed-optimal plans on such domains.

## Architecture 🏗️

```
jupyddl/
  parser/       tokenizer + AST + recursive-descent parser
  grounding.py  Domain+Problem -> grounded Task (typing, PNF, static pruning)
  task.py       grounded STRIPS(+conditional-effects) task & operators
  search/       planners + shared best-first engine + registry
  heuristics/   heuristics + delete-relaxation machinery + registry
  benchmark.py  comparative benchmarking (CSV + plots)
  cli.py        `jupyddl solve` / `jupyddl benchmark`
```

Add a planner by subclassing `jupyddl.search.Planner` (or reusing `best_first`)
and registering it in `jupyddl.search.PLANNERS`; add a heuristic by subclassing
`jupyddl.heuristics.Heuristic` and registering it in
`jupyddl.heuristics.HEURISTICS`.

## Development 🛠️

```bash
git submodule update --init      # fetch the pddl-examples used by the tests
uv pip install -e ".[dev,viz]"
pytest --cov=jupyddl             # run the test suite
flake8 jupyddl tests             # lint
```

## Cite 📰

```
@misc{https://doi.org/10.13140/rg.2.2.22418.89282,
  doi = {10.13140/RG.2.2.22418.89282},
  url = {http://rgdoi.net/10.13140/RG.2.2.22418.89282},
  author = {Erwin Lejeune},
  title = {Jupyddl, an extensible python library for PDDL planning and parsing},
  year = {2021}
}
```

## Maintainers Ⓜ️

- Erwin Lejeune
- Sampreet Sarkar
