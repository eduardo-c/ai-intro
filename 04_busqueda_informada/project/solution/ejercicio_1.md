# Ejercicio 1 — Solución: Comparar Greedy y A* en el mapa de Rumania (Oradea → Eforie)

## 1. Pareja origen–destino elegida

**Oradea → Eforie**

Elegí esta pareja porque el destino **no** es Bucharest, así que la heurística
es la **distancia euclidiana** sobre las coordenadas del mapa (no la tabla AIMA). 
Además, hay dos rutas claramente distintas para llegar (por Fagaras o por Pitesti): 
Fagaras se ve más cerca de Eforie en línea recta que Rimnicu Vilcea, pero el camino 
que pasa por Pitesti acumula menos kilómetros.

## 2. Subgrafo relevante (con km y h(n) hacia Eforie)

Subgrafo con las ciudades que aparecen en los caminos obtenidos (Greedy y A*)
y las aristas entre ellas. Los números en las aristas son km y `h` es la
distancia euclidiana a Eforie.

```
                          Oradea (h=513)
                         /        \
                        / 151    71 \
                       /            \ Zerind (no usado por ninguno)
                     Sibiu (h=391)
                  /    |   \    
            140 /    99|    \80  
               /      |     \
           Arad    Fagaras   Rimnicu Vilcea (h=349)
           (h=511) (h=301)      \     97
              \        \         \
               \     211\      Pitesti (h=253)
                \        \         \
                 \     Bucharest (h=166)
                  \     /         |
                   \ 101/          | 85
                       |          Urziceni (h=120)
                       |            | 98
                       |        Hirsova (h=64)
                       |            | 86
                       +-------> Eforie (h=0)
```

Camino de **Greedy** (6 carreteras): Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova → Eforie.

Camino de **A\*** (7 carreteras): Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova → Eforie.

Nota: Los dos caminos coinciden en el tramo Bucharest → Eforie; la
diferencia está en la primera mitad: llegar a Bucharest por **Fagaras**
(461 km) o por **Pitesti** (429 km).

## 3. Heurística usada

`02_heuristics.py` confirma qué heurística se usó:

```
python 02_heuristics.py --from-city Oradea --to Eforie
Heuristic: Euclidean distance to Eforie (map coordinates)
```

Es la **distancia euclidiana**, que es **admisible** (nunca sobrestima el costo por carretera:
la distancia en línea recta es <= km de cualquier ruta) y también
**consistente** (cumple la desigualdad triangular). 

Valores relevantes hacia Eforie:

| Ciudad         | h(n) |
|----------------|------|
| Eforie         |   0  |
| Hirsova        |  64  |
| Urziceni       | 120  |
| Bucharest      | 166  |
| Pitesti        | 253  |
| Fagaras        | 301  |
| Rimnicu Vilcea | 349  |
| Sibiu          | 391  |
| Arad           | 511  |
| Oradea         | 513  |

En la ciudad origen, los vecinos "candidatos" son Sibiu (h = 391) y Zerind
(h = 513); Greedy va a bajar por Sibiu. Después, desde Sibiu la decisión clave es
entre **Fagaras (h = 301)** y **Rimnicu Vilcea (h = 349)**: Greedy prefiere
Fagaras porque se ve más cerca (menor h), pese a que el tramo es más caro en
km.

## 4. Evidencias de ejecución

Salida de terminal de Greedy, A* y UCS (reto opcional), todos con la misma
pareja `--from-city Oradea --to Eforie`:

```
python 02_heuristics.py --from-city Oradea --to Eforie
Heuristic: Euclidean distance to Eforie (map coordinates)

  h(n)  city
      0  Eforie  <- goal
     64  Hirsova
    120  Urziceni
    160  Vaslui
    166  Bucharest
    188  Giurgiu
    231  Iasi
    253  Pitesti
    290  Neamt
    301  Fagaras
    309  Craiova
    349  Rimnicu Vilcea
    391  Sibiu
    397  Mehadia
    397  Drobeta
    406  Lugoj
    482  Timisoara
    511  Arad
    513  Zerind
    513  Oradea  <- start
```

```
python 03_greedy_best_first_search.py --from-city Oradea --to Eforie
Algorithm: Greedy best-first search
Problem:   Oradea → Eforie
Heuristic: Euclidean distance to Eforie (map coordinates)
Status:    success
Path:      Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova → Eforie
Depth:     6 roads
Cost:      730 km

  city                  g     h     f
  Oradea                   0   513   513
  Sibiu                  151   391   542
  Fagaras                250   301   551
  Bucharest              461   166   627
  Urziceni               546   120   666
  Hirsova                644    64   708
  Eforie                 730     0   730

Expanded:  6 nodes
Generated: 18 nodes
Frontier:  max size 7
```

```
$ python 04_a_star_search.py --from-city Oradea --to Eforie
Algorithm: A* search
Problem:   Oradea → Eforie
Heuristic: Euclidean distance to Eforie (map coordinates)
Status:    success
Path:      Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova → Eforie
Depth:     7 roads
Cost:      698 km

  city                  g     h     f
  Oradea                   0   513   513
  Sibiu                  151   391   542
  Rimnicu Vilcea         231   349   580
  Pitesti                328   253   581
  Bucharest              429   166   595
  Urziceni               514   120   634
  Hirsova                612    64   676
  Eforie                 698     0   698

Expanded:  11 nodes
Generated: 32 nodes
Frontier:  max size 6
```

Reto opcional (misma pareja con UCS en `Búsqueda no informada/project`, para
confirmar la optimalidad de A*):

```
$ python 03_uniform_cost_search.py --from-city Oradea --to Eforie
Algorithm: Uniform-cost search
Problem:   Oradea → Eforie
Status:    success
Path:      Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova → Eforie
Depth:     7 roads
Cost:      698 km
Expanded:  17 nodes
Generated: 43 nodes
Frontier:  max size 5
```

## 5. Tabla comparativa (Oradea → Eforie, heurística euclidiana)

| Algoritmo | Status | Path | Depth (roads) | Cost (km) | Expanded | Generated |
|---|---|---|---|---|---|---|
| Greedy best-first | success | Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova → Eforie | 6 | **730** | **6** | 18 |
| A* | success | Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova → Eforie | 7 | **698** | 11 | 32 |
| UCS (referencia) | success | Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova → Eforie | 7 | **698** | 17 | 43 |

## 6. Reporte

**¿A\* encontró el camino de menos km? ¿Greedy coincidió o se desvió?**
Sí, A* encontró el mínimo en kilómetros: **698 km** con el camino
`Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova
→ Eforie`, y lo confirma UCS (698 km con el mismo camino). Greedy **no
coincidió**: se desvió por Fagaras y llegó con **730 km** (32 km de más). Los
dos caminos solo difieren en la primera mitad: alcanzar Bucharest por Fagaras
cuesta 461 km (Oradea→Sibiu 151 + Fagaras 99 + Bucharest 211), mientras que por
Pitesti cuesta 429 km (Sibiu→Rimnicu 80 + Rimnicu→Pitesti 97 + Pitesti→Bucharest
101). El tramo Bucharest→Eforie (269 km) es idéntico en ambos.

**Punto de decisión explicado con g, h y f (en Sibiu).**
Al expandir Sibiu (g = 151), Greedy ordena la frontera solo por `h` y elige
**Fagaras** porque `h(Fagaras) = 301 < h(Rimnicu Vilcea) = 349`: ve que Fagaras
está "más cerca en línea recta" del destino y se toma ese rumbo, sin mirar
cuántos km ya recorrio ni cuánto sumarán las carreteras siguientes. A* también tiene a
Fagaras con buen `f` (`f(Fagaras) = 250 + 301 = 551` vs `f(RV) = 231 + 349 =
580`) y también lo expande, pero "no se compromete": lo deja registrado y
sigue explorando la rama de Rimnicu Vilcea. Cuando descubre Bucharest por
Pitesti llega con `g = 429` (f = 595), que es **menor** que el Bucharest por
Fagaras (`g = 461`, f = 627); por eso A* descarta la ruta de Fagaras en favor
de la más barata. La diferencia de 32 km está exactamente en esta decisión:
Fagaras "quedaba mejor" en h pero su arista a Bucharest (211 km) es mucho más
cara que la cadena Rimnicu(80) → Pitesti(97) → Bucharest(101) que A* sí tiene
en cuenta vía el costo acumulado `g`.

**¿Por qué Greedy puede devolver un camino más caro aunque h sea admisible?**
Porque una heurística admisible solo garantiza que `h(n)` no sobrestima el
costo *restante* real al destino. Greedy minimiza únicamente `h(n)` e **ignora
`g(n)`** (el costo ya recorrido) y, además, confirma la meta en cuanto la
expande, sin revisar nunca alternativas que dejó atrás en la frontera. Entonces
es perfectamente admisible ir "bajando h" a lo largo de una ruta costosa: el
supuesto "costo total real" = `g + costo real restante ≥ g + h` puede ser alto
aunque `h` sea chico, porque `g` ya se acumuló. Por eso en esta instancia
Greedy exploró menos nodos que A* (6 vs 11: "trabajó menos" porque siguió
una sola flecha de bajas h) pero topó con un camino de más kms.

**En el camino de A\*, ¿f tiende a no disminuir? Relación con la consistencia.**
Sí: a lo largo del camino óptimo los valores de `f = g + h` son **no
decrecientes** — 513, 542, 580, 581, 595, 634, 676, 698. Esto es consecuencia
directa de que `h` es **consistente**. Con consistencia `f` nunca baja
a lo largo de un camino, así que el primer goal que A* saca de la frontera es
el que minimiza `f` y, al ser `h(n_goal) = 0`, también minimiza `g`: **óptimo
en km**, tal como confirmó UCS con el mismo costo de 698 km.