class State():
    def __init__(self, description, parent_action=None, parent=None):
        self.description = description
        self.parent_action = parent_action
        self.parent = parent
