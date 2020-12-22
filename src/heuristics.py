def zero_heuristic(state, automated_planner):
    return 0


def goal_count_heuristic(state, automated_planner):
    count = 0
    for goal in automated_planner.goals:
        if not automated_planner.state_has_term(state, goal):
            count += 1
    return count
