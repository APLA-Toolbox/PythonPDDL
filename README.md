![tests](https://github.com/APLA-Toolbox/PythonPDDL/workflows/tests/badge.svg?branch=main)
![build](https://github.com/APLA-Toolbox/PythonPDDL/workflows/build/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/APLA-Toolbox/PythonPDDL/branch/main/graph/badge.svg?token=63GHA9JUND)](https://codecov.io/gh/APLA-Toolbox/PythonPDDL)
[![CodeFactor](https://www.codefactor.io/repository/github/apla-toolbox/pythonpddl/badge)](https://www.codefactor.io/repository/github/apla-toolbox/pythonpddl)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/APLA-Toolbox/PythonPDDL.svg)](http://isitmaintained.com/project/APLA-Toolbox/PythonPDDL "Percentage of issues still open")
[![GitHub license](https://img.shields.io/github/license/Apla-Toolbox/PythonPDDL.svg)](https://github.com/Apla-Toolbox/PythonPDDL/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/Apla-Toolbox/PythonPDDL.svg)](https://GitHub.com/Apla-Toolbox/PythonPDDL/graphs/contributors/)



# PyJulia PDDL Planner

A Python wrapper using JuliaPy for the PDDL.jl parser package and implementing its own planners.

## Features

- Easy to use API for exploring new states
- Depth First Search
- Breadth First Search
- Dijkstra
- A*
    - Goal Count Heuristic
    - Delete Relaxation Heuristics (Hmax, Hadd)
    - Critical Path Heuristic

## Docker

You can also use the project in a docker container using [docker-pythonpddl](https://github.com/APLA-Toolbox/docker-pythonpddl)

## Dependencies

- Install Python (3.7.5 is the tested version)

- Install Julia

```bash
$ wget https://julialang-s3.julialang.org/bin/linux/x64/1.5/julia-1.5.2-linux-x86_64.tar.gz
$ tar -xvzf julia-1.5.2-linux-x86_64.tar.gz
$ sudo cp -r julia-1.5.2 /opt/
$ sudo ln -s /opt/julia-1.5.2/bin/julia /usr/local/bin/julia
```

- Install Julia dependencies

```bash
$ julia --color=yes -e 'using Pkg; Pkg.add(Pkg.PackageSpec(path="https://github.com/APLA-Toolbox/PDDL.jl"))'
$ julia --color=yes -e 'using Pkg; Pkg.add(Pkg.PackageSpec(path="https://github.com/JuliaPy/PyCall.jl"))'
```

- Package installation (only if used as library, not needed to run the scripts)

```bash
$ python3 -m pip install --upgrade pip
$ python3 -m pip install jupyddl
```

## IPC Script

- Clone the project :
```shell
$ git clone https://github.com/APLA-Toolbox/PythonPDDL
$ cd PythonPDDL
$ python3 -m pip install -r requirements.txt
$ git submodule update --init // Only if you need PDDL files for testing
```

- Run the script :
```shell
$ cd scripts/
$ python ipc.py "path_to_domain.pddl" "path_to_problem.pddl" "path_to_desired_output_file"
```

The output file will show the path with a list of state, the path with a list of action and the metrics proposed by IPC2018.

## Library Usage

If using the jupyddl pip package:

- If you want to use the data analysis tool, create a pddl-examples folder with pddl instances subfolders containing "problem.pddl" and "domain.pddl". (refer to APLA-Toolbox/pddl-examples)

If you want to use it by cloning the project:

```shell
$ git clone https://github.com/APLA-Toolbox/PythonPDDL
$ cd PythonPDDL
$ python3 -m pip install -r requirements.txt
$ git submodule update --init
```

You should have a `pddl-examples` folder containing PDDL instances.

### [AutomatedPlanner]

```python
from jupyddl import AutomatedPlanner # takes some time because it has to instantiate the Julia interface
apl = AutomatedPlanner("pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl)

apl.available_heuristics
["basic/zero", "basic/goal_count", "delete_relaxation/h_max", "delete_relaxation/h_add"]

apl.initial_state
<PyCall.jlwrap PDDL.State(Set(Julog.Term[row(r1), column(c3), row(r3), row(r2), column(c2), column(c1)]), Set(Julog.Term[white(r2, c1), white(r1, c2), white(r3, c2), white(r2, c3)]), Dict{Symbol,Any}())>

actions = apl.available_actions(apl.initial_state)
[<PyCall.jlwrap flip_row(r1)>, <PyCall.jlwrap flip_row(r3)>, <PyCall.jlwrap flip_row(r2)>, <PyCall.jlwrap flip_column(c3)>, <PyCall.jlwrap flip_column(c2)>, <PyCall.jlwrap flip_column(c1)>]

apl.satisfies(apl.problem.goal, apl.initial_state)
False

apl.transition(apl.initial_state, actions[0])
<PyCall.jlwrap PDDL.State(Set(Julog.Term[row(r1), column(c3), row(r3), row(r2), column(c2), column(c1)]), Set(Julog.Term[white(r2, c1), white(r1, c1), white(r3, c2), white(r2, c3), white(r1, c3)]), Dict{Symbol,Any}())>

path = apl.breadth_first_search() # computes path ([]State) with BFS

print(apl.get_state_def_from_path(path))
[<PyCall.jlwrap PDDL.State(Set(Julog.Term[row(r1), column(c3), row(r3), row(r2), column(c2), column(c1)]), Set(Julog.Term[white(r2, c1), white(r1, c1), white(r3, c2), white(r2, c3), white(r1, c3)]), Dict{Symbol,Any}())>, <PyCall.jlwrap PDDL.State(Set(Julog.Term[row(r1), column(c3), row(r3), row(r2), column(c2), column(c1)]), Set(Julog.Term[white(r2, c1), white(r1, c1), white(r2, c3), white(r1, c3), white(r3, c3), white(r3, c1)]), Dict{Symbol,Any}())>, <PyCall.jlwrap PDDL.State(Set(Julog.Term[row(r1), column(c3), row(r3), row(r2), column(c2), column(c1)]), Set(Julog.Term[white(r2, c1), white(r1, c1), white(r1, c2), white(r3, c2), white(r2, c3), white(r1, c3), white(r3, c3), white(r3, c1), white(r2, c2)]), Dict{Symbol,Any}())>]

print(apl.get_actions_from_path(path))
[<PyCall.jlwrap flip_row(r1)>, <PyCall.jlwrap flip_row(r3)>, <PyCall.jlwrap flip_column(c2)>]
```

### [Data Analyst]

Make sure you have a pddl-examples folder where you run your environment that contains independent folders with "domain.pddl" and "problem.pddl" files, with those standard names. ( if you didn't generate with git submodule update )

```python
from jupyddl import DataAnalyst

da = DataAnalyst()
da.plot_astar() # plots complexity statistics for all the problem.pddl/domain.pddl couples in the pddl-examples/ folder

da.plot_astar(problem="pddl-examples/dinner/problem.pddl", domain="pddl-examples/dinner/domain.pddl") # scatter complexity statistics for the provided pddl

da.plot_astar(heuristic_key="basic/zero") # use h=0 instead of goal_count for your computation

da.plot_dfs() # same as astar

da.comparative_data_plot() # Run all planners on the pddl-examples folder and plots them on the same figure, data is stored in a data.json file 

da.comparative_data_plot(astar=False) # Exclude astar from the comparative plot

da.comparative_data_plot(heuristic_key="basic/zero") # use zero heuristic for h based planners

da.comparative_data_plot(collect_new_data=False) # uses data.json to plot the data

da.comparative_astar_heuristic_plot() # compare results of astar with all available heuristics
```

## Contribute

Open an issue to state clearly the contribution you want to make. Upon aproval send in a PR with the Issue referenced. (Implement Issue #No / Fix Issue #No).

## Maintainers

- Erwin Lejeune
- Sampreet Sarkar
