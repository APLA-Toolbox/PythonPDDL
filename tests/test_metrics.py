# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.metrics import Metrics


def test_metrics():
    m = Metrics()
    assert m.n_opened == 1 and m.n_generated and m.get_average_heuristic_runtime() == 0
