#!/usr/bin/env python3
"""Route-finding problem + heuristic for the Mexico graph, shaped so it can be
given straight to ``search/astar.a_star_search`` from the Romania project
(which only needs ``start``, ``actions``, ``result``, ``step_cost``,
``is_goal``)."""

from __future__ import annotations

from collections.abc import Callable

from mexico_graph import MexicoGraph, haversine


class MexicoRouteProblem:
    """State = int city id. Action = move to a neighbor id. Step cost = km."""

    def __init__(self, graph: MexicoGraph, start: int, goal: int) -> None:
        if not graph.has_city(start):
            raise ValueError(f"unknown start city id: {start}")
        if not graph.has_city(goal):
            raise ValueError(f"unknown goal city id: {goal}")
        self.graph = graph
        self.start = start
        self.goal = goal

    def actions(self, state: int) -> list[int]:
        return self.graph.actions(state)

    def result(self, state: int, action: int) -> int:
        return action

    def step_cost(self, state: int, action: int) -> float:
        return self.graph.cost(state, action)

    def is_goal(self, state: int) -> bool:
        return state == self.goal


def make_heuristic(
    graph: MexicoGraph, goal: int
) -> tuple[Callable[[int], float], str]:
    """h(n) = haversine(n, goal). Admissible and consistent: both edge costs and
    h measure great-circle km, so h never overestimates the road distance."""
    goal_node = graph.node(goal)

    def h(state: int) -> float:
        n = graph.node(state)
        return haversine(n["lat"], n["lon"], goal_node["lat"], goal_node["lon"])

    label = f"haversine straight-line distance to {goal_node['name']} (km)"
    return h, label