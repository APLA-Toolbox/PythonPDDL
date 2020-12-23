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

    def __get_all_pddl_from_data(self):
        tested_files = []
        domains_problems = []
        i = 0
        if "DISPLAY" in os.environ:
            for root, _, files in os.walk("data/", topdown=False):
                for name in files:
                    if ".gitkeep" in name:
                        continue
                    tested_files.append(os.getcwd() + "/" + os.path.join(root, name))
                    if i % 2 != 0:
                        domains_problems.append((tested_files[i - 1], tested_files[i]))
                    i += 1
            return domains_problems
        return [("data/problem.pddl", "data/domain.pddl")]

    def __plot_data(self, times, total_nodes, plot_title):
        plt.plot(total_nodes, times, "b:o")
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time")
        plt.title(plot_title)
        plt.xscale("symlog")
        plt.yscale("log")
        plt.grid(True)
        plt.show(block=False)

    def __scatter_data(self, times, total_nodes, plot_title):
        plt.scatter(total_nodes, times)
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time")
        plt.title(plot_title)
        plt.xscale("symlog")
        plt.yscale("log")
        plt.grid(True)
        plt.show(block=False)

    def __gather_data_astar(
        self, domain_path="", problem_path="", heuristic_key="goal_count"
    ):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            has_multiple_files_tested = False
            metrics = dict()
            for problem, domain in self.__get_all_pddl_from_data():
                logging.debug("Loading new PDDL instance planned with A*...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                if heuristic_key in apla.available_heuristics:
                    _, total_time, opened_nodes = apla.astar_best_first_search(
                        heuristic=apla.available_heuristics[heuristic_key]
                    )
                else:
                    logging.critical(
                        "Heuristic is not implemented! (Key not found in registered heuristics dict)"
                    )
                    return [0], [0], has_multiple_files_tested
                metrics[total_time] = opened_nodes

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        if heuristic_key in apla.available_heuristics:
            _, total_time, opened_nodes = apla.astar_best_first_search(
                heuristic=apla.available_heuristics[heuristic_key]
            )
        else:
            logging.critical(
                "Heuristic is not implemented! (Key not found in registered heuristics dict)"
            )
            return [0], [0], has_multiple_files_tested
        return [total_time], [opened_nodes], has_multiple_files_tested

    def plot_astar_data(self, heuristic_key="goal_count", domain="", problem=""):
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_astar(
            heuristic_key=heuristic_key, problem_path=problem, domain_path=domain
        )
        title = "A* Statistics" + "[Heuristic: " + heuristic_key + "]"
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_bfs(self, domain_path="", problem_path=""):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            has_multiple_files_tested = False
            metrics = dict()
            for problem, domain in self.__get_all_pddl_from_data():
                logging.debug("Loading new PDDL instance planned with BFS...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                _, total_time, opened_nodes = apla.breadth_first_search()
                metrics[total_time] = opened_nodes

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        _, total_time, opened_nodes = apla.breadth_first_search()
        return [total_time], [opened_nodes], has_multiple_files_tested

    def plot_bfs(self, domain="", problem=""):
        title = "BFS Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_bfs(
            problem_path=problem, domain_path=domain
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_dfs(self, domain_path="", problem_path=""):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            has_multiple_files_tested = False
            metrics = dict()
            for problem, domain in self.__get_all_pddl_from_data():
                logging.debug("Loading new PDDL instance planned with DFS...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                _, total_time, opened_nodes = apla.depth_first_search()
                metrics[total_time] = opened_nodes

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        _, total_time, opened_nodes = apla.depth_first_search()
        return [total_time], [opened_nodes], has_multiple_files_tested

    def plot_dfs(self, problem="", domain=""):
        title = "DFS Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_dfs(
            problem_path=problem, domain_path=domain
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data_dijkstra(self, domain_path="", problem_path=""):
        has_multiple_files_tested = True
        if not domain_path or not problem_path:
            has_multiple_files_tested = False
            metrics = dict()
            for problem, domain in self.__get_all_pddl_from_data():
                logging.debug("Loading new PDDL instance planned with Dijkstra...")
                logging.debug("Domain: " + domain)
                logging.debug("Problem: " + problem)
                apla = AutomatedPlanner(domain, problem)
                _, total_time, opened_nodes = apla.dijktra_best_first_search()
                metrics[total_time] = opened_nodes

            total_nodes = list(metrics.values())
            times = list(metrics.keys())
            return times, total_nodes, has_multiple_files_tested
        logging.debug("Loading new PDDL instance...")
        logging.debug("Domain: " + domain_path)
        logging.debug("Problem: " + problem_path)
        apla = AutomatedPlanner(domain_path, problem_path)
        _, total_time, opened_nodes = apla.dijktra_best_first_search()
        return [total_time], [opened_nodes], has_multiple_files_tested

    def plot_dijkstra(self, problem="", domain=""):
        title = "Dijkstra Statistics"
        if bool(not problem) != bool(not domain):
            logging.warning(
                "Either problem or domain wasn't provided, testing all files in data folder"
            )
            problem = domain = ""
        times, total_nodes, has_multiple_files_tested = self.__gather_data_dijkstra(
            problem_path=problem, domain_path=domain
        )
        if has_multiple_files_tested:
            self.__plot_data(times, total_nodes, title)
        else:
            self.__scatter_data(times, total_nodes, title)

    def __gather_data(
        self,
        heuristic_key="goal_count",
        astar=True,
        bfs=True,
        dfs=True,
        dijkstra=True,
        domain="",
        problem="",
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
                )
            else:
                times, nodes, _ = g(domain_path=domain, problem_path=problem)
            ydata[name] = times
            xdata[name] = nodes
        return xdata, ydata

    def comparative_data_plot(
        self,
        astar=True,
        bfs=True,
        dfs=True,
        dijkstra=True,
        domain="",
        problem="",
        heuristic_key="goal_count",
        collect_new_data=True,
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
                )
                json_dict["xdata"] = xdata
                json_dict["ydata"] = ydata
                with open("data.json", "w") as fp:
                    json.dump(json_dict, fp)
            else:
                with open("data.json") as fp:
                    json_dict = json.load(fp)

        fig, ax = plt.subplots()
        fig.set_figwidth(12)
        fig.set_figheight(6)
        plt.xlabel("Number of opened nodes")
        plt.ylabel("Planning computation time (s)")
        for planner in json_dict["xdata"].keys():
            ax.plot(
                sorted(json_dict["xdata"][planner]),
                sorted(json_dict["ydata"][planner]),
                "-o",
                label=planner,
            )
        plt.title("Planners complexity comparison")
        plt.legend(loc="upper left")
        plt.xscale("symlog")
        plt.yscale("log")
        plt.grid(True)
        plt.show(block=False)
