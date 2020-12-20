class State():
    def __init__(self, description, is_closed=None, is_open=None, g_cost=None, h_cost=None, parent_action=None, parent=None):
        self.description = description
        self.parent_action = parent_action
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = self.g_cost + self.h_cost
        self.is_closed = is_closed
        self.is_open = is_open

    def __lt__(self, other):
        return self.f_cost <= other.f_cost
