from .automated_planner import AutomatedPlanner

if __name__ == "__main__":
    _ = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
