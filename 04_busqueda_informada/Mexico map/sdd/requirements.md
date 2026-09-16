# SDD — Requerimientos

**Ejercicio:** Ejercicio 2 — A* para encontrar rutas en el mapa de México
(`inteligencia-artificial/Búsqueda informada/Ejercicios/ejercicio-02.md`)

**Contexto.** El proyecto `Mexico map/` tiene un grafo geográfico de **1,000
ciudades mexicanas** con lat/lon reales y aristas ponderadas en km
(`mexico_cities_graph.json`), explorable en `mexico_map.html`. Hoy el HTML solo
permite explorar; **no calcula rutas**. El A* que hay que reutilizar vive en
`Búsqueda informada/project/search/astar.py` (se puede importar o copiar con
comentario de origen). Ya existen `mexico_graph.py` (carga JSON, resuelve
nombres) y `mexico_problem.py` (problema + heurística).

**Bug conocido:** `mexico_problem.py` referencia `graph.node_count_safe` que no
existe en `MexicoGraph`. Se debe corregir a `graph.has_city(idx)` durante la
implementación.

**Reglas de oro:**

1. **No regenerar** el grafo (4-NN ∪ MST) ni el dump GeoNames.
2. **No regenerar** `mexico_map.html` con `generate_mexico_graph.py` (reescribe
   el HTML y borra la UI). Se permite editar `mexico_map.html` directamente y
   actualizar `HTML_TEMPLATE` en el generador como espejo.
3. **A*** — no BFS, no Dijkstra sin `h`, no "vecino más cercano" a mano.
4. **No cambiar** la topología del grafo (4-NN / MST).
5. Los nodos en el JSON tienen campos `id` (int), `name`, `state`, `lat`, `lon`,
   `population`. Hay **39 nombres duplicados** (ej. `Puebla`, `Guadalupe`,
   `Zaragoza`). Los estados deben modelarse con el **id entero**, no con el
   nombre (no es único).

---

## 1. Búsqueda (A*)

| # | Requerimiento | Tipo | Verificable por |
|---|---|---|---|
| R1 | El estado es **una ciudad del grafo** modelada como **id entero** del nodo JSON. La acción es ir a un vecino. El costo de arista es `edges[].km` (ya en km). | Funcional | Lectura de código de `MexicoRouteProblem` / corrida CLI |
| R2 | Usar **A\*** clásico: frontera ordenada por `f(n) = g(n) + h(n)`. Reutilizar `a_star_search` de `project/search/astar.py` (importar o copiar adaptada con comentario `# Copiado de .../astar.py`). El A* espera objeto con interfaz `start`, `actions(state)`, `result(state, action)`, `step_cost(state, action)`, `is_goal(state)` y devuelve `SearchResult` con `.status`, `.node`, `.nodes_expanded`, `.nodes_generated`, `.max_frontier`. El `Node` expone `.path()`, `.path_cost`, `.depth`. | Funcional | Salida CLI + inspección de código |
| R3 | `h(n)` = **haversine en línea recta** desde la ciudad `n` hasta el destino, calculada **al vuelo** con `lat`/`lon` usando `EARTH_KM = 6371.0`. Misma función que `generate_mexico_graph.py`. Admisible y consistente porque las aristas también son haversine (desigualdad del triángulo). No se usa tabla precomputada. | Funcional | Salida CLI ("Heuristic: …") + inspección de `make_heuristic` |
| R4 | El grafo está **conectado** (4-NN ∪ MST): debe existir camino entre **cualquier par** de ciudades. `MexicoGraph._check_connected()` lo verifica al cargar. | Supuesto verificado | Assert en código o inspección de `MexicoGraph.connected` |
| R5 | **Nombres repetidos** (~39): desambiguar de forma determinista (por id, o "Nombre, Estado", o la de mayor población) y **avisar en la salida**. Nunca elegir un nodo al azar en silencio. `MexicoGraph.resolve(text)` ya maneja esta lógica con warnings. | Funcional | Mensaje de aviso impreso en CLI cuando hay ambigüedad |
| R6 | Salida CLI que reporte al menos: **Status** (`success`/`failure`), **Path** (lista de ciudades), **Depth** (hops), **Cost** (km, float con 2 decimales), **Expanded** (nodos expandidos), **Generated** (nodos generados) y la **heurística usada** (etiqueta descriptiva). Si el camino tiene >10 nodos, imprimir primeras 3 + "…" + últimas 3 ciudades con el total completo. | Funcional | Corrida CLI e inspección de salida |
| R7 | Forma de invocación: `python find_route.py --from-city ORIGEN --to DESTINO`. Nombres deben coincidir **exactamente** con el JSON (`Mexico City`, `Cancún`, `León de los Aldama`, `Santiago de Querétaro`). Se acepta `"Nombre, Estado"` para desambiguar (ej. `"Puebla, Puebla"`). Se acepta id numérico. | Funcional | Corrida CLI |
| R8 | **Bug a corregir:** `mexico_problem.py:18` usa `graph.node_count_safe` que no existe en `MexicoGraph`. Cambiar a `graph.has_city(idx)` (método existente en `MexicoGraph`). | Funcional | Corrida de `find_route.py` sin `AttributeError` |

---

## 2. Interfaz (mapa `mexico_map.html`)

| # | Requerimiento | Tipo | Verificable por |
|---|---|---|---|
| R9 | En `mexico_map.html`, agregar **dos campos de entrada** (origen y destino) y un **botón "Find Route"** (o equivalente) en el panel lateral. | Funcional | Apertura del HTML en navegador |
| R10 | Al pulsar "Find Route", ejecutar **A\*** en el navegador sobre el JSON `G` ya incrustado en el HTML. Port del mismo algoritmo (`f = g + h` con haversine). No un simple `print`: debe ser búsqueda real con frontera. | Funcional | Inspección de código JS en el HTML |
| R11 | **Pintar la ruta:** nodos del camino y aristas usadas deben resaltarse (color/distinctivo). El resto del grafo se **atenua** (opacidad reducida). Origen y destino se marcan de forma distinguible. | Funcional | Visual en navegador |
| R12 | **Costo en km** en el panel lateral: mostrar distancia total de la ruta calculada. También mostrar depth (hops) y nodos expandidos si es posible. | Funcional | Visual en navegador |
| R13 | **Desambiguado en UI:** los campos de entrada deben resolver nombres igual que la CLI. Si hay duplicados, mostrar lista con estado (ej. "Puebla (Puebla)", "Puebla (Baja California)") para que el usuario elija. No elegir al azar. | Funcional | Probar con nombre duplicado (ej. "Puebla") |
| R14 | **Coincidencia de costos:** el costo km mostrado en el mapa debe ser **idéntico** al que produce la CLI para la misma pareja de ciudades. Ambos usan el mismo algoritmo y los mismos datos. | Funcional | Comparar salida CLI vs panel del mapa para ≥2 parejas |
| R15 | Al cambiar origen/destino y volver a buscar, la ruta anterior se reemplaza (no se acumulan rutas). | Funcional | Probar búsqueda sucesiva en navegador |

---

## 3. Parejas de prueba sugeridas

| # | Origen | Destino | Tipo | Notas |
|---|---|---|---|---|
| P1 | `Tijuana` | `Cancún` | **Larga (obligatoria)** | Península a península. Cruzar todo el país. Esperado: cientos de km, muchos hops. |
| P2 | `Mexico City` | `Monterrey` | Corta-intermedia | Centro a norte. Ciudad de México ↔ Monterrey. |
| P3 | `Guadalajara` | `Mérida` | Larga alternativa | Occidente a sureste. Cruzar la costa del golfo. |
| P4 | `Hermosillo` | `Oaxaca` | Larga alternativa | Noroeste a sureste. |

- **Obligatorio probar al menos 2 parejas** (una debe ser P1 o similar: ruta
  larga península a península).
- Nombres exactos del JSON: `Mexico City` (no `CDMX`), `Cancún` (no `Cancun`),
  `León de los Aldama`, `Santiago de Querétaro`, `Mérida` (con tilde).
- Para probar desambigüedad: `Puebla` (3+ coincidencias → aviso).
- Verificar que **CLI y mapa coinciden** en costo km para cada pareja.

---

## 4. Entrega del ejercicio

| # | Entregable | Contenido |
|---|---|---|
| E1 | **Código** en `Mexico map/` | `find_route.py` (CLI), `mexico_problem.py` (corregido), `mexico_graph.py` (sin cambios o con corrección menor), A* reutilizado (importado o copiado con comentario de origen). |
| E2 | **`mexico_map.html`** modificado | Con controles origen/destino y pintado de ruta. También actualizar `HTML_TEMPLATE` en `generate_mexico_graph.py` como espejo (para no perder la UI si alguien regenera). |
| E3 | **README corto** en `Mexico map/` | Cómo ejecutar el CLI (`python find_route.py --from-city X --to Y`). Cómo usar la ruta en el HTML (abrir, escribir ciudades, pulsar botón). |
| E4 | **Evidencias** de ≥2 parejas | Capturas del mapa con la ruta resaltada + salida del CLI para cada pareja. **Al menos 1 ruta larga** (P1 o equivalente). |
| E5 | **Reporte breve** (≈ media página) | Responder: (a) qué se usó como estado y cómo se resolvieron duplicados; (b) por qué haversine es admisible aquí; (c) costo en km, número de hops y nodos expandidos de la ruta larga. |

---

## 5. Criterios de aceptación

| AC | Criterio | Cómo verificar |
|---|---|---|
| **AC1** | **A\*** (no BFS, no UCS-sin-h, no "vecino más cercano") calcula la ruta. La frontera se ordena por `f = g + h`. | Inspección de código: buscar `heapq` + `path_cost + h(state)` en el algoritmo de búsqueda. |
| **AC2** | `h(n)` es **haversine al destino** con `EARTH_KM = 6371.0`. Admisible y consistente: las aristas también son haversine, por lo que `h(n) ≤ costo_real(n, goal)` siempre. | Inspección de código de `make_heuristic` + inspección de `haversine` en `mexico_graph.py` y `generate_mexico_graph.py` (misma fórmula). |
| **AC3** | `python find_route.py --from-city ORIGEN --to DESTINO` corre sin errores y muestra **Status, Path, Depth, Cost, Expanded, Generated, Heuristic**. Para P1 (Tijuana→Cancún), imprime camino y km. | Correr el comando con P1 y P2; verificar salida completa. |
| **AC4** | `mexico_map.html` permite elegir origen y destino y **pinta la ruta** (nodos + aristas resaltados, resto atenuado). | Abrir en navegador, buscar P1, verificar ruta visual. |
| **AC5** | Nombres ambiguos **no se resuelven en silencio**: se imprime aviso en CLI y se ofrece selector en UI. | Probar con `python find_route.py --from-city Puebla --to Cancún` y verificar warning. |
| **AC6** | El grafo **no cambió**: mismo JSON, mismas 2,565 aristas, misma topología 4-NN / MST. | `diff` del JSON o verificación de que `generate_mexico_graph.py` no se ejecutó. |
| **AC7** | CLI y mapa dan el **mismo costo km** para la misma pareja. | Comparar salida CLI con costo mostrado en el panel del mapa para ≥2 parejas. |
| **AC8** | El bug `node_count_safe` está corregido: `mexico_problem.py` usa `graph.has_city(idx)` y `find_route.py` no lanza `AttributeError`. | Correr `find_route.py` con cualquier pareja sin errores de atributo. |

---

## 6. Fuera de alcance

- Regenerar el grafo o el dump GeoNames.
- Cambiar la topología 4-NN / MST.
- Modificar la estructura de `mexico_cities_graph.json`.
- Reto opcional (comparar A* con UCS `h=0`, o con Greedy `h` solo) salvo que
  sobre tiempo. Si se implementa, documentar en el reporte.
