import logging

class BasicHeuristic:
    def __init__(self, automated_planner, heuristic_key):
        self.automated_planner = automated_planner
        self.heuristic_keys = {
            "basic/zero": self.__zero_heuristic,
            "basic/goal_count": self.__goal_count_heuristic
        }
        if heuristic_key not in list(self.heuristic_keys.keys()):
            logging.warning("Heuristic key isn't registered, forcing it to [basic/goal_count]")
            heuristic_key = "basic/goal_count"

        self.current_h = heuristic_key

    def compute(self, state):
        return self.heuristic_keys[self.current_h](state)

    def __zero_heuristic(self, state):
        return 0

    def __goal_count_heuristic(self, state):
        count = 0
        for goal in self.automated_planner.goals:
            if not self.automated_planner.state_has_term(state, goal):
                count += 1
        return count


class DeleteRelaxationHeuristic:
    def __init__(self, automated_planner, heuristic_key):
        self.automated_planner = automated_planner
        self.heuristic_keys = {
            "delete_relaxation/h_add": self.__h_add,
            "delete_relaxation/h_max": self.__h_max
        }
        if heuristic_key not in list(self.heuristic_keys.keys()):
            logging.warning("Heuristic key isn't registered, forcing it to [delete_relaxation/h_add]")
            heuristic_key = "delete_relaxation/h_add"

        self.current_h = heuristic_key

    def compute(self, state):
        return self.heuristic_keys[self.current_h](state)

    def __pre_compute(self):
        logging.fatal("Delete relaxation h_add is not yet implemented")
        exit()

    def __cache(self):
        logging.fatal("Delete relaxation h_add is not yet implemented")
        exit()

    def __h_add(self, state):
        logging.fatal("Delete relaxation h_add is not yet implemented")
        exit()

    def __h_max(self, state):
        logging.fatal("Delete relaxation h_max is not yet implemented")
        exit()
