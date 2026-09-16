#!/usr/bin/env python3
"""Command-line A* route finder for the Mexico 1,000-city graph.

Reuses ``a_star_search`` from the Romania/search project (imported, not
copied). Usage:

    python find_route.py --from-city Tijuana --to Cancún

Both endpoints accept an exact city name, a "Name, State" pair, or an
integer node id. Ambiguous names produce a WARNING (never a silent pick).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent / "project"
if PROJECT.is_dir():
    sys.path.insert(0, str(PROJECT))
else:
    sys.exit(f"error: expected A* project at {PROJECT}")

try:
    from search.astar import a_star_search  # noqa: E402
    from search.result import FAILURE, SUCCESS  # noqa: E402
except ImportError as exc:  # pragma: no cover - defensive
    sys.exit(
        f"error: could not import search.astar from {PROJECT} "
        f"({exc}). Needed to reuse A* from the Romania project."
    )

from mexico_graph import MexicoGraph  # noqa: E402
from mexico_problem import MexicoRouteProblem, make_heuristic  # noqa: E402

ALGORITHM = "A* search"
DEFAULT_FROM = "Tijuana"
DEFAULT_TO = "Cancún"
MAX_PRINT = 14  # paths longer than this are shown as first/last 5 cities


def fmt_names(graph: MexicoGraph, ids: list[int], max_print: int = MAX_PRINT) -> str:
    """Join city names; truncate long paths to first/last half with a total count."""
    limit = max_print or float("inf")
    if len(ids) <= limit:
        return " → ".join(graph.name(i) for i in ids)
    half = max_print // 2
    head = " → ".join(graph.name(i) for i in ids[:half])
    tail = " → ".join(graph.name(i) for i in ids[-half:])
    return f"{head} → … → {tail}  ({len(ids)} cities; showing first/last {half})"


def fmt_problem_endpoint(graph: MexicoGraph, idx: int, warning: str | None) -> str:
    """'Name' when unambiguous, 'Name (State)' when a warning was raised."""
    return graph.label(idx) if warning else graph.name(idx)


def print_g_h_f_table(graph: MexicoGraph, node, h: Callable[[int], float], max_print: int = MAX_PRINT) -> None:
    chain: list = []
    cur = node
    while cur is not None:
        chain.append(cur)
        cur = cur.parent
    chain.reverse()
    print()
    print("  city                          g        h        f")
    limit = max_print or float("inf")
    if len(chain) <= limit:
        for n in chain:
            hv = h(n.state)
            print(f"  {graph.name(n.state):<28} {n.path_cost:7.2f} {hv:7.2f} {n.path_cost + hv:7.2f}")
    else:
        half = max_print // 2
        rows = [(graph.name(n.state), n.path_cost, h(n.state)) for n in chain]
        for name, g, hv in rows[:half] + rows[-half:]:
            print(f"  {name:<28} {g:7.2f} {hv:7.2f} {g + hv:7.2f}")
        print(f"  … {len(chain)} cities total; showing first/last {half}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Find the shortest route (km) between two Mexican cities with {ALGORITHM}."
    )
    parser.add_argument("--from-city", dest="start", default=DEFAULT_FROM,
                        help=f"Start city (name, 'Name, State', or id). Default: {DEFAULT_FROM!r}")
    parser.add_argument("--to", dest="goal", default=DEFAULT_TO,
                        help=f"Goal city (name, 'Name, State', or id). Default: {DEFAULT_TO!r}")
    parser.add_argument("--max-print", type=int, default=MAX_PRINT,
                        help="Truncate paths/tables longer than N cities. Default: 14. Use 0 for full.")
    args = parser.parse_args()

    graph = MexicoGraph()
    if not graph.connected:
        print("WARNING: graph not connected — routes may be impossible.", file=sys.stderr)

    try:
        start_id, start_warn = graph.resolve(args.start)
        goal_id, goal_warn = graph.resolve(args.goal)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if start_warn:
        print(f"WARNING: {start_warn}")
    if goal_warn:
        print(f"WARNING: {goal_warn}")

    problem = MexicoRouteProblem(graph, start_id, goal_id)
    h, label = make_heuristic(graph, goal_id)
    result = a_star_search(problem, h)

    print(f"Algorithm: {ALGORITHM}")
    print(f"Problem:   {fmt_problem_endpoint(graph, start_id, start_warn)} → "
          f"{fmt_problem_endpoint(graph, goal_id, goal_warn)}")
    print(f"Heuristic: {label}")
    print(f"Status:    {result.status}")
    if result.status == SUCCESS and result.node is not None:
        path = result.path
        print(f"Path:      {fmt_names(graph, path, args.max_print)}")
        print(f"Depth:     {result.depth} roads")
        print(f"Cost:      {result.cost:.2f} km")
        print_g_h_f_table(graph, result.node, h, args.max_print)
    elif result.status == FAILURE:
        print("No route found between the requested cities.")
    print()
    print(f"Expanded:  {result.nodes_expanded} nodes")
    print(f"Generated: {result.nodes_generated} nodes")
    print(f"Frontier:  max size {result.max_frontier}")

    sys.exit(0)


if __name__ == "__main__":
    main()