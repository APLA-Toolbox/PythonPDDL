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
        class DRHCache:
            def __init__(self, domain=None, axioms=None, preconds=None, additions=None):
                self.domain = domain 
                self.axioms = axioms
                self.preconds = preconds
                self.additions = additions
        
        self.automated_planner = automated_planner
        self.cache = DRHCache()
        self.heuristic_keys = {
            "delete_relaxation/h_add": self.__h_add,
            "delete_relaxation/h_max": self.__h_max
        }
        if heuristic_key not in list(self.heuristic_keys.keys()):
            logging.warning("Heuristic key isn't registered, forcing it to [delete_relaxation/h_add]")
            heuristic_key = "delete_relaxation/h_add"

        self.current_h = heuristic_key
        self.has_been_precomputed = False
        self.__pre_compute()
        # return self.heuristic_keys[self.current_h](state)

    def compute(self, state, goals):
        if not self.has_been_precomputed:
            self.__pre_compute()
        domain = self.cache.domain
        goals = self.automated_planner.goals
        types = state.types 
        facts = state.facts 

        fact_costs = dict([(f, 0) for f in facts])
        while not(len(fact_costs) == len(facts) and self.__facts_eq(fact_costs, facts)):
            facts_set = self.automated_planner.pddl.Set(self.automated_planner.pddl.keys(fact_costs))
            state = self.automated_planner.pddl.create_state(types, facts_set)
            if self.automated_planner.satisfies(goals, state):
                costs = [fact_costs[g] for g in goals]
                costs.insert(0, 0)
                return self.heuristic_keys[self.current_h](costs)
            
            for ax in self.cache.axioms:
                pass

    def __pre_compute(self):
        if self.has_been_precomputed:
            return
        domain = self.automated_planner.domain
        domain, axioms = self.automated_planner.pddl.compute_hsp_axioms(domain)
        preconditions = dict()
        additions = dict()
        for name, definition in domain.actions.items():
            precond = self.automated_planner.pddl.filter_negative_preconds(definition)
            preconditions[name] = precond
            additions[name] = self.automated_planner.pddl.effect_diff(definition.effect).add
        self.cache.additions = additions
        self.cache.preconds = preconditions
        self.cache.domain = domain
        self.cache.axioms = axioms
        

    def __h_add(self, costs):
        return sum(costs)

    def __h_max(self, costs):
        return max(costs)

    def __facts_eq(self, facts_dict, facts_set):
        for f in facts_set:
            if not(f in facts_dict.keys()):
                return False
        return True

