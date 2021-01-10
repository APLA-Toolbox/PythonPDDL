from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.dijkstra import DijkstraBestFirstSearch, zero_heuristic
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.bfs import BreadthFirstSearch
from jupyddl.heuristics import BasicHeuristic, DeleteRelaxationHeuristic
from jupyddl.dfs import DepthFirstSearch
from os import path
import coloredlogs
import sys


def test_search_dfs():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    dfs = DepthFirstSearch(apla)
    path, metrics = dfs.search()
    assert path and metrics.n_evaluated > 0


def test_search_dfs_bounded():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    dfs = DepthFirstSearch(apla)
    path, _ = dfs.search(node_bound=1)
    assert not path


def test_search_bfs():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    bfs = BreadthFirstSearch(apla)
    path, metrics = bfs.search()  # Path, computation time, opened nodes
    assert path and metrics.n_evaluated > 0


def test_search_bfs_bounded():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    bfs = BreadthFirstSearch(apla)
    path, _ = bfs.search(node_bound=1)  # Path, computation time, opened nodes
    assert not path


def test_search_dijkstra():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    dijk = DijkstraBestFirstSearch(apla)
    path, metrics = dijk.search()  # Goal, computation_time, opened_nodes(in this order)
    assert path and metrics.n_evaluated > 0  # Assert that it took some time to compute


def test_search_dijkstra_bounded():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    dijk = DijkstraBestFirstSearch(apla)
    path, _ = dijk.search(
        node_bound=1
    )  # Goal, computation_time, opened_nodes(in this order)
    assert not path


def test_search_dijkstra_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    dijk = DijkstraBestFirstSearch(apla)
    path, metrics = dijk.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not path and metrics.n_evaluated > 0


def test_search_dfs_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    dfs = DepthFirstSearch(apla)
    path, metrics = dfs.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not path and metrics.n_evaluated > 0


def test_search_bfs_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    bfs = BreadthFirstSearch(apla)
    path, metrics = bfs.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not path and metrics.n_evaluated > 0


def test_search_astar_basic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    (
        path,
        metrics,
    ) = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert path and metrics.n_evaluated > 0


def test_search_astar_basic_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    (
        path,
        metrics,
    ) = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not path and metrics.n_evaluated > 0


def test_zero_heuristic():
    assert zero_heuristic() == 0
