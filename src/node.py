import uuid

class Node():
    def __init__(self, state, pddl, is_closed=None, is_open=None, parent_action=None, parent=None, g_cost=0, h_cost=0):
        self.uuid = str(uuid.uuid1())
        self.state = state
        self.parent_action = parent_action
        self.parent = parent
        temp_cost = pddl.get_value(state, "total-cost")
        if temp_cost:
            self.g_cost = temp_cost
            self.h_cost = h_cost
            self.f_cost = self.g_cost + self.h_cost
        else:
            self.g_cost = 1
            self.h_cost = h_cost
            self.f_cost = self.g_cost + self.h_cost

    
        self.is_closed = is_closed
        self.is_open = is_open

    def __lt__(self, other):
        return self.f_cost <= other.f_cost
