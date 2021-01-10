import logging
import time


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
        heuristic_based=False,
        metric=None,
    ):
        self.state = state
        self.parent_action = parent_action
        self.parent = parent
        self.automated_planner = automated_planner
        temp_cost = automated_planner.pddl.get_value(state, "total-cost")
        if temp_cost:
            self.g_cost = temp_cost
            if heuristic_based:
                if heuristic:
                    clock = time.time()
                    self.h_cost = heuristic(state)
                    if metric:
                        metric.heuristic_runtimes.append(time.time() - clock)
                else:
                    automated_planner.logger.warning(
                        "Heuristic function wasn't found, forcing it to return zero [Best practice: use the zero_heuristic function]"
                    )
                    self.h_cost = 0
            else:
                self.h_cost = 0
            self.f_cost = self.g_cost + self.h_cost
        else:
            if parent:
                self.g_cost = 1 + parent.g_cost
            else:
                self.g_cost = g_cost
            if heuristic_based:
                if heuristic:
                    clock = time.time()
                    self.h_cost = heuristic(state)
                    if metric:
                        metric.heuristic_runtimes.append(time.time() - clock)
                else:
                    automated_planner.logger.warning(
                        "Heuristic function wasn't found, forcing it to return zero [Best practice: use the zero_heuristic function]"
                    )
                    self.h_cost = 0
            else:
                self.h_cost = 0
            self.f_cost = self.g_cost + self.h_cost

        self.is_closed = is_closed
        self.is_open = is_open

    def __stringify_state(self, state):
        state_str = str(state).replace("<PyCall.jlwrap PDDL.State(", "")
        state_str = state_str.replace("Set(Julog.Term[", "")
        state_str = state_str.replace("])", "")
        state_str = state_str.replace(
            'Dict{Symbol,Any}(Symbol("total-cost") =>', "total-cost ="
        )
        state_str = state_str.replace("Dict{Symbol,Any}(", "")
        state_str = state_str.replace(" , ", "")
        state_str = state_str.replace("))>", "")
        return state_str

    def __lt__(self, other):
        return self.f_cost <= other.f_cost

    def __str__(self):
        state = self.__stringify_state(self.state)
        return "Node { %s | g = %.2f | h = %.2f | open = %s | closed = %s }" % (
            state,
            self.g_cost,
            self.h_cost,
            self.is_open,
            self.is_closed,
        )


class Path:
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return str([str(n) for n in self.nodes])
