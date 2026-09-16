#!/usr/bin/env python3
"""Mexico city graph: load the JSON, build an undirected (id-keyed) graph,
expose haversine, and resolve city names (unique or disambiguated).

Reused pieces:
- ``haversine`` / ``EARTH_KM`` mirror ``Mexico map/generate_mexico_graph.py``
  so the heuristic and the edge costs are computed with the SAME earth model.
- States are the integer node ``id`` from ``mexico_cities_graph.json`` (names
  are not unique: ~39 duplicated city names exist).
"""

from __future__ import annotations

import json
import math
import unicodedata
from collections import defaultdict
from pathlib import Path

EARTH_KM = 6371.0
ROOT = Path(__file__).resolve().parent
GRAPH_PATH = ROOT / "mexico_cities_graph.json"


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km (same function as generate_mexico_graph.py)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * EARTH_KM * math.asin(math.sqrt(min(1.0, a)))


def _norm(text: str) -> str:
    """Lower-case and strip accents so 'Cancún' matches 'Cancun' as a fallback."""
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch)
    ).casefold().strip()


class MexicoGraph:
    """Undirected weighted graph over the 1,000 Mexican cities, keyed by int id."""

    def __init__(self, path: Path = GRAPH_PATH) -> None:
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.path = path
        self.meta = raw["meta"]
        self.nodes: list[dict] = raw["nodes"]
        self.edges: list[dict] = raw["edges"]
        self._by_id = {n["id"]: n for n in self.nodes}
        self._by_name: dict[str, list[int]] = defaultdict(list)
        for n in self.nodes:
            self._by_name[n["name"]].append(n["id"])
        for ids in self._by_name.values():
            ids.sort(key=lambda i: (-self._by_id[i]["population"], i))

        self._adj: dict[int, list[tuple[int, float]]] = defaultdict(list)
        for e in self.edges:
            a, b, km = e["source"], e["target"], e["km"]
            self._adj[a].append((b, km))
            self._adj[b].append((a, km))
        for ids in self._adj.values():
            ids.sort(key=lambda pair: pair[0])
        self._edge_km: dict[tuple[int, int], float] = {
            (
                min(e["source"], e["target"]),
                max(e["source"], e["target"]),
            ): e["km"]
            for e in self.edges
        }
        self.connected = self._check_connected()

    def _check_connected(self) -> bool:
        if not self.nodes:
            return False
        seen = {0}
        stack = [0]
        while stack:
            u = stack.pop()
            for v, _km in self._adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return len(seen) == len(self.nodes)

    def node(self, idx: int) -> dict:
        return self._by_id[idx]

    def has_city(self, idx: int) -> bool:
        return idx in self._by_id

    def name(self, idx: int) -> str:
        return self._by_id[idx]["name"]

    def label(self, idx: int) -> str:
        n = self._by_id[idx]
        return f"{n['name']} ({n['state']})"

    def neighbors(self, state: int) -> list[tuple[int, float]]:
        """Sorted by neighbor id so runs are deterministic."""
        return self._adj[state]

    def actions(self, state: int) -> list[int]:
        return [v for v, _km in self._adj[state]]

    def cost(self, a: int, b: int) -> float:
        try:
            return self._edge_km[(min(a, b), max(a, b))]
        except KeyError:
            raise KeyError(f"no edge between {a} and {b}") from None

    def ambiguous_names(self) -> list[str]:
        return sorted(name for name, ids in self._by_name.items() if len(ids) > 1)

    # -- name resolution ---------------------------------------------------

    def by_name(self, name: str) -> list[int]:
        return list(self._by_name.get(name, []))

    def find_name_state(self, name: str, state: str) -> list[int]:
        """Case/accent-insensitive name + exact state."""
        nn = _norm(name)
        return [
            i
            for i in self._by_name.get(name, [])
            if self._by_id[i]["state"] == state
        ] or [
            i
            for i, _ in self._by_id.items()
            if _norm(self._by_id[i]["name"]) == nn and self._by_id[i]["state"] == state
        ]

    def descr(self, idx: int) -> str:
        n = self._by_id[idx]
        return f"{n['name']} (#{n['id']}, {n['state']}, pop {n['population']:,})"

    def resolve(self, text: str) -> tuple[int, str | None]:
        """Return (node id, warning|None).

        Resolution order:
          1. integer id        -> that city directly.
          2. "Name, State"     -> unambiguous (state-aware) pick.
          3. exact name        -> unique: use it; multiple: most populous + WARN.
          4. normalized name   -> accent/case-insensitive exact; WARN on fuzzy hit.
          5. ValueError with candidates (never silent random choice).
        """
        text = text.strip()
        warning: str | None = None

        if text.isdigit():
            idx = int(text)
            if idx in self._by_id:
                return idx, None
            raise ValueError(f"unknown city id: {idx}")

        if "," in text:
            name, state = (p.strip() for p in text.rsplit(",", 1))
            ids = self.find_name_state(name, state)
            if ids:
                if len(ids) == 1:
                    return ids[0], None
                chosen = max(ids, key=lambda i: self._by_id[i]["population"])
                cands = "; ".join(self.descr(i) for i in ids)
                warning = (
                    f"name {name!r} in state {state!r} is still ambiguous as "
                    f"[{cands}]; picked the most populous: {self.descr(chosen)}"
                )
                return chosen, warning
            warning = f"{name!r} ({state!r}): no exact state match; trying {name!r} alone"

        ids = self.by_name(text)
        if len(ids) == 1:
            return ids[0], warning
        if len(ids) > 1:
            chosen = max(ids, key=lambda i: self._by_id[i]["population"])
            cands = "; ".join(self.descr(i) for i in ids)
            warning = (
                f"ambiguous name {text!r}: candidates are [{cands}]. "
                f"Picked the most populous: {self.descr(chosen)}. "
                "Use 'Name, State' (or the integer id) to disambiguate."
            )
            return chosen, warning

        nn = _norm(text)
        fuzzy = [i for i in sorted(self._by_id) if _norm(self._by_id[i]["name"]) == nn]
        if len(fuzzy) == 1:
            warning = f"no exact match for {text!r}; using {self.descr(fuzzy[0])}"
            return fuzzy[0], warning
        if len(fuzzy) > 1:
            chosen = max(fuzzy, key=lambda i: self._by_id[i]["population"])
            cands = "; ".join(self.descr(i) for i in fuzzy)
            warning = (
                f"no exact match for {text!r}; candidates [{cands}]. "
                f"Picked the most populous: {self.descr(chosen)}"
            )
            return chosen, warning

        near = [
            i
            for i in sorted(self._by_id, key=lambda i: self._by_id[i]["name"])
            if nn in _norm(self._by_id[i]["name"])
        ]
        if near:
            top = "; ".join(self.descr(i) for i in near[:20])
            raise ValueError(
                f"no city matching {text!r}. Did you mean one of: {top}"
            )
        raise ValueError(f"no city matching {text!r} in {self.meta['nodes']} nodes")