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
    res = dfs.search()
    assert res[1] != 0  # Path, computation time, opened nodes


def test_search_bfs():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    bfs = BreadthFirstSearch(apla)
    res = bfs.search()  # Path, computation time, opened nodes
    assert res[1] != 0


def test_search_dijkstra():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    dijk = DijkstraBestFirstSearch(apla)
    res = dijk.search()  # Goal, computation_time, opened_nodes(in this order)
    assert res[1] != 0  # Assert that it took some time to compute
    assert res[-1] > 0  # Assert that it visited some nodes


def test_search_dijkstra_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    dijk = DijkstraBestFirstSearch(apla)
    res = dijk.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not res[0]


def test_search_dfs_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    dfs = DepthFirstSearch(apla)
    res = dfs.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not res[0]


def test_search_bfs_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    bfs = BreadthFirstSearch(apla)
    res = bfs.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not res[0]


def test_search_astar_basic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    res = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert res[1] != 0  # Assert that it took time to compute
    assert res[-1] > 0  # Assert that it visited at least one node


def test_search_astar_basic_no_path():
    apla = AutomatedPlanner(
        "pddl-examples/vehicle/domain.pddl", "pddl-examples/vehicle/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    res = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert not res[0]


def test_zero_heuristic():
    assert zero_heuristic() == 0
