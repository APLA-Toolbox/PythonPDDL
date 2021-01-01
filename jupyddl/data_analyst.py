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
                    path, total_time, opened_nodes = apla.astar_best_first_search(
                        heuristic_key=heuristic_key
                    )
                else:
                    logging.critical(
                        "Heuristic is not implemented! (Key not found in registered heuristics dict)"
                    )
                    return [0], [0], has_multiple_files_tested
                if path:
                    metrics[total_time] = opened_nodes
                else:
                    metrics[0] = 0

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        if heuristic_key in apla.available_heuristics:
            path, total_time, opened_nodes = apla.astar_best_first_search(
                heuristic_key=heuristic_key
            )
        else:
            logging.critical(
                "Heuristic is not implemented! (Key not found in registered heuristics dict)"
            )
            return [0], [0], has_multiple_files_tested
        if path:
            return [total_time], [opened_nodes], has_multiple_files_tested
        return [0], [0], has_multiple_files_tested

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
        times, total_nodes, has_multiple_files_tested = self.__gather_data_astar(
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

    def __gather_data_bfs(self, domain_path="", problem_path="", max_pddl_instances=-1):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            metrics = dict()
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug("Loading new PDDL instance planned with BFS...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                path, total_time, opened_nodes = apla.breadth_first_search()
                if path:
                    metrics[total_time] = opened_nodes
                else:
                    metrics[0] = 0

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        path, total_time, opened_nodes = apla.breadth_first_search()
        if path:
            return [total_time], [opened_nodes], has_multiple_files_tested
        return [0], [0], has_multiple_files_tested

    def plot_bfs(self, domain="", problem="", max_pddl_instances=-1):
        title = "BFS Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_bfs(
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
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug("Loading new PDDL instance planned with DFS...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                path, total_time, opened_nodes = apla.depth_first_search()
                if path:
                    metrics[total_time] = opened_nodes
                else:
                    metrics[0] = 0

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        path, total_time, opened_nodes = apla.depth_first_search()
        if path:
            return [total_time], [opened_nodes], has_multiple_files_tested
        return [0], [0], has_multiple_files_tested

    def plot_dfs(self, problem="", domain="", max_pddl_instances=-1):
        title = "DFS Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_dfs(
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
            for problem, domain in self.__get_all_pddl_from_data(
                max_pddl_instances=max_pddl_instances
            ):
                logging.debug("Loading new PDDL instance planned with Dijkstra...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                path, total_time, opened_nodes = apla.dijktra_best_first_search()
                if path:
                    metrics[total_time] = opened_nodes
                else:
                    metrics[0] = 0

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        has_multiple_files_tested = False
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        path, total_time, opened_nodes = apla.dijktra_best_first_search()
        if path:
            return [total_time], [opened_nodes], has_multiple_files_tested
        return [0], [0], has_multiple_files_tested

    def plot_dijkstra(self, problem="", domain="", max_pddl_instances=-1):
        title = "Dijkstra Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_dijkstra(
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

        _, _, _ = self.__gather_data_bfs(
            domain_path=domain, problem_path=problem
        )  # Dummy line to do first parsing and get rid of static loading
        for name, g in gatherers:
            if g == self.__gather_data_astar:
                times, nodes, _ = self.__gather_data_astar(
                    domain_path=domain,
                    problem_path=problem,
                    heuristic_key=heuristic_key,
                    max_pddl_instances=max_pddl_instances,
                )
            else:
                times, nodes, _ = g(
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
            times, nodes, _ = self.__gather_data_astar(
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
                nodes_sorted, times_y, "-o", label=h,
            )

        plt.title("A* heuristics complexity comparison")
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
                nodes_sorted, times_y, "-o", label=planner,
            )
        plt.title("Planners complexity comparison")
        plt.legend(loc="upper left")
        plt.xscale("symlog")
        plt.yscale("log")
        plt.grid(True)
        plt.show(block=False)
