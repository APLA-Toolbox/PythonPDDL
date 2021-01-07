# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.data_analyst import DataAnalyst


def test_data_analyst_constructor():
    _ = DataAnalyst()
    assert True


def test_heuristics_comparer():
    da = DataAnalyst()
    da.comparative_astar_heuristic_plot()


def test_heuristics_comparer_single():
    da = DataAnalyst()
    da.comparative_astar_heuristic_plot(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
    )


def test_data_analyst_plot_dfs_one_pddl():
    da = DataAnalyst()
    da.plot_dfs(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
    )
    assert True


def test_data_analyst_plot_bfs_one_pddl():
    da = DataAnalyst()
    da.plot_bfs(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
    )
    assert True


def test_data_analyst_plot_dijkstra_one_pddl():
    da = DataAnalyst()
    da.plot_dijkstra(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
    )
    assert True


def test_data_analyst_plot_astar_h_goal_count_one_pddl():
    da = DataAnalyst()
    da.plot_astar(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
    )
    assert True


def test_data_analyst_plot_dfs():
    da = DataAnalyst()
    da.plot_dfs()
    assert True


def test_data_analyst_plot_bfs():
    da = DataAnalyst()
    da.plot_bfs()
    assert True


def test_data_analyst_plot_dijkstra():
    da = DataAnalyst()
    da.plot_dijkstra()
    assert True


def test_data_analyst_plot_astar_h_goal_count():
    da = DataAnalyst()
    da.plot_astar()
    assert True


def test_data_analyst_plot_dfs_restricted():
    da = DataAnalyst()
    da.plot_dfs(max_pddl_instances=2)
    assert True


def test_data_analyst_plot_bfs_restricted():
    da = DataAnalyst()
    da.plot_bfs(max_pddl_instances=2)
    assert True


def test_data_analyst_plot_dijkstra_restricted():
    da = DataAnalyst()
    da.plot_dijkstra(max_pddl_instances=2)
    assert True


def test_data_analyst_plot_astar_h_goal_count_restricted():
    da = DataAnalyst()
    da.plot_astar(max_pddl_instances=2)
    assert True


def test_data_analyst_plot_astar_h_zero():
    da = DataAnalyst()
    da.plot_astar(heuristic_key="zero")
    assert True


def test_comparative_no_restrictions():
    da = DataAnalyst()
    da.comparative_data_plot()
    assert True


def test_comparative_no_astar():
    da = DataAnalyst()
    da.comparative_data_plot(astar=False)
    assert True


def test_comparative_no_bfs():
    da = DataAnalyst()
    da.comparative_data_plot(bfs=False)
    assert True


def test_comparative_no_dijkstra():
    da = DataAnalyst()
    da.comparative_data_plot(dijkstra=False)
    assert True


def test_comparative_no_dfs():
    da = DataAnalyst()
    da.comparative_data_plot(dfs=False)
    assert True


def test_comparative_one_pddl():
    da = DataAnalyst()
    da.comparative_data_plot(
        dfs=False,
        bfs=False,
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
    )
    assert True


def test_comparative_use_data_json():
    da = DataAnalyst()
    da.comparative_data_plot(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
        collect_new_data=False,
    )
    assert True


def test_comparative_zero_h():
    da = DataAnalyst()
    da.comparative_data_plot(
        domain="pddl-examples/dinner/domain.pddl",
        problem="pddl-examples/dinner/problem.pddl",
        heuristic_key="zero",
    )
    assert True

def test_success_rate():
    da = DataAnalyst()
    da.compute_planners_efficiency()
    assert True
