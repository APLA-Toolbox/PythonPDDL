import os
import glob
import matplotlib as mpl
import logging

if "DISPLAY" not in os.environ:
    mpl.use("agg")
else:
    mpl.use("TkAgg")
mpl.set_loglevel("WARNING")
import matplotlib.pyplot as plt

plt.style.use("ggplot")
from .automated_planner import AutomatedPlanner
from os import path
import json


class DataAnalyst:
    def __init__(self):
        logging.info("Instantiating data analyst...")
        self.available_heuristics = [
            "basic/goal_count",
            "basic/zero",
            "delete_relaxation/h_add",
            "delete_relaxation/h_max",
        ]

    def __get_all_pddl_from_data(self, max_pddl_instances=-1):
        tested_files = []
        domains_problems = []
        i = 0
        if "DISPLAY" in os.environ:
            for root, _, files in os.walk("pddl-examples/", topdown=False):
                for name in files:
                    # if "README" in name:
                    #    continue
                    # if "LICENSE" in name:
                    #    continue
                    # if ".gitignore" in name:
                    #    continue
                    tested_files.append(os.getcwd() + "/" + os.path.join(root, name))
                    if i % 2 != 0:
                        domains_problems.append((tested_files[i - 1], tested_files[i]))
                    i += 1
                    if max_pddl_instances != -1 and i >= max_pddl_instances * 2:
                        return domains_problems
            return domains_problems
        return [
            ("pddl-examples/dinner/problem.pddl", "pddl-examples/dinner/domain.pddl"),
            ("pddl-examples/dinner/problem.pddl", "pddl-examples/dinner/domain.pddl"),
        ]

    def __plot_data(self, times, total_nodes, plot_title):
        data = dict()
        for i, val in enumerate(total_nodes):
            data[val] = times[i]
        nodes_sorted = sorted(list(data.keys()))
        times_y = []
        for node_opened in nodes_sorted:
            times_y.append(data[node_opened])
        plt.plot(nodes_sorted, times_y, "r:o")
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time (s)")
        plt.xscale("symlog")
        plt.title(plot_title)
        plt.grid(True)
        plt.show(block=False)

    def __plot_data_generic(self, data, name):
        _, ax = plt.subplots()
        plt.xlabel("Domain")
        plt.ylabel(name)
        for key, val in data.items():
            ax.plot(val[name], "-o", label=key)

        plt.title("Planners metric comparison")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.show(block=False)

    def __scatter_data(self, times, total_nodes, plot_title):
        plt.scatter(total_nodes, times)
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time (s)")
        plt.xscale("symlog")
        plt.title(plot_title)
        plt.grid(True)
        plt.show(block=False)

    def __gather_data_astar(
        self,
        domain_path="",
        problem_path="",
        heuristic_key="basic/goal_count",
        max_pddl_instances=-1,
    ):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            metrics = dict()
            costs = []
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug(
                    "Loading new PDDL instance planned with A* [ "
                    + heuristic_key
                    + " ]"
                )
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                if heuristic_key in apla.available_heuristics:
                    path, metrics_obj = apla.astar_best_first_search(
                        heuristic_key=heuristic_key
                    )
                else:
                    logging.critical(
                        "Heuristic is not implemented! (Key not found in registered heuristics dict)"
                    )
                    return [0], [0], [0], has_multiple_files_tested
                if path:
                    metrics[metrics_obj.runtime] = metrics_obj.n_opened
                    costs.append(path[-1].g_cost)
                else:
                    metrics[0] = 0
                    costs.append(0)

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return costs, times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        if heuristic_key in apla.available_heuristics:
            path, metrics_obj = apla.astar_best_first_search(
                heuristic_key=heuristic_key
            )
        else:
            logging.critical(
                "Heuristic is not implemented! (Key not found in registered heuristics dict)"
            )
            return [0], [0], [0], has_multiple_files_tested
        if path:
            return (
                [path[-1].g_cost],
                [metrics_obj.runtime],
                [metrics_obj.n_opened],
                has_multiple_files_tested,
            )
        return [0], [0], [0], has_multiple_files_tested

    def plot_astar(
        self,
        heuristic_key="basic/goal_count",
        domain="",
        problem="",
        max_pddl_instances=-1,
    ):
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        _, times, total_nodes, has_multiple_files_tested = self.__gather_data_astar(
            heuristic_key=heuristic_key,
            problem_path=problem,
            domain_path=domain,
            max_pddl_instances=max_pddl_instances,
        )
        title = "A* Statistics" + "[Heuristic: " + heuristic_key + "]"
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_greedy_bfs(
        self,
        domain_path="",
        problem_path="",
        heuristic_key="basic/goal_count",
        max_pddl_instances=-1,
    ):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            metrics = dict()
            costs = []
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug(
                    "Loading new PDDL instance planned with A* [ "
                    + heuristic_key
                    + " ]"
                )
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                if heuristic_key in apla.available_heuristics:
                    path, metrics_obj = apla.greedy_best_first_search(
                        heuristic_key=heuristic_key
                    )
                else:
                    logging.critical(
                        "Heuristic is not implemented! (Key not found in registered heuristics dict)"
                    )
                    return [0], [0], [0], has_multiple_files_tested
                if path:
                    metrics[metrics_obj.runtime] = metrics_obj.n_opened
                    costs.append(path[-1].g_cost)
                else:
                    metrics[0] = 0
                    costs.append(0)

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return costs, times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        if heuristic_key in apla.available_heuristics:
            path, metrics_obj = apla.greedy_best_first_search(
                heuristic_key=heuristic_key
            )
        else:
            logging.critical(
                "Heuristic is not implemented! (Key not found in registered heuristics dict)"
            )
            return [0], [0], [0], has_multiple_files_tested
        if path:
            return (
                [path[-1].g_cost],
                [metrics_obj.runtime],
                [metrics_obj.n_opened],
                has_multiple_files_tested,
            )
        return [0], [0], [0], has_multiple_files_tested

    def plot_greedy_bfs(
        self,
        heuristic_key="basic/goal_count",
        domain="",
        problem="",
        max_pddl_instances=-1,
    ):
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        (
            _,
            times,
            total_nodes,
            has_multiple_files_tested,
        ) = self.__gather_data_greedy_bfs(
            heuristic_key=heuristic_key,
            problem_path=problem,
            domain_path=domain,
            max_pddl_instances=max_pddl_instances,
        )
        title = (
            "Greedy Best First Search Statistics" + "[Heuristic: " + heuristic_key + "]"
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_bfs(self, domain_path="", problem_path="", max_pddl_instances=-1):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            metrics = dict()
            costs = []
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug("Loading new PDDL instance planned with BFS...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                path, metrics_obj = apla.breadth_first_search()
                if path:
                    metrics[metrics_obj.runtime] = metrics_obj.n_opened
                    costs.append(path[-1].g_cost)
                else:
                    metrics[0] = 0
                    costs.append(0)

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return costs, times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        path, metrics_obj = apla.breadth_first_search()
        if path:
            return (
                [path[-1].g_cost],
                [metrics_obj.runtime],
                [metrics_obj.n_opened],
                has_multiple_files_tested,
            )
        return [0], [0], [0], has_multiple_files_tested

    def plot_bfs(self, domain="", problem="", max_pddl_instances=-1):
        title = "BFS Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        _, times, total_nodes, has_multiple_files_tested = self.__gather_data_bfs(
            problem_path=problem,
            domain_path=domain,
            max_pddl_instances=max_pddl_instances,
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_dfs(self, domain_path="", problem_path="", max_pddl_instances=-1):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            metrics = dict()
            costs = []
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug("Loading new PDDL instance planned with DFS...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                path, metrics_obj = apla.depth_first_search()
                if path:
                    metrics[metrics_obj.runtime] = metrics_obj.n_opened
                    costs.append(path[-1].g_cost)
                else:
                    metrics[0] = 0
                    costs.append(0)

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return costs, times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        path, metrics_obj = apla.depth_first_search()
        if path:
            return (
                [path[-1].g_cost],
                [metrics_obj.runtime],
                [metrics_obj.n_opened],
                has_multiple_files_tested,
            )
        return [0], [0], [0], has_multiple_files_tested

    def plot_dfs(self, problem="", domain="", max_pddl_instances=-1):
        title = "DFS Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        _, times, total_nodes, has_multiple_files_tested = self.__gather_data_dfs(
            problem_path=problem,
            domain_path=domain,
            max_pddl_instances=max_pddl_instances,
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_dijkstra(
        self, domain_path="", problem_path="", max_pddl_instances=-1
    ):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            metrics = dict()
            costs = []
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug("Loading new PDDL instance planned with Dijkstra...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                path, metrics_obj = apla.dijktra_best_first_search()
                if path:
                    metrics[metrics_obj.runtime] = metrics_obj.n_opened
                    costs.append(path[-1].g_cost)
                else:
                    metrics[0] = 0
                    costs.append(0)

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return costs, times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        path, metrics_obj = apla.dijktra_best_first_search()
        if path:
            return (
                [path[-1].g_cost],
                [metrics_obj.runtime],
                [metrics_obj.n_opened],
                has_multiple_files_tested,
            )
        return [0], [0], [0], has_multiple_files_tested

    def plot_dijkstra(self, problem="", domain="", max_pddl_instances=-1):
        title = "Dijkstra Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        _, times, total_nodes, has_multiple_files_tested = self.__gather_data_dijkstra(
            problem_path=problem,
            domain_path=domain,
            max_pddl_instances=max_pddl_instances,
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data(
        self,
        heuristic_key="basic/goal_count",
        astar=True,
        bfs=True,
        dfs=True,
        dijkstra=True,
        greedy_bfs=False,
        domain="",
        problem="",
        max_pddl_instances=-1,
    ):
        gatherers = []
        xdata = dict()
        ydata = dict()

        if bfs:
            gatherers.append(("BFS", self.__gather_data_bfs))
        if dfs:
            gatherers.append(("DFS", self.__gather_data_dfs))
        if dijkstra:
            gatherers.append(("Dijkstra", self.__gather_data_dijkstra))
        if astar:
            gatherers.append(("A*", self.__gather_data_astar))
        if greedy_bfs:
            gatherers.append(("Greedy Best First", self.__gather_data_greedy_bfs))

        _, _, _, _ = self.__gather_data_bfs(
            domain_path=domain, problem_path=problem
        )  # Dummy line to do first parsing and get rid of static loading
        for name, g in gatherers:
            if g == self.__gather_data_astar or g == self.__gather_data_greedy_bfs:
                _, times, nodes, _ = g(
                    domain_path=domain,
                    problem_path=problem,
                    heuristic_key=heuristic_key,
                    max_pddl_instances=max_pddl_instances,
                )
            else:
                _, times, nodes, _ = g(
                    domain_path=domain,
                    problem_path=problem,
                    max_pddl_instances=max_pddl_instances,
                )
            ydata[name] = times
            xdata[name] = nodes
        return xdata, ydata

    def comparative_astar_heuristic_plot(
        self, domain="", problem="", max_pddl_instances=-1
    ):
        _, ax = plt.subplots()
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time (s)")

        for h in self.available_heuristics:
            _, times, nodes, _ = self.__gather_data_astar(
                domain_path=domain,
                problem_path=problem,
                heuristic_key=h,
                max_pddl_instances=max_pddl_instances,
            )
            data = dict()
            for i, val in enumerate(nodes):
                data[val] = times[i]
            nodes_sorted = sorted(list(data.keys()))
            times_y = []
            for node_opened in nodes_sorted:
                times_y.append(data[node_opened])

            ax.plot(
                nodes_sorted,
                times_y,
                "-o",
                label=h,
            )

        plt.title("A* heuristics complexity comparison")
        plt.legend(loc="upper left")
        plt.xscale("symlog")
        plt.grid(True)
        plt.show(block=False)

    def comparative_greedy_bfs_heuristic_plot(
        self, domain="", problem="", max_pddl_instances=-1
    ):
        _, ax = plt.subplots()
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time (s)")

        for h in self.available_heuristics:
            _, times, nodes, _ = self.__gather_data_greedy_bfs(
                domain_path=domain,
                problem_path=problem,
                heuristic_key=h,
                max_pddl_instances=max_pddl_instances,
            )
            data = dict()
            for i, val in enumerate(nodes):
                data[val] = times[i]
            nodes_sorted = sorted(list(data.keys()))
            times_y = []
            for node_opened in nodes_sorted:
                times_y.append(data[node_opened])

            ax.plot(
                nodes_sorted,
                times_y,
                "-o",
                label=h,
            )

        plt.title("Greedy Best First heuristics complexity comparison")
        plt.legend(loc="upper left")
        plt.xscale("symlog")
        plt.grid(True)
        plt.show(block=False)

    def comparative_data_plot(
        self,
        astar=True,
        bfs=True,
        dfs=True,
        dijkstra=True,
        greedy_bfs=False,
        domain="",
        problem="",
        heuristic_key="basic/goal_count",
        collect_new_data=True,
        max_pddl_instances=-1,
    ):
        json_dict = {}
        if collect_new_data:
            xdata, ydata = self.__gather_data(
                heuristic_key=heuristic_key,
                astar=astar,
                dfs=dfs,
                bfs=bfs,
                dijkstra=dijkstra,
                greedy_bfs=greedy_bfs,
                domain=domain,
                problem=problem,
                max_pddl_instances=max_pddl_instances,
            )
            json_dict["xdata"] = xdata
            json_dict["ydata"] = ydata
            with open("data.json", "w") as fp:
                json.dump(json_dict, fp)
        else:
            if not path.exists("data.json"):
                logging.warning(
                    "Input says not to generate new data but no data was found. Generating new data..."
                )
                xdata, ydata = self.__gather_data(
                    heuristic_key=heuristic_key,
                    astar=astar,
                    dfs=dfs,
                    bfs=bfs,
                    greedy_bfs=greedy_bfs,
                    dijkstra=dijkstra,
                    domain=domain,
                    problem=problem,
                    max_pddl_instances=max_pddl_instances,
                )
                json_dict["xdata"] = xdata
                json_dict["ydata"] = ydata
                with open("data.json", "w") as fp:
                    json.dump(json_dict, fp)
            else:
                with open("data.json") as fp:
                    json_dict = json.load(fp)

        _, ax = plt.subplots()
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time (s)")
        for planner in json_dict["xdata"].keys():
            data = dict()
            for i, val in enumerate(json_dict["xdata"][planner]):
                data[val] = json_dict["ydata"][planner][i]
            nodes_sorted = sorted(list(data.keys()))
            times_y = []
            for node_opened in nodes_sorted:
                times_y.append(data[node_opened])
            ax.plot(
                nodes_sorted,
                times_y,
                "-o",
                label=planner,
            )
        plt.title("Planners complexity comparison")
        plt.legend(loc="upper left")
        plt.xscale("symlog")
        plt.yscale("log")
        plt.grid(True)
        plt.show(block=False)

    def plot_metrics(self):
        metrics_dict = dict()
        metrics_dict["A* [Zero]"] = []
        metrics_dict["DFS"] = []
        metrics_dict["BFS"] = []
        metrics_dict["A* [Goal_Count]"] = []
        metrics_dict["A* [H_Add]"] = []
        metrics_dict["A* [H_Max]"] = []
        metrics_dict["A* [Critical_Path (H2)]"] = []
        metrics_dict["A* [Critical_Path (H3)]"] = []
        logging.debug("Computation of all metrics for all domains registered...")
        for problem, domain in self.__get_all_pddl_from_data():
            logging.debug("Loading new PDDL instance planned with Dijkstra...")
            logging.debug("Domain: " + domain)
            logging.debug("Problem: " + problem)
            apla = AutomatedPlanner(domain, problem)
            _, metrics_bfs = apla.breadth_first_search()
            _, metrics_agc = apla.astar_best_first_search()
            _, metrics_ahadd = apla.astar_best_first_search(
                heuristic_key="delete_relaxation/h_add"
            )
            _, metrics_ahmax = apla.astar_best_first_search(
                heuristic_key="delete_relaxation/h_max"
            )
            _, metrics_dij = apla.astar_best_first_search(heuristic_key="basic/zero")
            _, metrics_dfs = apla.depth_first_search(
                node_bound=metrics_bfs.n_opened * 2
            )
            _, metrics_cp2 = apla.astar_best_first_search(
                heuristic_key="critical_path/2"
            )
            _, metrics_cp3 = apla.astar_best_first_search(
                heuristic_key="critical_path/3"
            )
            metrics_dict["A* [Zero]"].append(metrics_dij)
            metrics_dict["DFS"].append(metrics_dfs)
            metrics_dict["BFS"].append(metrics_bfs)
            metrics_dict["A* [Goal_Count]"].append(metrics_agc)
            metrics_dict["A* [H_Add]"].append(metrics_ahadd)
            metrics_dict["A* [H_Max]"].append(metrics_ahmax)
            metrics_dict["A* [Critical_Path (H2)]"].append(metrics_cp2)
            metrics_dict["A* [Critical_Path (H3)]"].append(metrics_cp3)

        plot_dict = dict()

        for key, val in metrics_dict.items():
            plot_dict[key] = dict()
            plot_dict[key]["Search Runtime (s)"] = [m.runtime for m in val]
            plot_dict[key]["Total Heuristics Runtime (s)"] = [
                sum(m.heuristic_runtimes) for m in val
            ]
            plot_dict[key]["Number of Expanded Nodes"] = [m.n_expended for m in val]
            plot_dict[key]["Number of Opened Nodes"] = [m.n_opened for m in val]
            plot_dict[key]["Number of Reopened Nodes"] = [m.n_reopened for m in val]
            plot_dict[key]["Number of Evaluated Nodes"] = [m.n_evaluated for m in val]
            plot_dict[key]["Number of Generated Nodes"] = [m.n_generated for m in val]
            plot_dict[key]["Number of Deadend States (No Actions from State)"] = [
                m.deadend_states for m in val
            ]

        metrics_keys = list(plot_dict["DFS"].keys())

        for key in metrics_keys:
            self.__plot_data_generic(plot_dict, key)

    def compute_planners_efficiency(self):
        costs = dict()
        costs["A* [Goal_Count]"], _, n_goal_count, _ = self.__gather_data_astar()
        costs["A* [H_Max]"], _, n_hmax, _ = self.__gather_data_astar(
            heuristic_key="delete_relaxation/h_max"
        )
        costs["A* [H_Add]"], _, n_hadd, _ = self.__gather_data_astar(
            heuristic_key="delete_relaxation/h_add"
        )
        (
            costs["Greedy Best First [Goal_Count]"],
            _,
            n_greed_goal_count,
            _,
        ) = self.__gather_data_greedy_bfs(heuristic_key="basic/goal_count")
        (
            costs["Greedy Best First [H_Max]"],
            _,
            n_greed_hmax,
            _,
        ) = self.__gather_data_greedy_bfs(heuristic_key="delete_relaxation/h_max")
        (
            costs["Greedy Best First [H_Add]"],
            _,
            n_greed_hadd,
            _,
        ) = self.__gather_data_greedy_bfs(heuristic_key="delete_relaxation/h_add")
        costs["DFS"], _, n_dfs, _ = self.__gather_data_dfs()
        costs["BFS"], _, n_bfs, _ = self.__gather_data_bfs()
        costs["Dijkstra"], _, n_dij, _ = self.__gather_data_dijkstra()

        p_gc = (len(n_goal_count) - n_goal_count.count(0)) / len(n_goal_count) * 100
        p_hmax = (len(n_hmax) - n_hmax.count(0)) / len(n_hmax) * 100
        p_hadd = (len(n_hadd) - n_hadd.count(0)) / len(n_hadd) * 100
        p_greedy_gc = (
            (len(n_greed_goal_count) - n_greed_goal_count.count(0))
            / len(n_greed_goal_count)
            * 100
        )
        p_greedy_hmax = (
            (len(n_greed_hmax) - n_greed_hmax.count(0)) / len(n_greed_hmax) * 100
        )
        p_greedy_hadd = (
            (len(n_greed_hadd) - n_greed_hadd.count(0)) / len(n_greed_hadd) * 100
        )
        p_dfs = (len(n_dfs) - n_dfs.count(0)) / len(n_dfs) * 100
        p_bfs = (len(n_bfs) - n_bfs.count(0)) / len(n_bfs) * 100
        p_dij = (len(n_dij) - n_dij.count(0)) / len(n_dij) * 100

        _, ax = plt.subplots()
        plt.xlabel("Domain evaluated")
        plt.ylabel("Cost to goal")
        for key, val in costs.items():
            ax.plot(
                val,
                "-o",
                label=key,
            )
            costs[key] = [i for i in costs[key] if i != 0]
        plt.title("Planners efficiency (costs)")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.show(block=False)

        logging.info(
            "DFS succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (p_dfs, sum(costs["DFS"]) / len(costs["DFS"]))
        )
        logging.info(
            "BFS succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (p_bfs, sum(costs["BFS"]) / len(costs["BFS"]))
        )
        logging.info(
            "Dijkstra succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (p_dij, sum(costs["Dijkstra"]) / len(costs["Dijkstra"]))
        )
        logging.info(
            "A* [Goal_Count] succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (p_gc, sum(costs["A* [Goal_Count]"]) / len(costs["A* [Goal_Count]"]))
        )
        logging.info(
            "A* [H_Max] succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (p_hmax, sum(costs["A* [H_Max]"]) / len(costs["A* [H_Max]"]))
        )
        logging.info(
            "A* [H_Add] succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (p_hadd, sum(costs["A* [H_Add]"]) / len(costs["A* [H_Add]"]))
        )
        logging.info(
            "Greedy Best First [Goal_Count] succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (
                p_greedy_gc,
                sum(costs["Greedy Best First [Goal_Count]"])
                / len(costs["Greedy Best First [Goal_Count]"]),
            )
        )
        logging.info(
            "Greedy Best First [H_Max] succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (
                p_greedy_hmax,
                sum(costs["Greedy Best First [H_Max]"])
                / len(costs["Greedy Best First [H_Max]"]),
            )
        )
        logging.info(
            "Greedy Best First [H_Add] succeeded to build a plan with a %.2f%% rate and a %.2f cost average"
            % (
                p_greedy_hadd,
                sum(costs["Greedy Best First [H_Add]"])
                / len(costs["Greedy Best First [H_Add]"]),
            )
        )
