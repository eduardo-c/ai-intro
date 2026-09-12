# Ejercicio 1 — Solución: BFS, UCS, DFS, DLS e IDS en el mapa de Rumania

## 1. Pareja origen–destino elegida

**Oradea → Bucharest**

Elegi esta pareja de origen-destino porque tiene varias opciones 
de rutas para llegar a Bucharest (a diferencia de por ejemplo Neamt - Bucharest)

## 2. Subgrafo relevante

Ciudades que aparecen en los caminos obtenidos y sus aristas:

```
Camino que toman BFS, DLS(3/4) e IDS (3 carreteras):

          Oradea ──151── Sibiu ──99── Fagaras ──211── Bucharest

Camino que toma UCS (4 carreteras, menos km):

          Oradea ──151── Sibiu ──80── Rimnicu Vilcea ──97── Pitesti ──101── Bucharest

Rama que DFS recorre antes de llegar a Bucharest (9 carreteras):

          Oradea ──151── Sibiu ──140── Arad ──118── Timisoara ──111── Lugoj ──70──
          Mehadia ──75── Drobeta ──120── Craiova ──138── Pitesti ──101── Bucharest
```

## 3. Tabla comparativa (Oradea → Bucharest)

| Algoritmo | Status | Path | Depth (roads) | Cost (km) | Expanded | Generated |
|---|---|---|---|---|---|---|
| BFS | success | Oradea → Sibiu → Fagaras → Bucharest | 3 | 461 | 5 | 13 |
| UCS | success | Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest | 4 | **429** | 10 | 27 |
| DFS | success | Oradea → Sibiu → Arad → Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest | 9 | 1024 | 9 | 24 |
| DLS (`--limit 2`) | **cutoff** | — | — | — | 3 | 9 |
| DLS (`--limit 3`) | success | Oradea → Sibiu → Fagaras → Bucharest | 3 | 461 | 4 | 8 |
| DLS (`--limit 4`) | success | Oradea → Sibiu → Fagaras → Bucharest | 3 | 461 | 6 | 12 |
| IDS | success (`last_limit=3`) | Oradea → Sibiu → Fagaras → Bucharest | 3 | 461 | 8 | 21 |

## 4. Evidencias de ejecución

Salida de terminal de los cinco algoritmos con `--from-city Oradea --to Bucharest`:

```
$ python 02_breadth_first_search.py --from-city Oradea --to Bucharest
Algorithm: Breadth-first search
Problem:   Oradea → Bucharest
Status:    success
Path:      Oradea → Sibiu → Fagaras → Bucharest
Depth:     3 roads
Cost:      461 km
Expanded:  5 nodes
Generated: 13 nodes
Frontier:  max size 4
```

```
$ python 03_uniform_cost_search.py --from-city Oradea --to Bucharest
Algorithm: Uniform-cost search
Problem:   Oradea → Bucharest
Status:    success
Path:      Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest
Depth:     4 roads
Cost:      429 km
Expanded:  10 nodes
Generated: 27 nodes
Frontier:  max size 4
```

```
$ python 04_depth_first_search.py --from-city Oradea --to Bucharest
Algorithm: Depth-first search
Problem:   Oradea → Bucharest
Status:    success
Path:      Oradea → Sibiu → Arad → Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest
Depth:     9 roads
Cost:      1024 km
Expanded:  9 nodes
Generated: 24 nodes
Frontier:  max size 4
```

```
$ python 05_depth_limited_search.py --from-city Oradea --to Bucharest --limit 2
Algorithm: Depth-limited search
Problem:   Oradea → Bucharest
Status:    cutoff
Detail:    limit=2
Expanded:  3 nodes
Generated: 9 nodes
Frontier:  max size 6
```

```
$ python 05_depth_limited_search.py --from-city Oradea --to Bucharest --limit 3
Algorithm: Depth-limited search
Problem:   Oradea → Bucharest
Status:    success
Detail:    limit=3
Path:      Oradea → Sibiu → Fagaras → Bucharest
Depth:     3 roads
Cost:      461 km
Expanded:  4 nodes
Generated: 8 nodes
Frontier:  max size 6
```

```
$ python 05_depth_limited_search.py --from-city Oradea --to Bucharest --limit 4
Algorithm: Depth-limited search
Problem:   Oradea → Bucharest
Status:    success
Detail:    limit=4
Path:      Oradea → Sibiu → Fagaras → Bucharest
Depth:     3 roads
Cost:      461 km
Expanded:  6 nodes
Generated: 12 nodes
Frontier:  max size 6
```

```
$ python 06_iterative_deepening_search.py --from-city Oradea --to Bucharest
Algorithm: Iterative deepening search
Problem:   Oradea → Bucharest
Status:    success
Detail:    last_limit=3
Path:      Oradea → Sibiu → Fagaras → Bucharest
Depth:     3 roads
Cost:      461 km
Expanded:  8 nodes
Generated: 21 nodes
Frontier:  max size 6
```

## 5. Reporte

**¿BFS encontró el camino con menos carreteras? ¿UCS el de menos km?**
Sí. BFS devolvió `Oradea → Sibiu → Fagaras → Bucharest` (3 carreteras), el
mínimo de carreteras posible en este mapa, a cambio de **461 km**. 

UCS devolvió `Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest` (**429 km**, el mínimo
en kilómetros) a cambio de 1 carretera mas (4). Es decir, **ambos son
óptimos en su propia métrica**, y por eso discrepan.

BFS minimiza profundidad (aristas) sin mirar costos, mientras UCS ordena la frontera 
por costo acumulado y encuentra el camino más barato aunque sea más largo en saltos. En este mapa
UCS exploro mas nodos (10 nodos expandidos vs. 5 de BFS), precisamente porque no
puede detenerse en el primer goal alcanzado y debe confirmar que no hay una ruta
más barata pendiente en la frontera.

**¿Por qué DFS puede devolver un camino más largo aunque el grafo sea el mismo?**
Porque DFS explora a fondo antes que en anchura: desde Oradea baja por
`Sibiu → Arad → Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti` y
recién ahí encuentra Bucharest (debido al orden en el que genera y añade nodos en la cola), 
con un camino de 9 carreteras y **1024 km**. No usa ningún criterio de costo ni garantiza 
optimalidad: el primer goal que descubre es el que devuelve. La expansión en orden 
alfabético hace el resultado determinista, pero no "inteligente".

**¿Con qué `--limit` DLS pasó de cutoff a solución?**
Con `--limit 3` encontró la solución `Oradea → Sibiu → Fagaras → Bucharest`, idéntica 
a la de BFS/IDS. Esto se correlaciona directamente con la profundidad del óptimo por hops: 
el límite mínimo útil coincide con la profundidad del camino de BFS/IDS
(`last_limit=3` de IDS lo confirma). IDS repitió DLS con límites 0, 1, 2 y 3 y
encontró el mismo camino que BFS, validando que IDS hereda la optimalidad por
hops o carreteras de BFS.
