from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.dijkstra import DijkstraBestFirstSearch
from jupyddl.a_star import AStarBestFirstSearch
from jupyddl.bfs import BreadthFirstSearch
from jupyddl.dfs import DepthFirstSearch
from os import path
import coloredlogs
import sys

def test_searchDFS():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    dfs = DepthFirstSearch(apla)
    _,ct = dfs.search()
    assert ct != 0

def test_searchBFS():
    apla = AutomatedPlanner("data/domain.pddl", "data/problem.pddl")
    bfs = BreadthFirstSearch(apla)
    _,ct = bfs.search()
    assert ct != 0
