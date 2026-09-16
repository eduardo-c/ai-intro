# Entrega del Ejercicio 2 — A* para encontrar rutas en el mapa de México

Esta entrega extiende `Mexico map/` con dos opciones de ruta sobre el grafo de
ciudades mexicanas (1,000 ciudades, 2,565 aristas, 4-NN ∪ MST, conectado): un CLI
(`find_route.py`) y la sección **Find route** en el mapa interactivo. Ambos
corren el mismo A*, con la misma heurística, sobre el mismo grafo.

## Implementacion

Se creó find_route.py que importa a_star_search desde ../project/search/astar.py sin modificar Rumania (para que este
proyecto funcione, se debe mantener la carpeta project en el mismo directorio como sibbling folder), 
y se añadio a mexico_map.html la sección Find Route con ambos selectores (Nombre — Estado para duplicados) 
y un port JS de A* con semánticas idénticas al Python.                                                                                        
                                                                                                       
## Resultados verificados (CLI == mapa):                                                             
                                                                                                       
- Tijuana → Cancún: 4528.20 km · 124 hops · 949 expanded                                          
- Mexico City → Monterrey: 1041.87 km · 27 hops · 428 expanded                                    
- Guadalajara → Mérida: 1984.75 km · 70 hops · 736 expanded                                       
- Puebla → imprime WARNING y desambigua por población; Puebla, Puebla no avisa                    
                                                                                                       
El agente de aceptación re-ejecutó todo de forma independiente: los 8 criterios satisfechos, el conteo/nodo/g h 
coinciden entre el port JS y el CLI, el grafo no se regeneró (1000/2565 aristas intactas) y node --check pasa.

## Cómo ejecutar el CLI

Desde el directorio `Mexico map/`:

```bash
python3 find_route.py --from-city Tijuana --to Cancún
python3 find_route.py --from-city "Mexico City" --to Monterrey
python3 find_route.py --from-city "Puebla, Puebla" --to Monterrey
```

Opciones:

- `--from-city ORIGEN` — ciudad de salida. Por defecto `Tijuana`.
- `--to DESTINO` — ciudad de llegada. Por defecto `Cancún`.
- `--max-print N` — trunca el listado del camino a las primeras/últimas
  ciudades cuando la ruta es larga. Por defecto 14. Usa `0` para imprimir el
  camino completo.

Los nombres deben coincidir **exactamente** con el JSON (`Mexico City`, no
`CDMX`; `Cancún`, no `Cancun`). Se aceptan tres formatos:

| Formato | Ejemplo |
|---|---|
| Nombre exacto único | `--from-city Tijuana --to Cancún` |
| `"Nombre, Estado"` para desambiguar | `--from-city "Puebla, Puebla"` |
| Id numérico del nodo | `--from-city 6 --to 25` |

Si un nombre tiene duplicados (p. ej. `Puebla`), el CLI imprime una línea
`WARNING:` con los candidatos y elige el de mayor población. Nunca elige en
silencio; usa `"Nombre, Estado"` o el id para evitarlo.

La salida reporta el algoritmo, la heurística usada, `Status`, `Path`, `Depth`
(hops), `Cost` en km, una tabla `g/h/f` por ciudad y `Expanded`, `Generated` y
`Frontier`:

```
$ python3 find_route.py --from-city Tijuana --to Cancún
Algorithm: A* search
Problem:   Tijuana → Cancún
Heuristic: haversine straight-line distance to Cancún (km)
Status:    success
Path:      Tijuana → Villa del Prado 2da Sección → … → Tulum → Playa del Carmen → Cancún  (125 cities; showing first/last 7)
Depth:     124 roads
Cost:      4528.20 km
Expanded:  949 nodes
Generated: 4886 nodes
Frontier:  max size 89
```

Resultados verificados para las parejas de prueba:

| Ruta | Cost (km) | Hops | Expanded |
|---|---|---|---|
| Tijuana → Cancún | 4528.20 | 124 | 949 |
| Mexico City → Monterrey | 1041.87 | 27 | 428 |
| Guadalajara → Mérida | 1984.75 | 70 | 736 |
| Puebla (desambiguada) → Monterrey | 1121.15 | 30 | 452 |

## Cómo usar la ruta en el HTML

Abre `mexico_map.html` en un navegador (los datos ya van incrustados; no hace
falta servidor):

```bash
open mexico_map.html      # macOS
xdg-open mexico_map.html  # Linux
```

En el panel lateral:

1. En la sección **Find route**, elige **From** y **To** en los desplegables.
   Cada ciudad aparece como `Nombre — Estado`, de modo que los nombres repetidos
   (como las dos `Puebla`) quedan distinguibles.
2. Pulsa el botón **Find Route**.
3. El panel `routeResult` muestra el costo total (`Cost: 4528.20 km`), los hops
   y los nodos expandidos (`Nodes expanded`).
4. El mapa resalta la ruta: nodos y aristas del camino en verde, origen y
   destino con marcas distinguibles, y el resto del grafo atenuado. Cambiar
   From/To y pulsar de nuevo el botón reemplaza la ruta anterior.

El costo del panel coincide con el del CLI para la misma pareja porque ambos
usan el mismo A* y el mismo grafo.

## De dónde sale A*

- `find_route.py` **importa** `a_star_search` (no lo copia) desde la copia de
  `Búsqueda informada/project/search/astar.py` vía `../project` (`find_route.py:27-29`).
- El estado es el **id entero** de la ciudad, no el nombre (hay ~39 nombres
  repetidos). El costo de arista es `edges[].km`.
- La heurística es la **distancia haversine en línea recta** desde la ciudad `n`
  hasta el destino (`mexico_problem.py`, `make_heuristic`). Como las aristas
  también se miden con haversine, `h` nunca sobreestima y A* es óptimo en km.
- El HTML contiene un port en JavaScript del mismo algoritmo (`aStagSearchJS`,
  frontera por `f = g + h` con haversine) sobre el grafo incrustado, por eso el
  costo coincide con el CLI.

## Advertencia

**No regeneres** el grafo con `generate_mexico_graph.py`: ese script reescribe
`mexico_map.html` y `mexico_cities_graph.json`, y borraría la sección **Find
route** y la UI editada a mano. Solo se debe tocar el HTML a mano (la plantilla
`HTML_TEMPLATE` del generador se mantuvo en espejo para no perder la UI).

## Nota

La carpeta SDD, contiene los archivos generados por los agentes usados con la 
metodologia Spec-Driven Development (SDD)

# Mexico as a 1,000-city graph

A geographic graph of Mexico: **1,000 cities** pinned to real latitude/longitude, linked by proximity rather than a force-directed layout.

Open [`mexico_map.html`](mexico_map.html) in a browser to explore it. Search a city, filter by state, hover a node for its neighborhood, and pan/zoom the map. Circle size is log population.

| | |
| --- | --- |
| Nodes | 1,000 |
| Edges | 2,565 |
| Mean edge | 31.55 km |
| MST bridges | 10 |

## How the graph is built

1. Load Mexican populated places from [GeoNames `cities1000`](https://download.geonames.org/export/dump/) (`data/cities1000.txt`).
2. Keep the most populous 1,000 places with at least **3 km** of separation, so stacked suburbs do not collapse into one pixel.
3. Connect each city to its **4 nearest neighbors** by haversine distance. That local mesh already looks like a road sketch.
4. Union a **minimum spanning tree** so remote ends (Baja California, Yucatán, the northern border) stay in one connected component. Ten of those MST edges are bridges that were not already in the 4-NN mesh.

Layout is longitude × latitude, not a scramble.

## Regenerating

Python 3, no extra packages for the graph and HTML:

```bash
python3 generate_mexico_graph.py
```

That writes:

- `mexico_cities_graph.json` — nodes, edges, coast outline, and metadata
- `mexico_map.html` — self-contained interactive map (graph JSON inlined)

Optional static PNG (needs matplotlib):

```bash
python3 emit_viz.py
```

Writes `mexico_graph_preview.png` from the current graph JSON.

## Files

```
generate_mexico_graph.py   build graph, HTML, and adjacency matrix
emit_viz.py                PNG preview from mexico_cities_graph.json
mexico_map.html            interactive map
mexico_cities_graph.json   graph payload
data/cities1000.txt        GeoNames dump (CC-BY 3.0)
data/mexico.geojson        country outline
```

## Data

City coordinates and populations come from [GeoNames](https://www.geonames.org/) `cities1000`, licensed [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Admin-1 codes in that dump are the historic GeoNames numbering, mapped to state names in `generate_mexico_graph.py`.