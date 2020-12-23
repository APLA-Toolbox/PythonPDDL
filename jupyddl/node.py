import logging


class Node:
    def __init__(
        self,
        state,
        automated_planner,
        is_closed=None,
        is_open=None,
        parent_action=None,
        parent=None,
        g_cost=0,
        heuristic=None,
    ):
        self.state = state
        self.parent_action = parent_action
        self.parent = parent
        temp_cost = automated_planner.pddl.get_value(state, "total-cost")
        if temp_cost:
            self.g_cost = temp_cost
            if heuristic:
                self.h_cost = heuristic(state, automated_planner)
            else:
                self.h_cost = 0
            self.f_cost = self.g_cost + self.h_cost
        else:
            if parent:
                self.g_cost = 1 + parent.g_cost
            else:
                self.g_cost = g_cost
            if heuristic:
                self.h_cost = heuristic(state, automated_planner)
            else:
                automated_planner.logger.warning(
                    "Heuristic function wasn't found, forcing it to return zero [Best practice: use the zero_heuristic function]"
                )
                self.h_cost = 0
            self.f_cost = self.g_cost + self.h_cost

        self.is_closed = is_closed
        self.is_open = is_open

    def __lt__(self, other):
        return self.f_cost <= other.f_cost
