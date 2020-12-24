from jupyddl.heuristics import goal_count_heuristic, zero_heuristic
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.dijkstra import DijkstraBestFirstSearch
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.bfs import BreadthFirstSearch
from jupyddl.dfs import DepthFirstSearch
from os import path
import coloredlogs
import sys

apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")

def test_searchDFS():
    dfs = DepthFirstSearch(apla)
    _, ct = dfs.search()
    assert ct != 0


def test_searchBFS():
    bfs = BreadthFirstSearch(apla)
    _, ct = bfs.search()
    assert ct != 0

def test_searchDijkstra():
    dijk = DijkstraBestFirstSearch(apla)
    res = dijk.search()                        # None, computation_time, opened_nodes(in this order)
    assert(res[1] != 0)
    assert(res[-1] >= 1)

def test_searchAStar():
    astar = AStarBestFirstSearch(apla, goal_count_heuristic)
    res = astar.search()                        # None, computation_time, opened_nodes(in this order)
    assert(res[1] != 0)
    assert(res[-1] >= 1)
