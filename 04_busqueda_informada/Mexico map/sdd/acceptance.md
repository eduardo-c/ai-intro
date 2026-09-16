# SDD — Acceptance / Validación independiente (Ejercicio 2)

**Ejercicio:** A* para encontrar rutas en el mapa de México
(`inteligencia-artificial/Búsqueda informada/Ejercicios/ejercicio-02.md`).
**Ámbito de validación:** requerimientos R1–R15 y criterios de aceptación AC1–AC8
de `sdd/requirements.md`, verificado **de forma independiente** por el agente de
aceptación (este documento): TODAS las corridas y comprobaciones de código fueron
RE-EJECUTADAS en esta sesión (no se confió en `tasks.md`).

**Entorno de validación real:**
- `python3` → Python 3.13.9
- `node` → v24.11.0
- Directorio de trabajo: `Mexico map/` (ruta con espacio, entrecomillada)

---

## 1. Trazabilidad requerimientos R1–R15

| # | Requerimiento | Resultado | Evidencia (re-ejecutada aquí) |
|---|---|---|---|
| R1 | Estado = id entero del nodo; acción = ir a vecino; costo = `edges[].km` | ✓ SATISFECHO | `mexico_problem.py:14` ("State = int city id"); `result().action` devuelve el id vecino; `step_cost → graph.cost()`. CLI `--from-city 6 --to 25` corre (id 6=Tijuana, 25=Cancún): éxito. |
| R2 | A* clásico `f=g+h` reutilizando `a_star_search` de `project/search/astar.py` | ✓ SATISFECHO | `find_route.py:27-29` importa `from search.astar import a_star_search` vía `sys.path` a `../project` (importado, NO copiado). `astar.py:24,54-55` usa `heapq` con `(path_cost + h(state), counter, node)`. |
| R3 | `h(n)` = haversine en línea recta a destino, al vuelo, `EARTH_KM=6371.0` | ✓ SATISFECHO | `mexico_problem.py:46-48` `make_heuristic` calcula haversine con lat/lon del goal, sin tabla. Salida CLI: `Heuristic: haversine straight-line distance to Cancún (km)`. Fórmula idéntica en `mexico_graph.py:25-31` y `generate_mexico_graph.py:65-70`. |
| R4 | Grafo conectado (4-NN ∪ MST); camino entre cualquier par | ✓ SATISFECHO | `MexicoGraph._check_connected()` (`mexico_graph.py:73-84`); verificado en vivo `connected=True`; 1000 nodos / 2565 aristas / `_edge_km` con 2565 claves / `cost(6,280)=7.28`. |
| R5 | Nombres repetidos (~39): desambiguar determinista + aviso; nunca silencioso | ✓ SATISFECHO | `resolve()` (`mexico_graph.py:137-208`): 39 nombres duplicados confirmados en vivo. `--from-city Puebla` → `WARNING: ambiguous name 'Puebla'…` con candidatos e id elegido. |
| R6 | Salida CLI: Status/Path/Depth/Cost/Expanded/Generated + heurística; truncado path largo | ✓ SATISFECHO | Salidas completas de P1/P2/P3/P4 (ver §4). Path de 125 ciudades truncado `primeras 7 + … + últimas 7` + total (variación del split 3+3 — ver desviación D1). |
| R7 | Invocación `python find_route.py --from-city O --to D`; nombre exacto / "Nombre, Estado" / id | ✓ SATISFECHO | `Mexico City→Monterrey` (espacio, entrecomillado); `"Puebla, Puebla"→Monterrey`; `6→25`; fuzzy `Cancun` con WARNING. ABC: nombre exacto del JSON. |
| R8 | Bug `node_count_safe` corregido → `graph.has_city(idx)` | ✓ SATISFECHO | `mexico_problem.py:18-21` usa `graph.has_city`. `grep -rn node_count_safe` en el repo: **0 referencias**. Ninguna corrida lanza `AttributeError`. |
| R9 | HTML: dos campos entrada + botón "Find Route" | ✓ SATISFECHO | `mexico_map.html:139-148`: `<select id="routeFrom">`, `<select id="routeTo">`, `<button id="findRouteBtn">Find Route</button>`, `<div id="routeResult">`. |
| R10 | A* en el navegador sobre `G` incrustado (port, frontera real) | ✓ SATISFECHO | `mexico_map.html:465-500` `aStagSearchJS`: heap por `(f, counter)`, `best_g`, `explored`, goal-check al extraer, vecinos por id asc. `G` incrustado = JSON (verificado idéntico). |
| R11 | Pintar ruta: nodos+aristas resaltados, resto atenuado, origen/destino distinguibles | ✓ SATISFECHO | `redraw()` (`mexico_map.html:303-336`): aristas de ruta `#1f4d3a` op. 0.95, resto `#8a7d6b` op. 0.10; nodos ruta `#1f4d3a`, origen `#14532d`, destino `#c2410c` con anillo, resto op. 0.12. |
| R12 | Costo en km en el panel + depth + expanded | ✓ SATISFECHO | `runRoute()` (`mexico_map.html:555-560`): `Cost: XX.XX km`, `Hops: N`, `Nodes expanded: N`, `Nodes generated: N`. |
| R13 | Desambiguado en UI ("Nombre — Estado"), no al azar | ✓ SATISFECHO | `renderRouteSelects()` (`mexico_map.html:506-521`): opciones `n.name + " — " + n.state` (los duplicados quedan distinguibles por construcción, ej. dos "Puebla"). |
| R14 | Costo mapa == costo CLI para la misma pareja | ✓ SATISFECHO | Harness JS independiente (Node v24) vs CLI sobre el mismo JSON: cost/expanded/generated/`maxFrontier` idénticos en **5 parejas**; path P1 idéntico ciudad a ciudad (§4.3). |
| R15 | Nueva búsqueda reemplaza la ruta previa | ✓ SATISFECHO | Listeners `change` de `routeFrom`/`routeTo` (`mexico_map.html:568-575`) llaman `clearRoute()`; `paintRoute` (`:524-525`) limpia `routePath`/`routeEdges` antes de repintar. |

---

## 2. Criterios de aceptación AC1–AC8

| AC | Criterio | Veredicto | Evidencia |
|---|---|---|---|
| AC1 | A* real, frontera por `f=g+h` | ✓ SATISFECHO | `heapq` + `path_cost + h(state)` en `astar.py` (importado por `find_route.py`). Port JS hereda mismas semánticas. No BFS/UCS/h=0/"vecino más cercano". |
| AC2 | `h` = haversine, `EARTH_KM=6371.0`, admisible/consistente | ✓ SATISFECHO | Fórmula idéntica en los 3 lugares (Python ×2 + JS); aristas también son haversine ⇒ `h(n) ≤ costo real` (desigualdad del triángulo). |
| AC3 | `python find_route.py --from-city X --to Y` corre y muestra camino+km | ✓ SATISFECHO | P1: `Status success`, `Cost 4528.20 km`, `Depth 124 roads`, `Expanded 949`, `Generated 4886`, `Max frontier 89`; P2: `1041.87 / 27 / 428 / 2174 / 56`. Exit 0. |
| AC4 | HTML permite elegir origen/destino y pinta la ruta | ✓ SATISFECHO | Selects + botón + `paintRoute/redraw`: nodos/aristas resaltados (verde), resto atenuado, origen/destino con anillo distinguible. `node --check` del `<script>` completo: OK. |
| AC5 | Nombres ambiguos no se resuelven en silencio | ✓ SATISFECHO | CLI: WARNING con candidatos y elegido (`Puebla`); UI: `Name — State` en cada `<option>`. Nunca aleatorio. |
| AC6 | El grafo no cambió (mismo JSON, 2565 aristas, 4-NN/MST) | ✓ SATISFECHO | JSON: 1000 nodos/2565 aristas; sha256 `c6cab812…`; mtime **Sep 12 15:08** (HTML/generador tocados Sep 14). Ningún `.py` de ejecución escribe el JSON; `generate_mexico_graph.py` **no se ejecutó**. |
| AC7 | CLI y mapa dan el mismo costo km (≥2 parejas) | ✓ SATISFECHO | 5 parejas con costo/depth/expanded/generated idénticos entre JS (Node) y CLI; path P1 completo idéntico. |
| AC8 | Bug `node_count_safe` corregido, sin `AttributeError` | ✓ SATISFECHO | `mexico_problem.py` usa `has_city`; `node_count_safe` ausente en todo el repo; todas las corridas limpias (exit 0). |

---

## 3. Reporte breve (E5, solicitado por el enunciado)

**(a) Qué se usó como estado y cómo se resolvieron los duplicados.**
El estado es el **id entero** del nodo (`nodes[].id`), no el nombre: en el grafo
hay **39 nombres repetidos** (verificado: `ambiguous_names()` → 39), así que el
nombre no es identificador válido. `MexicoGraph.resolve()` (`mexico_graph.py`)
implementa el desambiguado determinista y **nunca silencioso**: acepta el id
numérico directo, `"Nombre, Estado"` (búsqueda por estado exacto) o el nombre;
cuando un nombre es ambiguo, imprime `WARNING:` con los candidatos (id, estado,
población) y elige el de **mayor población**. Por ejemplo
`--from-city Puebla` avisa entre `Puebla (#4, Puebla, pop 1,434,062)` y
`Puebla (#580, Baja California, pop 15,168)` y elige la id 4. En la UI no hay
ambigüedad posible: los selectores listan cada ciudad como `Nombre — Estado`.

**(b) Por qué haversine es admisible aquí.**
Las aristas del grafo, `edges[].km`, se construyeron con la **misma** función
haversine (4-NN ∪ MST sobre la esfera, `EARTH_KM = 6371.0`). La heurística
`h(n)` es la distancia de gran círculo en línea recta entre la ciudad `n` y el
destino. Por la desigualdad del triángulo sobre la esfera, esa recta nunca puede
ser mayor que ningún camino por aristas haversine reales, es decir
`h(n) ≤ costo_real(n, goal)` para todo `n`: `h` es **admisible** (y además
consistente). Por tanto A* devuelve la ruta óptima en km.

**(c) Ruta larga Tijuana → Cancún.**
Costo **4528.20 km**, **124 hops** (125 ciudades), y A* expandió **949 nodos**
(generados 4886, frontera máxima 89). La recta haversine Tijuana–Cancún es
~3232 km (el `h` inicial impreso por el CLI), así que la ruta por carretera es
~1.3× la distancia en línea recta, y al estar el grafo disperso (4 vecinos por
nodo) el A* exploró casi todo el mapa.

---

## 4. Evidencias completas (salidas reales re-ejecutadas el Sep 14 2026)

### 4.1 P1 — Tijuana → Cancún (larga, obligatoria)

```
$ python3 find_route.py --from-city Tijuana --to Cancún   # exit 0
Algorithm: A* search
Problem:   Tijuana → Cancún
Heuristic: haversine straight-line distance to Cancún (km)
Status:    success
Path:      Tijuana → Villa del Prado 2da Sección → Terrazas del Valle → Tecate → Progreso → San Luis Río Colorado → Puerto Peñasco → … → Oxkutzkab → Akil → Peto → Felipe Carrillo Puerto → Tulum → Playa del Carmen → Cancún  (125 cities; showing first/last 7)
Depth:     124 roads
Cost:      4528.20 km
… (tabla g-h-f)
Expanded:  949 nodes
Generated: 4886 nodes
Frontier:  max size 89
```

### 4.2 P2 — Mexico City → Monterrey

```
$ python3 find_route.py --from-city "Mexico City" --to Monterrey   # exit 0
Algorithm: A* search
Problem:   Mexico City → Monterrey
Heuristic: haversine straight-line distance to Monterrey (km)
Status:    success
Path:      Mexico City → Gustavo Adolfo Madero → Puerto Escondido (Tepeolulco…) → … → Cadereyta Jiménez → Jardines de la Silla (Jardines) → Monterrey  (28 cities; showing first/last 7)
Depth:     27 roads   Cost: 1041.87 km
Expanded:  428 nodes   Generated: 2174 nodes   Frontier: max size 56
```

### 4.3 Pareja adicional P3 — Guadalajara → Mérida

```
$ python3 find_route.py --from-city Guadalajara --to Mérida   # exit 0
Path:      Guadalajara → Tlaquepaque → … → Tekit → Tekoh → Mérida  (71 cities)
Depth:     70 roads   Cost: 1984.75 km
Expanded:  736 nodes   Generated: 3769 nodes   Frontier: max size 83
```

### 4.4 Pareja corta (arista mínima del grafo, verificado con python)

Arista mínima del JSON: `{source:190, target:771, km:3.01, kind:"knn"}` →
`Teziutlan → Chinautla`.

```
$ python3 find_route.py --from-city Teziutlan --to Chinautla   # exit 0
Path: Teziutlan → Chinautla   Depth: 1 roads   Cost: 3.01 km
Expanded: 1   Generated: 7   Frontier: max size 6
```

### 4.5 Integridad del Path (cada hop es una arista real del JSON, verificado con python)

```
Tijuana -> Cancún:        depth=124 cost=4528.20 hops_sum=4528.20 chain_edges_exist=True expanded=949
Mexico City -> Monterrey: depth=27  cost=1041.87 hops_sum=1041.87 chain_edges_exist=True expanded=428
Guadalajara -> Mérida:    depth=70  cost=1984.75 hops_sum=1984.75 chain_edges_exist=True expanded=736
Teziutlan -> Chinautla:   depth=1   cost=3.01   hops_sum=3.01   chain_edges_exist=True expanded=1
Puebla -> Monterrey:      depth=30  cost=1121.15 hops_sum=1121.15 chain_edges_exist=True expanded=452
```
`hops_sum` (suma de `edges[].km` de cada salto) == `Cost`, y todos los saltos
existen en el JSON ⇒ Depth==hops y costos finitos y coherentes.

### 4.6 Desambiguación (AC5) — Puebla

```
$ python3 find_route.py --from-city Puebla --to Monterrey   # exit 0, CON warning
WARNING: ambiguous name 'Puebla': candidates are [Puebla (#4, Puebla, pop 1,434,062); Puebla (#580, Baja California, pop 15,168)]. Picked the most populous: Puebla (#4, Puebla, pop 1,434,062). Use 'Name, State' (or the integer id) to disambiguate.
Problem:   Puebla (Puebla) → Monterrey
Depth: 30 roads   Cost: 1121.15 km   Expanded: 452   Generated: 2309

$ python3 find_route.py --from-city "Puebla, Puebla" --to Monterrey   # exit 0, SIN warning
Problem:   Puebla → Monterrey
Depth: 30 roads   Cost: 1121.15 km   (idem)

$ python3 find_route.py --from-city 6 --to 25   # id numérico aceptado
Problem:   Tijuana → Cancún   Cost: 4528.20 km   Depth: 124 roads
```

Nombres duplicados confirmados en vivo: `ambiguous_names()` → **39**.

### 4.7 Errores y fuzzy

```
$ python3 find_route.py --from-city NoExiste --to Tijuana
error: no city matching 'NoExiste' in 1000 nodes        # stderr, exit code 1

$ python3 find_route.py --from-city Cancun --to Tijuana
WARNING: no exact match for 'Cancun'; using Cancún (#25, Quintana Roo, pop 628,306)
Depth: 124 roads   Cost: 4528.20 km
```

### 4.8 AC6 — el grafo no cambió

```
mexico_cities_graph.json : 1000 nodos, 2565 aristas (cargado), sha256 c6cab812a40f…   mtime Sep 12 15:08
mexico_map.html          : mtime Sep 14 14:19
generate_mexico_graph.py : mtime Sep 14 14:21 (editado HTML_TEMPLATE, NO ejecutado)
grep escrituras *.py      : mexico_graph/mexico_problem/find_route NO escriben nada; las únicas
                            escrituras viven dentro de generate_mexico_graph.py (no invocada)
G incrustado en el HTML   : nodes/edges/meta IDÉNTICOS al JSON del disco (python: equal True)
HTML_TEMPLATE             : espejo de la UI, conserva "const G = __GRAPH_JSON__;" (1 placeholder)
```

### 4.9 AC4 / R14 — port JS vs CLI (harness JS independiente del agente de aceptación)

Extracción propia de las funciones puras del `<script>` de `mexico_map.html`
(`haversineKm`, `buildAdjacency`, `edgeKm`, heap, `aStagSearchJS`) a
`/tmp/accept_astar_block.js` + `/tmp/accept_harness.js`, cargadas en Node v24.11.0
con el JSON real:

```
$ node --check /tmp/accept_astar_block.js && node --check /tmp/accept_harness.js   # SYNTAX OK
$ node /tmp/accept_harness.js mexico_cities_graph.json

Tijuana -> Cancun:  cost=4528.20 depth=124 expanded=949  generated=4886 maxFrontier=89  status=success | head=Tijuana, Villa del Prado 2da Sección, Terrazas del Valle | tail=Tulum, Playa del Carmen, Cancún
Mexico City -> Monterrey: cost=1041.87 depth=27  expanded=428  generated=2174 maxFrontier=56  | head=Mexico City, Gustavo Adolfo Madero, … | tail=…, Jardines de la Silla (Jardines), Monterrey
Guadalajara -> Merida: cost=1984.75 depth=70  expanded=736  generated=3769 maxFrontier=83  | head=Guadalajara, Tlaquepaque, Tonalá | tail=…, Tekoh, Mérida
Teziutlan -> Chinautla: cost=3.01  depth=1   expanded=1    generated=7    maxFrontier=6   | path Idéntico
Puebla -> Monterrey:  cost=1121.15 depth=30  expanded=452  generated=2309 maxFrontier=52
```

**Path P1 (Tijuana→Cancún) JS vs CLI:** 125 ids, `diff`/comparación python → **idénticos
ciudad a ciudad** (Villa del Prado 2da Sección, Terrazas del Valle … Tulum, Playa del
Carmen, Cancún). Todos los contadores coinciden con la CLI. **Coincidencia CLI==mapa
completa.**

### 4.10 UI — fragmentos clave de `mexico_map.html`

- Controles (`:139-148`): `<h2>Find route</h2>`, "A* shortest path between two cities (km)",
  `<select id="routeFrom">`, `<select id="routeTo">`,
  `<button id="findRouteBtn" …>Find Route</button>`, `<div id="routeResult">`.
- Selectores (`:506-521`): opciones `o.textContent = n.name + " — " + n.state`.
- A* en JS (`:465-500`): `const frontier = [[startH, 0, startChain]];` … `heapPop` →
  `if (s === toId) return {status:"success", …}` → expansión con `gc = g + edgeKm.get(s+"|"+nb)`
  y `f = gc + haversineKm(…)`. Comentario: *"Same semantics as astar.py: heap by (f, counter),
  explored set, best_g gate, goal checked on POP, neighbors expanded in ascending id order"*.
- Pintado (`:303-336` `redraw()`): aristas de ruta `#1f4d3a`/op 0.95/ancho 2.2, resto
  `#8a7d6b`/op 0.10; nodos ruta `#1f4d3a`, origen `#14532d` + anillo 2, destino `#c2410c`
  + anillo 2, resto op 0.12 (ruta activa). `paintRoute` (`:523-535`) y `clearRoute`
  (`:537-544`) → reemplazo garantizado (R15).

### 4.11 Bombitas de código (AC1/AC2/AC8)

- `find_route.py:27-29`: `from search.astar import a_star_search` (import proyectado).
- `astar.py:24`: `heapq.heappush(frontier, (node.path_cost + h(node.state), counter, node))`.
- `mexico_problem.py:46-50`: `h(state) = haversine(n.lat, n.lon, goal.lat, goal.lon)`; label.
- `mexico_graph.py:64-70`: `_edge_km` con `min/max(e["source"],e["target"])` (2565 claves, verificado).
- `mexico_problem.py:18-21`: `graph.has_city(start/goal)` (sin `node_count_safe`).

---

## 5. Desviaciones observadas (con severidad)

| # | Desviación | Severidad | Impacto en veredicto |
|---|---|---|---|
| D1 | Truncado de path/tabla: R6 sugiere `primeras 3 + … + últimas 3`; la implementación usa `--max-print 14` (default) → `primeras/últimas 7` + total. La esencia del requisito (truncar salida larga mostrando extremos y total) se cumple; R6 no se viola conceptualmente. | BAJA | No impide aprobación |
| D2 | `find_route.py` imprime además una tabla `g-h-f` por ciudad (extra sobre el mínimo exigido) | BAJA (cosmética) | No impide aprobación |
| D3 | README entregado como `README2.md` (el plan ordenaba no tocar `README.md` existente); el enunciado pide "un README corto en Mexico map/" — existe, se llama distinto | BAJA (formal) | No impide aprobación |
| D4 | La verificación visual en navegador (captura de pantalla) es EVIDENCIA QUE NO SE PUEDE PRODUCIR EN ESTA SESIÓN DE TERMINAL; se sustituye por: inspección estática de la UI+`node --check`+coincidencia JS-vs-CLI numérica y de path completa | INFORMATIVA | La UI se valida por código; se documenta la no-captura visual |

Ninguna desviación afecta requerimientos funcionales, costos ni topología.

---

## 6. Veredicto global

# ✅ APROBADO

Todos los requerimientos R1–R15 y todos los criterios AC1–AC8 se verifican de forma
independiente: A* real reutilizado (`a_star_search` importado), h = haversine al
destino admisible/consistente, CLI robusto con desambiguado nunca silencioso, port
JS con costos/expansión/path idénticos al CLI, UI con resaltado de ruta y reemplazo,
bug `node_count_safe` corregido y grafo intacto (mismas 2,565 aristas, generador no
ejecutado). No se detectó ninguna discrepancia de costos ni de topología.