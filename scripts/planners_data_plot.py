from astar_data_plot import gather_data_astar
from bfs_data_plot import gather_data_bfs
from dfs_data_plot import gather_data_dfs
from dijkstra_data_plot import gather_data_dijkstra
from common import plt
import logging
import json
from os import path


def gather_data(
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
        gatherers.append(("BFS", gather_data_bfs))
    if dfs:
        gatherers.append(("DFS", gather_data_dfs))
    if dijkstra:
        gatherers.append(("Dijkstra", gather_data_dijkstra))
    if astar:
        gatherers.append(("A*", gather_data_astar))

    _, _, _ = gather_data_bfs(
        domain_path=domain, problem_path=problem
    )  # Dummy line to do first parsing and get rid of static loading
    for name, g in gatherers:
        if g == gather_data_astar:
            times, nodes, _ = gather_data_astar(
                domain_path=domain, problem_path=problem, heuristic_key=heuristic_key
            )
        else:
            times, nodes, _ = g(domain_path=domain, problem_path=problem)
        ydata[name] = times
        xdata[name] = nodes
    return xdata, ydata


def comparative_data_plot(
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
        xdata, ydata = gather_data(
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
            xdata, ydata = gather_data(
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
    plt.show()


if __name__ == "__main__":
    logging.info("Gathering data from selected planners for complexity comparison...")
    comparative_data_plot(collect_new_data=True)
