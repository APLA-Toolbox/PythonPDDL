import logging
from .node import Node


class BasicHeuristic:
    def __init__(self, automated_planner, heuristic_key):
        self.automated_planner = automated_planner
        self.heuristic_keys = {
            "basic/zero": self.__zero_heuristic,
            "basic/goal_count": self.__goal_count_heuristic,
        }
        if heuristic_key not in list(self.heuristic_keys.keys()):
            logging.warning(
                "Heuristic key isn't registered, forcing it to [basic/goal_count]"
            )
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
            "delete_relaxation/h_max": self.__h_max,
        }
        if heuristic_key not in list(self.heuristic_keys.keys()):
            logging.warning(
                "Heuristic key isn't registered, forcing it to [delete_relaxation/h_add]"
            )
            heuristic_key = "delete_relaxation/h_add"

        self.current_h = heuristic_key
        self.has_been_precomputed = False
        self.__pre_compute()
        # return self.heuristic_keys[self.current_h](state)

    def compute(self, state):
        if not self.has_been_precomputed:
            self.__pre_compute()
        domain = self.cache.domain
        goals = self.automated_planner.goals
        types = state.types
        facts = state.facts
        fact_costs = self.automated_planner.pddl.init_facts_costs(facts)
        while True:
            facts, state = self.automated_planner.pddl.get_facts_and_state(
                fact_costs, types
            )
            if self.automated_planner.satisfies(goals, state):
                costs = []
                fact_costs_str = dict([(str(k), val) for k, val in fact_costs.items()])
                for g in goals:
                    if str(g) in fact_costs_str:
                        costs.append(fact_costs_str[str(g)])
                costs.insert(0, 0)
                return self.heuristic_keys[self.current_h](costs)

            for ax in self.cache.axioms:
                fact_costs = (
                    self.automated_planner.pddl.compute_costs_one_step_derivation(
                        facts, fact_costs, ax, self.current_h
                    )
                )

            actions = self.automated_planner.available_actions(state)
            for act in actions:
                fact_costs = self.automated_planner.pddl.compute_cost_action_effect(
                    fact_costs, act, domain, self.cache.additions, self.current_h
                )

            if len(fact_costs) == self.automated_planner.pddl.length(
                facts
            ) and self.__facts_eq(fact_costs, facts):
                break

        return float("inf")

    def __pre_compute(self):
        if self.has_been_precomputed:
            return
        domain = self.automated_planner.domain
        domain, axioms = self.automated_planner.pddl.compute_hsp_axioms(domain)
        # preconditions = dict()
        additions = dict()
        self.automated_planner.pddl.cache_global_preconditions(domain)
        for name, definition in domain.actions.items():
            additions[name] = self.automated_planner.pddl.effect_diff(
                definition.effect
            ).add
        self.cache.additions = additions
        self.cache.preconds = self.automated_planner.pddl.g_preconditions
        self.cache.domain = domain
        self.cache.axioms = axioms
        self.has_been_precomputed = True

    def __h_add(self, costs):
        return sum(costs)

    def __h_max(self, costs):
        return max(costs)

    def __facts_eq(self, facts_dict, facts_set):
        fact_costs_str = dict([(str(k), val) for k, val in facts_dict.items()])
        for f in facts_set:
            if not (str(f) in fact_costs_str.keys()):
                return False
        return True


class RelaxedCriticalPathHeuristic:
    def __init__(self, automated_planner, critical_path_level=1):
        class RCPCache:
            def __init__(self, domain=None, axioms=None, preconds=None, additions=None):
                self.domain = domain
                self.axioms = axioms
                self.preconds = preconds
                self.additions = additions

        self.automated_planner = automated_planner
        self.cache = RCPCache()
        if critical_path_level > 3:
            logging.warning(
                "Critical Path level is only implemented until 3, forcing it to 3."
            )
            self.critical_path_level = 3
        if critical_path_level < 1:
            logging.warning(
                "Critical Path level has to be at least 1, forcing it to 1."
            )
            self.critical_path_level = 1
        else:
            self.critical_path_level = critical_path_level
        self.has_been_precomputed = False
        self.__pre_compute()
        # return self.heuristic_keys[self.current_h](state)

    def compute(self, state):
        if not self.has_been_precomputed:
            self.__pre_compute()
        domain = self.cache.domain
        goals = self.automated_planner.goals
        types = state.types
        facts = state.facts
        fact_costs = self.automated_planner.pddl.init_facts_costs(facts)
        while True:
            facts, state = self.automated_planner.pddl.get_facts_and_state(
                fact_costs, types
            )
            if self.automated_planner.satisfies(goals, state):
                costs = []
                fact_costs_str = dict([(str(k), val) for k, val in fact_costs.items()])
                print(fact_costs_str)
                if self.critical_path_level == 1:
                    for g in goals:
                        if str(g) in fact_costs_str:
                            costs.append(fact_costs_str[str(g)])
                if self.critical_path_level == 2:
                    pairs_of_goals = [
                        (g1, g2) for g1 in goals for g2 in goals if g1 != g2
                    ]
                    for gs in pairs_of_goals:
                        if (
                            str(gs[0]) in fact_costs_str
                            and str(gs[1]) in fact_costs_str
                        ):
                            costs.append(
                                fact_costs_str[str(gs[0])] + fact_costs_str[str(gs[1])]
                            )
                if self.critical_path_level == 3:
                    triplets_of_goals = [
                        (g1, g2, g3)
                        for g1 in goals
                        for g2 in goals
                        for g3 in goals
                        if g1 != g2 and g1 != g3 and g2 != g3
                    ]
                    for gs in triplets_of_goals:
                        if (
                            str(gs[0]) in fact_costs_str
                            and str(gs[1]) in fact_costs_str
                            and str(gs[2]) in fact_costs_str
                        ):
                            costs.append(
                                fact_costs_str[str(gs[0])]
                                + fact_costs_str[str(gs[1])]
                                + fact_costs_str[str(gs[2])]
                            )
                costs.insert(0, 0)
                return max(costs)

            for ax in self.cache.axioms:
                fact_costs = (
                    self.automated_planner.pddl.compute_costs_one_step_derivation(
                        facts, fact_costs, ax, "max"
                    )
                )

            actions = self.automated_planner.available_actions(state)
            for act in actions:
                fact_costs = self.automated_planner.pddl.compute_cost_action_effect(
                    fact_costs, act, domain, self.cache.additions, "max"
                )

            if len(fact_costs) == self.automated_planner.pddl.length(
                facts
            ) and self.__facts_eq(fact_costs, facts):
                break

        return float("inf")

    def __pre_compute(self):
        if self.has_been_precomputed:
            return
        domain = self.automated_planner.domain
        domain, axioms = self.automated_planner.pddl.compute_hsp_axioms(domain)
        # preconditions = dict()
        additions = dict()
        self.automated_planner.pddl.cache_global_preconditions(domain)
        for name, definition in domain.actions.items():
            additions[name] = self.automated_planner.pddl.effect_diff(
                definition.effect
            ).add
        self.cache.additions = additions
        self.cache.preconds = self.automated_planner.pddl.g_preconditions
        self.cache.domain = domain
        self.cache.axioms = axioms
        self.has_been_precomputed = True

    def __h_add(self, costs):
        return sum(costs)

    def __h_max(self, costs):
        return max(costs)

    def __facts_eq(self, facts_dict, facts_set):
        fact_costs_str = dict([(str(k), val) for k, val in facts_dict.items()])
        for f in facts_set:
            if not (str(f) in fact_costs_str.keys()):
                return False
        return True


class CriticalPathHeuristic:
    def __init__(self, automated_planner, critical_path_level=1):
        self.automated_planner = automated_planner

        if critical_path_level > 3:
            logging.warning(
                "Critical Path level is only implemented until 3, forcing it to 3."
            )
            self.critical_path_level = 3
        if critical_path_level < 1:
            logging.warning(
                "Critical Path level has to be at least 1, forcing it to 1."
            )
            self.critical_path_level = 1
        else:
            self.critical_path_level = critical_path_level

        self.goals = []

        if self.critical_path_level == 1:
            self.goals = self.automated_planner.goals

        if self.critical_path_level == 2:
            if len(self.automated_planner.goals) < 2:
                logging.warning("Only 1 goal predicate, forcing H2 to H1")
                self.goals = self.automated_planner.goals
            else:
                self.goals = [
                    [g1, g2]
                    for g1 in self.automated_planner.goals
                    for g2 in self.automated_planner.goals
                    if g1 != g2
                ]

        if self.critical_path_level == 3:
            if len(self.automated_planner.goals) < 2:
                logging.warning("Only 1 goal predicate, forcing H3 to H1")
                self.goals = self.automated_planner.goals
            elif len(self.automated_planner.goals) < 3:
                logging.warning("Only 2 goal predicate, forcing H3 to H2")
                self.goals = [
                    [g1, g2]
                    for g1 in self.automated_planner.goals
                    for g2 in self.automated_planner.goals
                    if g1 != g2
                ]
            else:
                self.goals = [
                    [g1, g2, g3]
                    for g1 in self.automated_planner.goals
                    for g2 in self.automated_planner.goals
                    for g3 in self.automated_planner.goals
                    if g1 != g2 and g1 != g3 and g2 != g3
                ]

    def __h_max(self, costs):
        return max(costs)

    def compute(self, state):
        costs = []

        for subgoal in self.goals:
            costs.append(self.__dijkstra_search(state, subgoal))

        return self.__h_max(costs)

    def __hash(self, node):
        sep = ", Dict{Symbol,Any}"
        string = str(node.state)
        return string.split(sep, 1)[0] + ")"

    def __dijkstra_search(self, state, goal):
        def zero_heuristic():
            return 0

        init = Node(
            state,
            self.automated_planner,
            is_closed=False,
            is_open=True,
            heuristic=zero_heuristic,
        )

        open_nodes_n = 1
        nodes = dict()
        nodes[self.__hash(init)] = init

        while open_nodes_n > 0:
            current_key = min(
                [n for n in nodes if nodes[n].is_open],
                key=(lambda k: nodes[k].f_cost),
            )
            current_node = nodes[current_key]

            if self.automated_planner.satisfies(goal, current_node.state):
                return current_node.g_cost

            current_node.is_closed = True
            current_node.is_open = False
            open_nodes_n -= 1

            actions = self.automated_planner.available_actions(current_node.state)

            for act in actions:
                child = Node(
                    state=self.automated_planner.transition(current_node.state, act),
                    automated_planner=self.automated_planner,
                    parent_action=act,
                    parent=current_node,
                    heuristic=zero_heuristic,
                    is_closed=False,
                    is_open=True,
                )

                child_hash = self.__hash(child)

                if child_hash in nodes:
                    if nodes[child_hash].is_closed:
                        continue

                    if not nodes[child_hash].is_open:
                        nodes[child_hash] = child
                        open_nodes_n += 1

                    else:
                        if child.g_cost < nodes[child_hash].g_cost:
                            nodes[child_hash] = child
                            open_nodes_n += 1

                else:
                    nodes[child_hash] = child
                    open_nodes_n += 1
            return float("inf")
