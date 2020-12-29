from jupyddl.heuristics import goal_count_heuristic, zero_heuristic
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.dijkstra import DijkstraBestFirstSearch
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.bfs import BreadthFirstSearch
from jupyddl.dfs import DepthFirstSearch
from os import path
import coloredlogs
import sys

apla = AutomatedPlanner("pddl-examples/dinner/domain.pddl", "pddl-examples/dinner/problem.pddl")


def test_searchDFS():
    dfs = DepthFirstSearch(apla)
    res = dfs.search()
    assert res[1] != 0  # Path, computation time, opened nodes


def test_searchBFS():
    bfs = BreadthFirstSearch(apla)
    res = bfs.search()  # Path, computation time, opened nodes
    assert res[1] != 0


def test_searchDijkstra():
    dijk = DijkstraBestFirstSearch(apla)
    res = dijk.search()  # Goal, computation_time, opened_nodes(in this order)
    assert res[1] != 0  # Assert that it took some time to compute
    assert res[-1] > 0  # Assert that it visited some nodes


def test_searchAStar():
    astar = AStarBestFirstSearch(apla, apla.available_heuristics["goal_count"])
    res = astar.search()  # Goal, computation_time, opened_nodes(in this order)
    assert res[1] != 0  # Assert that it took time to compute
    assert res[-1] > 0  # Assert that it visited at least one node
