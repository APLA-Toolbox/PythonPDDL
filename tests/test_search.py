from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.dijkstra import DijkstraBestFirstSearch
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
        "pddl-examples/flip/domain.pddl", "pddl-examples/flip/problem.pddl"
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


def test_search_astar_basic():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = BasicHeuristic(apla, "basic/goal_count")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    res = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert res[1] != 0  # Assert that it took time to compute
    assert res[-1] > 0  # Assert that it visited at least one node

def test_search_astar_delete_relaxation():
    apla = AutomatedPlanner(
        "pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl"
    )
    heuristic = DeleteRelaxationHeuristic(apla, "delete_relaxation/h_max")
    astar = AStarBestFirstSearch(apla, heuristic.compute)
    res = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert res[1] != 0  # Assert that it took time to compute
    assert res[-1] > 0  # Assert that it visited at least one node

