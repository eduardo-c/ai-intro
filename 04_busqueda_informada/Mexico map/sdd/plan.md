# SDD — Plan de implementación (Ejercicio 2: A* en el mapa de México)

> Entregable del agente de planificación. Lo sigue un agente de implementación
> **sin** acceso a este contexto previo, así que todo lo que necesita está aquí.
> Fuentes de verdad: `sdd/requirements.md` (R1–R15, AC1–AC8) y el enunciado
> `ejercicio-02.md`.

---

## 1. Resumen del objetivo

Agregar a `Mexico map/` la capacidad de calcular la **ruta de menor costo en km**
entre dos ciudades con **A\*** (`f = g + h`), expuesta por **dos frentes**:

1. **CLI** `find_route.py` — reutiliza el A\* existente de
   `Búsqueda informada/project/search/astar.py` (importado, no copiado).
2. **Mapa `mexico_map.html`** — controles origen/destino, un **port JS** del
   mismo A\* con las **mismas semánticas** (mismos costos y expansiones), y
   pintado del camino resaltado con el resto atenuado.

Se modifica **solo** búsqueda/UI. **No** se regenera el grafo, **no** se cambia
la topología 4-NN ∪ MST, **no** se toca `mexico_cities_graph.json`.

**Hallazgos de la fase de planificación (críticos, verifícalos al implementar):**

- **Bug A — `mexico_problem.py`**: `graph.node_count_safe` no existe
  (requerimiento R8). Hay que usar `graph.has_city(idx)`.
- **Bug B — `mexico_graph.py` (NO documentado en requirements, descubierto
  corriendo A\*):** el dict `_edge_km` (líneas 64–66) se construye con una
  comprensión que reutiliza las variables `a`, `b` del bucle anterior
  (`for e in self.edges` no reasigna `a`/`b`), por lo que **solo guarda 1 clave**
  y `cost()` lanza `KeyError` en la primera expansión del A\*. Verificado:
  `len(g._edge_km) == 1` en vez de `2565`. **Sin corregirlo, R3/AC3 fallan**
  (cualquier corrida A\* explota). Esto es la "corrección menor" que permite E1.
- **Invariante útil verificado:** los ids de `G.nodes` son `0..999` contiguos y
  el array ya está ordenado por id ⇒ en JS el `id` del nodo coincide con el
  índice del array, pero conviene teclear por `id` explícitamente por claridad.

**Valores de referencia** (obtenidos con A\* importado + ambos bugs corregidos,
para orientar la verificación; NUNCA hardcodearlos — deben salir del algoritmo):

| Pareja | Cost km (2 dec.) | Hops | Expanded | Generated | Max frontier |
|---|---|---|---|---|---|
| P1 `Tijuana` → `Cancún` | `4528.20` | `124` | `949` | `4886` | `89` |
| P2 `Mexico City` → `Monterrey` | `1041.87` | `27` | `428` | `2174` | `56` |
| P3 `Guadalajara` → `Mérida` | `1984.75` | `70` | `736` | `3769` | `83` |
| P4 `Hermosillo` → `Oaxaca` | `2361.45` | `62` | `408` | `2077` | `106` |

(Id de referencia: `Tijuana=6`, `Cancún=25`, `Mexico City=0`, `Monterrey=10`,
`Guadalajara=3`, `Mérida=14`, `Hermosillo=18`, `Oaxaca=72`.)

---

## 2. Decisiones de diseño

### D1. Estado = id entero del nodo
El estado del problema es el campo `id` (int) de cada nodo del JSON, no el
nombre (hay 39 nombres duplicados). Es lo que ya hace `mexico_graph.py` y lo que
recomienda el enunciado. `Node` de Rumania está anotado `str` pero **no hace
ningún `isinstance`** en runtime: cargar ints funciona (verificado).

### D2. Import vs copia del A\*: **IMPORTAR** desde `../project`
Se **importa** `a_star_search` desde `search.astar` añadiendo `../project` a
`sys.path` en `find_route.py`. Razones:
- El enunciado dice "reutilizar (importar o copiar y adaptar)"; el proyecto de
  referencia ya usa este patrón exacto en `project/04_a_star_search.py`
  (`sys.path.insert(0, str(ROOT))` + `from search.astar import a_star_search`).
- Evita duplicar lógica y deriva entre la referencia y la entrega.
- No se modifica absolutamente nada de `../project`.

Patrón exacto en `find_route.py` (después de `ROOT`):
```python
PROJECT = ROOT.parent / "project"
sys.path.insert(0, str(PROJECT))
from search.astar import a_star_search      # noqa: E402
from search.result import SUCCESS, FAILURE  # noqa: E402  (opcional)
```
La importación arrastra `from romania.node import Node` y
`from search.result import SearchResult` — resolverán contra `../project` y no
colisionan con módulos locales (no existe `search`/`romania` locales).
`ROOT = Path(__file__).resolve().parent` (no depende del CWD).

### D3. Problema propio de México compatible con la interfaz de `a_star_search`
`a_star_search` solo usa (duck-typing): `problem.start`, `problem.actions(state)`,
`problem.result(state, action)`, `problem.step_cost(state, action)`,
`problem.is_goal(state)`. `MexicoRouteProblem` ya cumple la forma; se corrige
el **Bug A** (validación) y el **Bug B** (en `mexico_graph.py`):
- `__init__`: `if not graph.has_city(start): raise ValueError(...)` (idem
  `goal`) — sustituye `if start not in graph.node_count_safe`.
- `actions(state)` → `graph.actions(state)` = vecinos **ordenados por id**
  (determinismo idéntico en CLI y JS).
- `result(state, action)` → `action` (ir a ese vecino).
- `step_cost(state, action)` → `graph.cost(state, action)` (km float).
- `is_goal(state)` → `state == self.goal`.

### D4. Heurística = haversine al destino, al vuelo
`make_heuristic(graph, goal)` devuelve `(h, label)` al estilo de
`romania/heuristics.py`. `h(state) = haversine(lat_n, lon_n, lat_goal, lon_goal)`
con `EARTH_KM = 6371.0`, **sin tabla precomputada**.
Admisible/consistente porque las aristas también se miden con haversine
(desigualdad del triángulo): `h(n) ≤ costo_real(n, goal)`. La fórmula debe ser
idéntica a `mexico_graph.haversine` y a `generate_mexico_graph.haversine`
(los tres lugares usan la misma cuenta). Label: `"haversine straight-line distance to {name} (km)"`.

### D5. Desambiguación de nombres (nunca silenciosa)
Se usa `MexicoGraph.resolve(text)` **tal cual existe**, sin duplicarla:
1. Entero puro → id directo.
2. `"Nombre, Estado"` → desambigua por estado (`find_name_state`).
3. Nombre exacto → único directo; múltiples → **más poblada + WARN con
   candidatos** (`descr`).
4. Fallback case/accent-insensitive → fuzzy + WARN.
5. Sin match → `ValueError` con sugerencias.

El plan implica **espejar esta misma lógica en el JS**: como en la UI se usan
selectores poblados desde `G` (ver D7), el desambiguado queda garantizado por
construcción.

### D6. Port JS con las MISMAS semánticas que el Python
Para que CLI y mapa den **el mismo costo y las mismas expansiones** (R14/AC7),
el A\* JS replica exactamente `search/astar.py`:
- Heap mínimo ordenado por `(f, contador)` (tie-break por inserción, igual que
  el `counter` del heap de Python).
- `best_g` como diccionario/Mapl `state → g`; solo se inserta si
  `child.path_cost < best_g[s]` o es la primera vez.
- `explored` como `Set`; goal-check **al extraer** de la frontera.
- Vecinos en orden **ascendente de id** (igual que `graph.actions`).
- `generated`, `expanded`, `max_frontier` contados igual.

### D7. UI = selectores, no cajas de texto
Para satisfacer R13/AC5 ("ofrecer selector, no elegir al azar") sin reintroducir
desambiguación JS, los campos origen/destino son dos `<select>` poblados con
todas las ciudades como **`<option value="<id>">Name (State)</option>`**
etiquetadas con estado (los duplicados quedan distinguibles por construcción).

### D8. Edición del HTML a mano + espejo en `HTML_TEMPLATE`
`mexico_map.html` se edita a mano. `generate_mexico_graph.py` **no se ejecuta**.
Los mismos cambios (CSS + aside + script) se reflejan después en la variable
`HTML_TEMPLATE` de `generate_mexico_graph.py` (líneas ~282–619, entre
`HTML_TEMPLATE = r"""` y el cierre previo a `def build_html`), **conservando el
placeholder `const G = __GRAPH_JSON__;`** que hoy está en la línea ~409 del
generador. Así una regeneración futura no pierde la UI.

---

## 3. Inventario de archivos (acción + contenidos esperados)

| # | Archivo | Acción | Contenidos esperados |
|---|---|---|---|
| 1 | `mexico_graph.py` | **EDITAR** | Sin cambios estructurales. **Corregir Bug B**: reconstruir `_edge_km` con sus propios `source`/`target`, p. ej. `self._edge_km = {(min(e["source"], e["target"]), max(e["source"], e["target"])): e["km"] for e in self.edges}` → debe quedar **2565 claves**. Todo lo demás (haversine, `_norm`, `MexicoGraph`, `resolve`, `find_name_state`, `descr`, `has_city`, `actions`, `cost`, `neighbors`, `ambiguous_names`, `connected`) se conserva. |
| 2 | `mexico_problem.py` | **EDITAR** | Corregir **Bug A**: `graph.node_count_safe` → `graph.has_city(idx)` en el `__init__`. `MexicoRouteProblem` + `make_heuristic` sin otros cambios. |
| 3 | `find_route.py` | **CREAR** | CLI con argparse (`--from-city`, `--to`, `--max-print`), `sys.path` a `../project` (D2), uso de `MexicoGraph.resolve`, `MexicoRouteProblem`, `make_heuristic`, `a_star_search`, impresión estilo Rumania (sección 4). |
| 4 | `mexico_map.html` | **EDITAR** | CSS para el panel de ruta; `<aside>` con `#routeFrom`, `#routeTo`, `#findRouteBtn`, `#routeResult`; port JS del A\* (sección 5); pintado de ruta y limpieza al re-buscar (R15). |
| 5 | `generate_mexico_graph.py` | **EDITAR** | Solo `HTML_TEMPLATE`: espejo del HTML editado (D8), manteniendo `__GRAPH_JSON__`. No tocar lógica de grafo ni `main`. |
| 6 | `README2.md` | **CREAR** | README corto de entrega (E3): cómo correr el CLI (`python find_route.py --from-city X --to Y`), ejemplos P1/P2, cómo usar la ruta en el HTML, parejas sugeridas, nota de "no regenerar". |
| 7 | `tasks.md` | **CREAR** | Check-list de implementación con progreso (por archivo + verificación). Se llena durante la implementación. |
| 8 | `sdd/acceptance.md` | **CREAR** | Validación contra **AC1–AC8** punto por punto, con comandos/salidas/evidencias (E4: capturas + salidas CLI). Debe quedar completado al cerrar. |
| 9 | `sdd/requirements.md` | (ya existe) | **Sin cambios** — referencia R1–R15 / AC1–AC8. |
| — | `README.md` | No tocar | Se conserva tal cual. |
| — | `mexico_cities_graph.json`, `data/`, `emit_viz.py` | No tocar | Grafo y tooling; no se regeneran. |

---

## 4. Plan del CLI `find_route.py`

### 4.1 Interfaz de línea de comandos

```
python find_route.py --from-city ORIGEN --to DESTINO [--max-print N]
```
- `--from-city` (obligatorio en la práctica; default `"Mexico City"`), `--to`
  (default `"Monterrey"`). Acepta nombre exacto, `"Nombre, Estado"`, o **id
  numérico** (R7).
- `--max-print N` (default `10`): si la ruta tiene **más de N nodos**, imprime
  `primeras 3 + "…" + últimas 3` con el total completo. `--max-print 0` imprime
  completo. (R6 exige el truncado para rutas largas.)

### 4.2 Estructura del script (nombres exactos)

```python
ROOT  = Path(__file__).resolve().parent
PROJECT = ROOT.parent / "project"         # o ../project relativo a ROOT
sys.path.insert(0, str(PROJECT))
from search.astar import a_star_search    # noqa: E402

from mexico_graph import MexicoGraph      # módulos locales del dir del script
from mexico_problem import MexicoRouteProblem, make_heuristic

def fmt_path(graph, path_ids, max_print=10) -> str
def main() -> None
```

Pasos de `main`:
1. `parser = argparse.ArgumentParser(...)` con los 3 argumentos.
2. `graph = MexicoGraph()` (carga; `graph.connected` se valida solo — si fuera
   `False`, imprimir warning y continuar de todas formas).
3. `(start_id, warn_start) = graph.resolve(args.start)`; idem `(goal_id, warn_goal)
   = graph.resolve(args.to)`. Cada warning con prefijo `WARNING:` a stdout
   (R5/AC5: "avisar en la salida").
4. `problem = MexicoRouteProblem(graph, start_id, goal_id)`.
5. `h, label = make_heuristic(graph, goal_id)`.
6. `result = a_star_search(problem, h)`.
7. Imprimir bloque de salida (4.3). `sys.exit(0)`.

### 4.3 Salida requerida

```
WARNING: ambiguous name 'Puebla': candidates are [Puebla (#4, Puebla, pop 1,434,062); Puebla (#580, Baja California, pop 15,168)]. Picked the most populous: Puebla (#4, Puebla, pop 1,434,062). ...   (solo si hay aviso)
Algorithm: A* search
Problem:   <label_origen> → <label_destino>          # label = "Name (State)" vía graph.label(id)
Heuristic: haversine straight-line distance to Cancún (km)
Status:    success
Path:      Tijuana → Villa del Prado 2da Sección → Terrazas del Valle → … → Tulum → Playa del Carmen → Cancún
Depth:     124 roads
Cost:      4528.20 km
Expanded:  949 nodes
Generated: 4886 nodes
Max frontier: 89
```

Detalles de formato:
- `Status:` → `result.status` (`"success"` / `"failure"`). En case de
  `"failure"` imprimir solo Status + Expanded/Generated y terminar.
- `Path:` nombres (no estados). Truncar según `fmt_path`
  (`nodo > N → [:3] + "…" + [-3:]`) y añadir `(X cities; showing first/last 3)`.
- `Cost:` float con **2 decimales** (`f"{result.cost:.2f} km"`; R6/AC3).
- `Depth:` `result.depth` y "roads".
- `Expanded:` `result.nodes_expanded`; `Generated:` `result.nodes_generated`;
  `Max frontier:` `result.max_frontier` (paridad con el CLI de Rumania).

### 4.4 Comportamiento de errores
- `ValueError` de `resolve` (no existe / sugerencias) → `parser.error(str(e))` o
  `sys.exit(f"error: {e}")` con código ≠ 0 y mensaje legible.
- `ImportError` de `search.astar` → mensaje claro indicando la ruta esperada
  `../project` y salir con código ≠ 0 (mitigación de import frágil).
- Advertencias de desambiguación/fuzzy van **antes** del bloque principal y con
  prefijo distinto (`WARNING:`).

---

## 5. Plan del port JS en `mexico_map.html`

### 5.1 Estructura de datos (son las mismas del Python)

- `EARTH_KM = 6371.0`.
- `haversineKm(lat1, lon1, lat2, lon2)` — fórmula idéntica a `mexico_graph.haversine`
  usando `Math.radians` (implementar `deg2rad` o `Math.PI/180`).
- `buildAdjacency()` → `Map<number, number[]>`: por cada `edge` en `G.edges`
  añade `source→target` y `target→source`; luego **ordena cada lista
  ascendente** (identico a `graph.actions` / `graph.neighbors`).
- `edgeKm` → `Map<string, number>`: clave `"a|b"` en **ambos sentidos**
  (`edgeCost.set(a+"|"+b, km)` y viceversa) para lookup directo sin `min/max`.
- `aStagSearchJS(fromId, toId)` → `{status, path:[], cost, expanded, generated,
  maxFrontier}` replicando `search/astar.py` con números contra `G.nodes`.

### 5.2 Algoritmo A* JS (mismas semánticas, mismo orden)

```js
// heap mínimo de [f, counter, state, g, parent]; comparador: a[0]-b[0] || a[1]-b[1]
// heapPush/heapPop sobre array (implementar sift-up/sift-down). Paquete con:
//   node = [f, counter, state, g, parent]
//   frontier contiene el nodo inicial [h(start), counter=0, start, 0, null]
const best_g = new Map([[fromId, 0.0]]);
const explored = new Set();
generated = 1; expanded = 0; maxFrontier = 1; counter = 0;
while (frontier.length) {
  const [, , s, g, parent] = heapPop(frontier);
  if (explored.has(s)) continue;
  if (s === toId) return {status:"success", path:rebuild(parent chain), cost:g, ...};
  explored.add(s); expanded++;
  for (const nb of adjacency.get(s)) {              // nb ascendente por id
    generated++;
    if (explored.has(nb)) continue;
    const gc = g + edgeKm.get(s + "|" + nb);
    if (!best_g.has(nb) || gc < best_g.get(nb)) {
      best_g.set(nb, gc);
      counter++;
      heapPush(frontier, [gc + haversineKm(nodes[nb], nodes[toId]), counter, nb, gc, {state:s,g,parent}]);
      maxFrontier = Math.max(maxFrontier, frontier.length);
    }
  }
}
return {status:"failure", ...};
```

Reconstruir el path caminando hacia atrás por la cadena `parent`. El `h` usa
`haversineKm(nb.lat, nb.lon, goal.lat, goal.lon)`. Contadores idénticos al
Python (goal-check al extraer, `continue` si explorado, actualización condicional
de `best_g`, contador estricto en cada push).

### 5.3 Integración al HTML existente (nombres exactos)

**CSS nuevo** (en el `<style>` existente): estilos para `.route-row`,
`.route-btn`, `.route-result`, y `.route-node`/`.route-edge` (o manejar solo vía
atributos; ver 5.4).

**Aside** — insertar un bloque `<div>` después del bloque de "Find a city"
(input `#q`) y antes de `#detail`:
```html
<div>
  <h2>Find route</h2>
  <label for="routeFrom">From</label>
  <select id="routeFrom"></select>
  <label for="routeTo">To</label>
  <select id="routeTo"></select>
  <button id="findRouteBtn" type="button">Find Route</button>
  <div class="route-result" id="routeResult"></div>
</div>
```
(`routeFrom`/`routeTo` se llenan con `<option value="<id>">Name (State)</option>`
ordenadas por nombre; el estado va en la etiqueta, duplicados distinguibles —
D7/R13.)

**Script JS nuevo** (al final del `<script>` existente, después del bloque de
pan/zoom):
- `renderRouteSelects()` — puebla los dos `<select>`.
- `paintRoute(ids)` / `clearRoute()` — lógica de colores (5.4).
- Listener del botón: `aStagSearchJS(+routeFrom.value, +routeTo.value)`, llena
  `#routeResult` con `Cost: XX.XX km`, `Hops: N`, `Expanded: N`, `Generated: N`,
  y llama `paintRoundtrip(path)`. En `status === "failure"` mostrar mensaje.
- Al cambiar `routeFrom`/`routeTo` o pulsar de nuevo → `clearRoute()` primero y
  repintar (R15: la ruta se reemplaza, no se acumula).

### 5.4 Pintado de la ruta (R11/AC4) — capas existentes reutilizadas

No se crean capas nuevas: se reutilizan `edgeLayer`/`nodeLayer` ya existentes
(conservan `dataset.s`, `dataset.t`, `dataset.i`). El estado se guarda en
`const routePath = new Set()` (ids) y `const routeEdges = new Set()` (claves
`"min|max"`). Reglas de `redraw()` (llamada desde `paint`/`clear`/`highlight`):

- **Aristas:** si clave ∈ `routeEdges` → `stroke #1f4d3a`, `stroke-opacity 0.95`,
  `stroke-width 2.2`. Si no → `#8a7d6b`, opacidad 0.10 (atenuado), salvo hover
  del vecindario que la sube a 0.5.
- **Nodos:** si id ∈ `routePath` → `fill #1f4d3a` opacidad 0.95. Origen:
  `fill #14532d` + `stroke #14532d` ancho 2 (distinguible). Destino: `fill #c2410c`
  + anillo `stroke #c2410c` ancho 2. Resto → `#9a3412` opacidad 0.12, salvo
  nodo/vecinos del hover que suben a 0.95.
- `highlight(i)` (hover) debe **respetar el estado de ruta**: los elementos de
  ruta conservan su color; solo el vecindario hover eleva opacidad sobre el
  fondo atenuado. Implementar `redraw()` como función única y hacer que
  `highlight`, `paint`, `clear` terminen llamándola (evita duplicación).
- La caja `#q`/`filter`/pan-zoom no se tocan (operan sobre `style.display` y el
  transform de `world`; no se pisan con colores).

---

## 6. Secuencia de pasos numerada (implementación + verificación)

1. **Corregir `mexico_graph.py` (Bug B).**
   - Editar solo la construcción de `_edge_km`.
   - Verificación:
     ```bash
     python3 -m py_compile "/.../Mexico map/mexico_graph.py"
     python3 -c "import sys; sys.path.insert(0, 'Mexico map'); from mexico_graph import MexicoGraph; g=MexicoGraph(); assert len(g._edge_km)==2565, len(g._edge_km); assert g.cost(6,280)==7.28; assert g.connected"
     ```
     Criterio "done": `len(_edge_km)==2565`, `cost(6,280)==7.28`, `connected is True`.

2. **Corregir `mexico_problem.py` (Bug A).**
   - `graph.node_count_safe` → `graph.has_city(...)` (dos sitios).
   - Verificación: `py_compile` + import sin errores + `MexicoRouteProblem(g,6,25)`
     no lanza.

3. **Crear `find_route.py`** (sección 4).
   - Verificación: `py_compile`.

4. **Batería CLI.**
   - Vecinos de prueba: `python find_route.py --from-city Tijuana --to Tijuana`
     (mismo nodo) y una pareja de pueblos vecinos (elegir dos conectados por
     arista, p. ej. consultar `g.actions(6)` y usar ese vecino) → 1 hop.
   - **P1** `--from-city Tijuana --to Cancún` → esperado cost `4528.20`,
     hops `124`, expanded `949` (tabla 1). Imprimir todo + truncado de path.
   - **P2** `--from-city Mexico City --to Monterrey` → `1041.87` / `27`.
   - **P3** `--from-city Guadalajara --to Mérida` → `1984.75` / `70`.
   - **P4** `--from-city Hermosillo --to Oaxaca` → `2361.45` / `62`.
   - **Desambiguación (AC5):** `--from-city Puebla --to Cancún` → WARNING con
     candidatos (ids 4 y 580), usa la más poblada (id 4).
   - **"Nombre, Estado":** `--from-city "Puebla, Puebla" --to Cancún` → sin
     warning, id 4.
   - **Id numérico:** `--from-city 6 --to 25`.
   - **Fuzzy:** `--from-city Cancun --to Tijuana` → WARNING fuzzy, id 25.
   - **Error:** `--from-city NoExiste` → error claro, exit ≠ 0.
   - Criterio "done": los números coinciden con la tabla 1 (o difieren por cuestión
     de orden de vecinos legítimo, y en ese caso verificado el AC6) y R6/R7 completos.

5. **Port JS + UI en `mexico_map.html`** (sección 5).
   - Añadir CSS, aside, funciones, listener, redraw.
   - Verificación sintaxis: extraer el contenido de `<script>` (líneas 127–334)
     a `/tmp/mexico_script.js` y:
     ```bash
     node --check /tmp/mexico_script.js
     ```
     (editar el HTML SIEMPRE con el bloque `<script>` intacto entre `// <script>`…)
   - Verificación en navegador (abrir `file://`):
     - P1 en los selectores → `Cost: 4528.20 km`, `Hops: 124`; ruta resaltada,
       resto atenuado, origen/destino distinguibles.
     - P2 → `1041.87` / `27`.
     - Repetir búsqueda P1 y luego P2: la primera ruta desaparece (R15).
     - Inspeccionar `nodos duplicados` en los selectores (p. ej. escribir/buscar
       "Puebla" → ver "Puebla (Puebla)" y "Puebla (Baja California)") (R13).
   - _Opcional fuerte (recomendado):_ en la consola del navegador comparar
     `aStagSearchJS(6,25)` contra CLI (costo y path) para garantizar R14.
   - Criterio "done": AC4 visual y R12/R13/R14/R15 verificados; `node --check` ok.

6. **Espejar cambios en `generate_mexico_graph.py` (D8).**
   - Copiar CSS+aside+script nuevos a `HTML_TEMPLATE` (línea ~282–619),
     **conservando `const G = __GRAPH_JSON__;`**.
   - Verificación: `python3 -m py_compile generate_mexico_graph.py` y
     `rg -n "__GRAPH_JSON__"` en el archivo sigue presente; NO ejecutar el
     generador (AC6). Opcional: render devolviendo `HTML_TEMPLATE.replace(...)`
     con un JSON mínimo en un direct/luego comparar diffs del HTML vivo vs plantilla
     (fuera de un cambio esperado = el placeholder).
   - Criterio "done": plantilla contiene la misma UI (diff texto sin el G).

7. **Documentación y cierre.**
   - Escribir `README2.md` (E3), `tasks.md` marcar todo completo, y completar
     `sdd/acceptance.md` con AC1–AC8 (E5: el reporte de media página con estado
     en la ruta larga, por qué haversine es admisible, y costo/hops/expanded de
     la larga como constancia).
   - Verificación final: re-correr P1 y P2 (CLI + mapa) y anotar evidencias
     (capturas + salidas) para E4.

---

## 7. Estrategia de pruebas y criterios "done" por archivo

Reglas generales: comparar SIEMPRE los costos del CLI contra el panel del mapa
(R14) con al menos 2 parejas (una larga). Nunca hardcodear los valores de la
tabla 1 en el código; solo sirven para validar. Evidencias (E4): salida CLI de
cada pareja + una captura del mapa corriendo P1.

| Archivo | Prueba mínima | Criterio "done" |
|---|---|---|
| `mexico_graph.py` | `py_compile` + script de asserts (una línea, paso 1) | `_edge_km` con 2565 claves; `cost(6,280)==7.28`; `connected` True; `resolve` devuelve warnings correctos en Puebla/Cancun/Puebla-Puebla. |
| `mexico_problem.py` | `py_compile` + instanciar `MexicoRouteProblem(g,6,25)` | Sin `AttributeError` (`node_count_safe` desaparecido); interfaz completa para `a_star_search`. |
| `find_route.py` | Batería del paso 4 (6 casos) | Sin errores; salida exacta de 4.3; exit códigos correctos; warnings presentes; números ≈ tabla 1. |
| `mexico_map.html` | `node --check` del script extraído + pruebas manuales de 5 | Consola limpia; costos idénticos al CLI (P1 y P2); ruta reemplazable; ruta resaltada/resto atenuado. |
| `generate_mexico_graph.py` | `py_compile` + `rg __GRAPH_JSON__` | Plantilla mirror del HTML; placeholder intacto; generador NO ejecutado (AC6). |
| `README2.md` | lectura | Comandos CLI, uso HTML, parejas, nota no-regenerar. |
| `tasks.md` / `sdd/acceptance.md` | revisión | Todo tachado / cada AC con evidencia concreta (AC1 código; AC2 fórmulas; AC3 corridas; AC4 captura; AC5 warning Puebla; AC6 diff JSON/generador no corrido; AC7 costos CLI vs mapa; AC8 sin AttributeError). |
| `sdd/requirements.md` | — | Sin tocar. |

---

## 8. Riesgos y mitigaciones

| # | Riesgo | Mitigación |
|---|---|---|
| 1 | **Regenerar `mexico_map.html`** con `generate_mexico_graph.py` borra la UI (reescribe). | Nunca ejecutar el generador (AC6). Editar a mano; espejar en `HTML_TEMPLATE`; aviso en `README2.md`. |
| 2 | **Import de `../project` frágil** (ruta, refactor, CWD). | `ROOT = Path(__file__).resolve().parent`; `PROJECT = ROOT.parent / "project"`; `try/except ImportError` con mensaje claro y salida ≠ 0. Patrón ya usado por `04_a_star_search.py`. |
| 3 | **Bug `node_count_safe`** (AC8). | Sustituir por `graph.has_city(idx)` (método existente verificado). Prueba: correr cualquier pareja sin AttributeError. |
| 4 | **Bug `_edge_km`** (descubierto en planificación, NO en requirements): solo 1 clave → `KeyError` en la primera expansión. | Corregir a comprensión con `e["source"]`/`e["target"]`; assert de 2565 claves y `cost(6,280)==7.28`. |
| 5 | **Discrepancia de costos CLI vs mapa** (R14/AC7). | Mismas semánticas (heap por (f,counter), goal al extraer, `best_g`, vecinos ordenados por id), misma fórmula haversine, mismos datos (`G` incrustado = JSON). Prueba con ≥2 parejas; tolerancia de redondeo a 2 decimales (formato de impresión, ambos IEEE doubles en la misma cuenta). |
| 6 | **Estados `int` dentro de `Node` tipado como `str`** (Rumania). | Runtime duck-typed, sin `isinstance` en `search/astar.py`. Verificado con corrida real en planificación. |
| 7 | **Nombres duplicados elegidos en silencio** (R5/AC5). | `resolve()` avisa siempre en CLI; UI usa `<select>` con `Name (State)` (nunca azar). |
| 8 | **Rutas largas (124+ nodos) saturan la salida** (R6). | `--max-print 10` (default): primeras 3 + "…" + últimas 3; el mapa muestra la ruta completa. |
| 9 | **`index` vs `id` en el JS** (el HTML usa `dataset.i` = índice del array). | Los ids son 0..999 contiguos y `G.nodes` está ordenado por id (verificado), pero teclear por `id` explícito evita suposiciones encubiertas. |
| 10 | **Flotantes: suma de costos con orden distinto** → último ulp distinto. | Python y JS suman `path_cost` en el mismo sentido (padre→hijo); display a 2 decimales; tolerancia 0.01 en comparaciones. |
| 11 | **Hover/filtro/pan-zoom interfieren con el pintado de ruta** | `redraw()` central: `highlight`, `paint`, `clear` convergen ahí; el filtro solo toca `style.display`, el transform de `world` es independiente de colores de `edgeLayer`/`nodeLayer`. |
| 12 | **Regresión del grafo / topología** (AC6). | No se toca el JSON ni la construcción; `diff`/checksum de `mexico_cities_graph.json` sin cambios; el generador no se invoca. |

---

## 9. Notas de cierre para el implementador

1. Arranca por los dos bugs (pasos 1 y 2) — sin ellos CUALQUIER corrida A\* falla.
2. Mantén el orden de vecinos por id en ambos lados; es la llave de R14.
3. No muevas/comentes el bloque `const G = ...` al editar HTML.
4. Al terminar, deja `tasks.md` y `sdd/acceptance.md` completos (son parte de la entrega E4/E5).