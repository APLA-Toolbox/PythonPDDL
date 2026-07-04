"""Search-node helpers and plan reconstruction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchNode:
    state: frozenset
    parent: Optional["SearchNode"]
    action: object  # Operator that produced this node (None for the root)
    g: int  # accumulated path cost
    depth: int  # number of actions from the root


def make_root(state: frozenset) -> SearchNode:
    return SearchNode(state, None, None, 0, 0)


def make_child(parent: SearchNode, action, state: frozenset, cost: int) -> SearchNode:
    return SearchNode(state, parent, action, parent.g + cost, parent.depth + 1)


def extract_plan(node: SearchNode) -> list:
    """Walk parent pointers to recover the ordered list of operators."""
    plan = []
    while node is not None and node.action is not None:
        plan.append(node.action)
        node = node.parent
    plan.reverse()
    return plan
