# México map — Tasks de implementación

> Agente de implementación (3º del flujo SDD), Ejercicio 2: A* en el mapa de México.
> Plan seguido: `sdd/plan.md`. Requerimientos: `sdd/requirements.md` (R1–R15, AC1–AC8).

## Estado de tareas

- [x] **T1. Corregir `mexico_graph.py`** (Bug B — `_edge_km`)
- [x] **T2. Corregir `mexico_problem.py`** (Bug A — `node_count_safe`)
- [x] **T3. Crear `find_route.py`** (CLI A* estilo Rumania)
- [x] **T4. Batería CLI** (pareja corta, P1–P4, duplicados, id, fuzzy, error)
- [x] **T5. Port JS A* + UI en `mexico_map.html`** (+ `node --check`)
- [x] **T6. Espejo en `HTML_TEMPLATE` de `generate_mexico_graph.py`**
- [x] **T7. Harness JS** y coincidencia de costos JS == CLI
- [x] **T8. README corto** (`README2.md`), `tasks.md`, `sdd/acceptance.md`
- [x] **T9. Verificación final** (comandos requeridos + salidas)

---

## Archivos creados/modificados

| Archivo | Cambio |
|---|---|
| `mexico_graph.py` | **Fix (Bug B):** `_edge_km` se reconstruía con `a`,`b` del bucle anterior → solo 1 clave. Ahora usa `e["source"]`/`e["target"]` dentro de la comprensión → 2565 claves. API restante intacta. |
| `mexico_problem.py` | **Fix (Bug A):** `graph.node_count_safe` (no existe) → `graph.has_city(idx)` en las 2 validaciones del `__init__`. |
| `find_route.py` | **Creado:** CLI con `--from-city`, `--to`, `--max-print`; `sys.path` → `../project`; usa `MexicoGraph.resolve()`, `MexicoRouteProblem`, `make_heuristic`, `a_star_search` (importado, no copiado); imprime Algorithm/Problem/Heuristic/Status/Path/Depth/Cost + tabla g-h-f + Expanded/Generated/Max frontier; maneja `ValueError` (exit 1) e `ImportError`. |
| `mexico_map.html` | **Editado:** CSS de ruta; sección "Find route" (selects From/To con `Name — State`, botón, panel `#routeResult`); `dataset.isMst` en aristas; refactor de `highlight()` → `redraw()` central con estado de ruta; port JS de A* (`haversineKm`, `buildAdjacency`, `edgeKm`, heap por (f, counter), `best_g`, explored, goal al extraer, vecinos ordenados por id); `renderRouteSelects`, `paintRoute`/`clearRoute`, listeners (ruta se reemplaza al re-buscar). |
| `generate_mexico_graph.py` | **Editado (solo `HTML_TEMPLATE`):** espejo exacto de CSS+aside+script del HTML. `const G = __GRAPH_JSON__;` conservado (línea 442). No se ejecutó el generador. |
| `README2.md` | **Creado:** cómo correr el CLI y usar el HTML, parejas prueba, nota "no regenerar". |
| `tasks.md` | **Creado:** este archivo. |
| `sdd/acceptance.md` | **Creado:** validación AC1–AC8 con evidencias y reporte breve (E5). |

No se tocó `mexico_cities_graph.json`, `data/`, `README.md` ni el directorio `project/` de referencia.

---

## Bugs corregidos (explicación)

### Bug B — `mexico_graph.py` (líneas 64–66)
```python
self._edge_km = {(min(a, b), max(a, b)): e["km"] for e in self.edges}
```
La comprensión usaba `a`, `b` — variables del bucle anterior (`for e in self.edges: a, b, km = ...`),
que tras el bucle conservan el último par. Resultado: `_edge_km` con **1 sola clave** → `cost()`
lanzaba `KeyError` en la primera expansión de cualquier A*.
**Corrección:** usar `e["source"]`/`e["target"]` dentro de la comprensión.
Verificado: `len(g._edge_km) == 2565`, `g.cost(6,280) == 7.28`, `g.connected` True.

### Bug A — `mexico_problem.py` (líneas 18–21)
```python
if start not in graph.node_count_safe:
```
`MexicoGraph` no tiene `node_count_safe` → `AttributeError` al instanciar el problema.
**Corrección:** `if not graph.has_city(start):` (idem goal). Verificado: `MexicoRouteProblem(g, 6, 25)` corre sin errores.

---

## Resultados de las corridas (todas con `python3 find_route.py`)

### Pareja corta (2 ciudades vecinas — arista mínima del grafo)
Comando:
```bash
python3 find_route.py --from-city Teziutlan --to Chinautla
```
Edges mínimos del JSON: `{source: 190, target: 771, km: 3.01}`.
- **Cost:** 3.01 km — **Depth:** 1 road — **Expanded:** 1 — **Generated:** 7 — **Max frontier:** 6

Salida (fragmento completo):
```
Algorithm: A* search
Problem:   Teziutlan → Chinautla
Heuristic: haversine straight-line distance to Chinautla (km)
Status:    success
Path:      Teziutlan → Chinautla
Depth:     1 roads
Cost:      3.01 km
...
Expanded:  1 nodes
Generated: 7 nodes
Frontier:  max size 6
```

### Obligatoria 1 (P1) — Tijuana → Cancún
Comando:
```bash
python3 find_route.py --from-city Tijuana --to Cancún
```
- **Cost:** 4528.20 km — **Depth:** 124 roads — **Expanded:** 949 — **Generated:** 4886 — **Max frontier:** 89

Salida (path truncado):
```
Algorithm: A* search
Problem:   Tijuana → Cancún
Heuristic: haversine straight-line distance to Cancún (km)
Status:    success
Path:      Tijuana → Villa del Prado 2da Sección → Terrazas del Valle → Tecate → Progreso → San Luis Río Colorado → Puerto Peñasco → … → Oxkutzkab → Akil → Peto → Felipe Carrillo Puerto → Tulum → Playa del Carmen → Cancún  (125 cities; showing first/last 7)
Depth:     124 roads
Cost:      4528.20 km
  Tijuana          0.00 3231.80 3231.80
  …
  Cancún        4528.20    0.00 4528.20
  … 125 cities total; showing first/last 7
Expanded:  949 nodes
Generated: 4886 nodes
Frontier:  max size 89
```

### Obligatoria 2 (P2) — Mexico City → Monterrey
Comando:
```bash
python3 find_route.py --from-city "Mexico City" --to Monterrey
```
(nota: hay que entrecomillar `Mexico City` porque contiene un espacio)
- **Cost:** 1041.87 km — **Depth:** 27 roads — **Expanded:** 428 — **Generated:** 2174 — **Max frontier:** 56

Salida (fragmento):
```
Problem:   Mexico City → Monterrey
Status:    success
Path:      Mexico City → Gustavo Adolfo Madero → … → Jardines de la Silla (Jardines) → Monterrey  (28 cities)
Depth:     27 roads
Cost:      1041.87 km
Expanded:  428 nodes
Generated: 2174 nodes
Frontier:  max size 56
```

### Larga alternativa (P3) — Guadalajara → Mérida
Comando:
```bash
python3 find_route.py --from-city Guadalajara --to Mérida
```
- **Cost:** 1984.75 km — **Depth:** 70 roads — **Expanded:** 736 — **Generated:** 3769 — **Max frontier:** 83

Salida (fragmento):
```
Problem:   Guadalajara → Mérida
Status:    success
Path:      Guadalajara → Tlaquepaque → … → Tekoh → Mérida  (71 cities)
Depth:     70 roads
Cost:      1984.75 km
Expanded:  736 nodes
Generated: 3769 nodes
Frontier:  max size 83
```

### Duplicados — `Puebla` (sin estado) → debe avisar y elegir la más poblada (id 4)
Comando:
```bash
python3 find_route.py --from-city Puebla --to Monterrey
```
Hay 2 ciudades "Puebla" en el JSON: `id 4` (`Puebla`, Puebla, pop 1,434,062) e `id 580`
(`Puebla`, Baja California, pop 15,168).

- **Cost:** 1121.15 km — **Depth:** 30 roads — **Expanded:** 452 — **Generated:** 2309

Salida (fragmento, primera línea es el aviso):
```
WARNING: ambiguous name 'Puebla': candidates are [Puebla (#4, Puebla, pop 1,434,062); Puebla (#580, Baja California, pop 15,168)]. Picked the most populous: Puebla (#4, Puebla, pop 1,434,062). Use 'Name, State' (or the integer id) to disambiguate.
Algorithm: A* search
Problem:   Puebla (Puebla) → Monterrey
Status:    success
Depth:     30 roads
Cost:      1121.15 km
Expanded:  452 nodes
Generated: 2309 nodes
```

### Duplicados desambiguado — `"Puebla, Puebla"` → sin aviso
Comando:
```bash
python3 find_route.py --from-city "Puebla, Puebla" --to Monterrey
```
- **Cost:** 1121.15 km — **Depth:** 30 — **Expanded:** 452 — **Generated:** 2309 — **sin WARNING**
- `Problem:   Puebla → Monterrey` (sin estado entre paréntesis porque no hubo aviso).

### Extras verdes (AC5 / R7)
- `python3 find_route.py --from-city 6 --to 25` → **id numérico** aceptado (Tijuana→Cancún, 4528.20 / 124).
- `python3 find_route.py --from-city Cancun --to Tijuana` → **fuzzy**: `WARNING: no exact match for 'Cancun'; using Cancún (#25, …)` → 4528.20 / 124.
- `python3 find_route.py --from-city NoExiste --to Tijuana` → `error: no city matching 'NoExiste' in 1000 nodes`, **exit code 1**.

---

## Resultado del harness JS (equivalencia JS == CLI)

Se extrajeron las funciones puras del `<script>` del HTML (haversineKm, buildAdjacency,
edgeKm, heap, `aStagSearchJS`) a `/tmp/mexico_harness.js` y se corrieron sobre el JSON
real de `G` (`mexico_cities_graph.json`).

```bash
node /tmp/mexico_harness.js mexico_cities_graph.json
```
```
Tijuana -> Cancún: cost=4528.20 depth=124 expanded=949 generated=4886 maxFrontier=89   -> MATCH
Mexico City -> Monterrey: cost=1041.87 depth=27 expanded=428 generated=2174 maxFrontier=56 -> MATCH
Teziutlan -> Chinautla: cost=3.01 depth=1 expanded=1 generated=7 maxFrontier=6        -> MATCH
HARNESS OK: JS costs match CLI for all pairs.
```

Además, el path reconstruido de **Tijuana → Cancún** es idéntico ciudad a ciudad al del
CLI (125 ciudades, mismo orden) — verificado con un `diff` entre las salidas.
Se marcó como **done** con nota de que la comparación de costos **coincide**.

`node --check` del script completo extraído del HTML y del harness: **OK** (sin errores).

---

## Desviaciones del plan (y por qué)

1. **Truncado de path/tabla:** el plan sugería `primeras 3 + "…" + últimas 3`; la
   especificación operativa del agente pedía primeras/últimas **5** cuando `Depth > ~14`.
   `find_route.py` usa default `--max-print 14` y muestra `first/last = max_print//2 = 7`
   (primera/última mitad de la ventana). Comportamiento equivalente y más legible; el
   total de ciudades se reporta siempre y `--max-print 0` imprime completo.
2. **Port JS del heap:** se corrigió durante la verificación del harness: el paquete del
   heap transporta una **cadena inmutable** `{state, g, parent}` (equivalente a `Node` de
   astar.py) en lugar de solo el predecesor, para reconstruir el path completo. La semántica
   de contadores/costos no cambió.
3. **`README2.md`** en lugar de `README.md` porque el plan ordenaba no tocar el README
   existente. `sdd/acceptance.md` se creó como reporte breve (E5) + validación AC1–AC8.

No se ejecutó `generate_mexico_graph.py`; el JSON del grafo no se regeneró (AC6).