# AGENTS.md

## Cursor Cloud specific instructions

`jupyddl` (PythonPDDL) is a Python library + CLI for PDDL automated planning. It is a
thin wrapper around the Julia `PDDL.jl` parser, bridged through `pyjulia`/`PyCall.jl`.
There are no servers/databases — "running the app" means parsing PDDL domain/problem
files and running the planners, either via the library or the `scripts/ipc.py` CLI.

### Environment layout (baked into the VM snapshot)
- Julia 1.5.2 in `/opt/julia-1.5.2` (symlinked at `/usr/local/bin/julia`).
- Python 3.8 venv at `.venv`, built from the **deadsnakes** `/usr/bin/python3.8`.
- Julia packages `PyCall.jl` + the `APLA-Toolbox/PDDL.jl` fork live in `~/.julia`.
  `PyCall` is built against `.venv/bin/python`.
- `.venv`, `logs/*`, and the `pddl-examples` submodule contents are git-ignored.

### Running / testing / linting
Always use the venv interpreter and run from the repo root (relative `pddl-examples/...`
paths and the auto-created `logs/` dir depend on CWD):
- Library / hello-world: `.venv/bin/python -c "from jupyddl import AutomatedPlanner; ..."`
- CLI: `cd scripts && ../.venv/bin/python ipc.py <domain.pddl> <problem.pddl> <output>`
- Tests: `.venv/bin/python -m pytest --cov=./` (from repo root).
- Lint (as CI): `.venv/bin/python -m flake8 . --select=E9,F63,F7,F82` is the build-gating
  check; the second CI `flake8` pass uses `--exit-zero` (style warnings only, non-blocking).

### Non-obvious gotchas
- **pyjulia needs a dynamically-linked Python.** The `.venv` intentionally uses the
  deadsnakes `python3.8` (dynamically linked). Do **not** rebuild the venv from a
  `uv`-managed / python-build-standalone interpreter — those are statically linked to
  libpython and break the in-process Julia bridge.
- **If the venv is recreated at a different path, rebuild PyCall** so it points at the new
  interpreter: `PYTHON=/workspace/.venv/bin/python .venv/bin/python -c "import julia; julia.install()"`.
- **matplotlib backend.** `jupyddl/data_analyst.py` picks `TkAgg` when `DISPLAY` is set and
  `Agg` otherwise. The VM has a virtual display (`DISPLAY=:1`) and `python3.8-tk` is
  installed, so the default import works. For a purely headless run, invoke with
  `env -u DISPLAY ...` (or `MPLBACKEND=Agg` when the import path allows it) to force `Agg`.
- **Known pre-existing test failures (not an environment problem):** 19 `DataAnalyst`
  tests that iterate over the *whole* `pddl-examples/` folder fail with a
  `PyCall.jlwrap ... 'domain' keyword is missing` error. Cause is a code bug in
  `__get_all_pddl_from_data`, which pairs files from an unsorted `os.walk` and assumes
  `domain.pddl` precedes `problem.pddl`; the `pallet` example is listed in the opposite
  order, so a problem file gets parsed as a domain. The 58 core tests (planners, parser,
  heuristics, node, metrics, single-instance `DataAnalyst`) pass.
