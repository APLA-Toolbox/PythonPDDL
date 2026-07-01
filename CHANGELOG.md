# Changelog

All notable changes to this project are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-01

Complete rewrite: **the Julia dependency is removed** and the project is now a
pure-Python planning framework.

### Added
- Hand-written PDDL tokenizer, AST and recursive-descent parser
  (`jupyddl.parser`).
- Grounder (`jupyddl.grounding`) with type hierarchies, static-predicate
  pruning, positive-normal-form compilation of negative preconditions/goals,
  object harvesting for undeclared constants, and `forall`/`when` conditional
  effect expansion.
- Grounded task representation with conditional effects (`jupyddl.task`).
- Planners (`jupyddl.search`): BFS, DFS, Iterative Deepening, Dijkstra
  (uniform cost), Greedy Best-First, A*, Weighted A*, IDA*, and Enforced Hill
  Climbing, plus a shared best-first engine and a planner registry.
- Heuristics (`jupyddl.heuristics`): blind, goal-count, `h_max`, `h_add`, FF,
  critical-path `h^m` (`h1`/`h2`), and LM-cut, plus a heuristic registry.
- Benchmarking harness (`jupyddl.benchmark`) with CSV export and comparison
  plots, and a CLI (`jupyddl solve` / `jupyddl benchmark`).
- High-level API: `solve`, `build_task`, `solve_task`, `validate_plan`.
- Comprehensive pytest suite covering parsing, grounding, search optimality,
  heuristic admissibility, the API, the benchmark harness and the CLI.

### Changed
- Packaging migrated from `setup.py`/`requirements.txt` to `pyproject.toml`
  (hatchling); the core has **zero runtime dependencies** (matplotlib is an
  optional `viz` extra).
- CI reworked to run on modern Python without Julia.

### Removed
- The Julia / `PDDL.jl` / PyCall / pyjulia integration and the old
  `AutomatedPlanner` / `DataAnalyst` API.
