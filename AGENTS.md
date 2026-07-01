# AGENTS.md

## Cursor Cloud specific instructions

`jupyddl` is a **pure-Python** PDDL planning framework (parser, grounder,
planners, heuristics, benchmarking). The Julia/`PDDL.jl`/PyCall integration has
been removed — there is no Julia, no native build step, and the core has zero
runtime dependencies.

### Environment
- Python ≥ 3.9; a `.venv` (created with `uv`, Python 3.12) with an editable
  install: `uv pip install -e ".[dev]"` (add `viz` for matplotlib-based
  benchmark plots). `.venv` and `pddl-examples/` contents are git-ignored.
- The `pddl-examples` git submodule supplies the domains/problems the tests use;
  it must be initialised (`git submodule update --init`).

### Running / testing / linting (use the venv interpreter)
- Tests: `.venv/bin/python -m pytest` (add `--cov=jupyddl`).
- Lint (as CI): `flake8 jupyddl tests` (config in `.flake8`, max-line 100).
- CLI: `.venv/bin/python -m jupyddl.cli solve <domain> <problem> -s astar -H lmcut`
  or `... benchmark pddl-examples --csv out.csv`. Installed as `jupyddl` too.

### Non-obvious notes
- **Example data quirks (external submodule, do not "fix" in this repo):**
  `grid` uses numeric fluents and is intentionally unsupported (raises
  `UnsupportedFeatureError`); `vehicle` has typos in its problem file
  (`struck`/`truck`, `acessible`) so its goal is unreachable and it is correctly
  reported unsolvable. Tests treat both as expected.
- **Conditional effects (`flip`)**: the delete-relaxation heuristics (`hadd`,
  `hff`, `lmcut`, `h^m`) are *not guaranteed admissible* on domains with
  conditional effects because each conditional effect is relaxed into its own
  operator. For guaranteed-optimal plans there use `bfs`, `dijkstra`, or
  `astar`/`idastar` with the `blind` heuristic. Optimality tests use these.
- **Matplotlib is optional**: only `jupyddl.benchmark.plot_summary` (and
  `jupyddl solve/benchmark --plot`) need it; run headless with `MPLBACKEND=Agg`
  if no display. The test suite does not require it.
- Extend via the registries: `jupyddl.search.PLANNERS` and
  `jupyddl.heuristics.HEURISTICS`.
