class Metrics:
    def __init__(self):
        self.runtime = 0
        self.heuristic_runtimes = []
        self.n_expended = 0
        self.n_reopened = 0
        self.n_evaluated = 0
        self.n_opened = 1
        self.n_generated = 1
        self.deadend_states = 0
        self.total_cost = 0

    def get_average_heuristic_runtime(self):
        if self.heuristic_runtimes:
            return sum(self.heuristic_runtimes) / len(self.heuristic_runtimes)
        return 0

    def __str__(self):
        if self.heuristic_runtimes:
            av = sum(self.heuristic_runtimes)
            w = sum(self.heuristic_runtimes) / self.runtime * 100
        else:
            av = 0
            w = 0
        return "Expanded %d state(s).\nOpened %d state(s).\nReopened %d state(s).\nEvaluated %d state(s).\nGenerated %d state(s).\nDead ends: %d state(s).\nRuntime: %.2fs.\nTotal heuristic runtime: %.2fs\nComputational weight of heuristic in the search: %.2f%%" % (
            self.n_expended,
            self.n_opened,
            self.n_reopened,
            self.n_evaluated,
            self.n_generated,
            self.deadend_states,
            self.runtime,
            av,
            w,
        )
