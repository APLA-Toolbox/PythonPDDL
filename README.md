# Pyjulia PDDL

A Python wrapper using JuliaPy for the PDDL.jl package. It implements Planners (Best-First, Breadth-First, Depth-First) as class methods. Easy to use even in REFL mode. The AutomatedPlanning class is clear and understandable, easy to contribute to.

# REFL Mode

- Clone the repository: `git clone https://github.com/APLA-Toolbox/pyjulia-pddl`
- Move to the repository folder: `cd pyjulia-pddl`
- Run `python3` in the terminal.
- Use the AutomatedPlanning class to do what you want:
```python
from src.pddl import AutomatedPlanning # takes some time because it has to instantiate the Julia interface
apl = AutomatedPlanning("data/domain.pddl", "data/problem.pddl)

apl.initial_state
<PyCall.jlwrap PDDL.State(Set(Julog.Term[row(r1), column(c3), row(r3), row(r2), column(c2), column(c1)]), Set(Julog.Term[white(r2, c1), white(r1, c2), white(r3, c2), white(r2, c3)]), Dict{Symbol,Any}())>

apl.available_actions(apl.initial_state)
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

# Script mode

UC

# Contribute

Open an issue to state clearly the contribution you want to make. Upon aproval send in a PR with the Issue referenced. (Implement Issue #No / Fix Issue #No).

# Contributors

- Erwin Lejeune
- Sampreet Sarkar
