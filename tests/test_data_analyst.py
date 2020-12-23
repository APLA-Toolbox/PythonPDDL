# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.data_analyst import DataAnalyst

def test_data_analyst_constructor():
    _ = DataAnalyst()
    assert(True)

def test_data_analyst_plot_dfs():
    da = DataAnalyst()
    da.plot_dfs()
    assert(True)

def test_data_analyst_plot_bfs():
    da = DataAnalyst()
    da.plot_bfs()
    assert(True)

def test_data_analyst_plot_dijkstra():
    da = DataAnalyst()
    da.plot_dijkstra()
    assert(True)

def test_data_analyst_plot_astar_h_goal_count():
    da = DataAnalyst()
    da.plot_astar_data()
    assert(True)

def test_data_analyst_plot_astar_h_zero():
    da = DataAnalyst()
    da.plot_astar_data(heuristic_key="zero")
    assert(True)

def test_comparative_no_restrictions():
    da = DataAnalyst()
    da.comparative_data_plot()
    assert(True)

def test_comparative_no_astar():
    da = DataAnalyst()
    da.comparative_data_plot(astar=False)
    assert(True)

def test_comparative_no_bfs():
    da = DataAnalyst()
    da.comparative_data_plot(bfs=False)
    assert(True)

def test_comparative_no_dijkstra():
    da = DataAnalyst()
    da.comparative_data_plot(dijkstra=False)
    assert(True)

def test_comparative_no_dfs():
    da = DataAnalyst()
    da.comparative_data_plot(dfs=False)
    assert(True)

def test_comparative_one_pddl():
    da = DataAnalyst()
    da.comparative_data_plot(dfs=False, bfs=False, domain="data/domain.pddl", problem="data/problem.pddl")
    assert(True)

def test_comparative_use_data_json():
    da = DataAnalyst()
    da.comparative_data_plot(domain="data/domain.pddl", problem="data/problem.pddl", collect_new_data=False)
    assert(True)

def test_comparative_zero_h():
    da = DataAnalyst()
    da.comparative_data_plot(domain="data/domain.pddl", problem="data/problem.pddl", heuristic_key="zero")
    assert(True)


