class State():
    def __init__(self, description, pddl, is_closed=None, is_open=None, parent_action=None, parent=None):
        self.description = description
        self.parent_action = parent_action
        self.parent = parent
        temp_cost = pddl.get_value(description, "total-cost")
        if temp_cost:
            self.g_cost = temp_cost
            self.h_cost = 0
            self.f_cost = self.g_cost + self.h_cost
        else:
            self.g_cost = None
            self.h_cost = None
            self.f_cost = None

    
        self.is_closed = is_closed
        self.is_open = is_open

    def __lt__(self, other):
        return self.f_cost <= other.f_cost
