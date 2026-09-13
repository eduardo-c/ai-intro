# Solución — Ejercicio 1: Más capas en el perceptrón multicapa (Iris)

## 1. Archivos y evidencias

Se trabajó en **Google Colab** con copias de las dos notebooks `04 Multilayer perceptron.ipynb` (MLP a mano en NumPy) y `05 Keras - multilayer perceptron - iris.ipynb` (Keras). En cada copia se conservó la corrida original `4 × 3 × 3` y se añadió una sección "Red profunda" con topología **`4 × 3 × 3 × 3 × 3`** (dos capas ocultas extra; salida sigue siendo de 3 neuronas), manteniendo **sigmoide** en todas las capas, **η = 0.03** y **500 épocas**.

- `04 Multilayer perceptron - red profunda.ipynb` → ejecutada en Colab: `04_Multilayer_perceptron_red_profunda_colab.ipynb`
- `05 Keras - multilayer perceptron - iris - red profunda.ipynb` → ejecutada en Colab: `05_Keras_multilayer_perceptron_iris_red_profunda_colab.ipynb`

**Modificaciones en la notebook 01 (NumPy):** se actualizaron todas las partes que asumían dos capas: nueva topología con `layer1 … layer4`, `init_weights_deep()` (4 capas), el forward de `calculate_error_deep()` y el ciclo de entrenamiento con propagación **y retropropagación** completas (δ de salida a entrada: `layer4 → layer3 → layer2 → layer1`, cada δ usa los pesos y los δ de la capa siguiente).

**Modificaciones en la notebook 02 (Keras):** dos `layers.Dense(3, activation="sigmoid")` extra antes de la salida (`model_deep` con `layer1 … layer4`); `model.summary()` muestra **4 capas Dense**. Se creó un optimizador `SGD`/`MSE` nuevos para el modelo profundo (Keras no permite reutilizar un optimizer ya construido sobre otro modelo).

**Links de colab:**
- https://colab.research.google.com/drive/1JOERCs90zhkj7LTVb7H451XBChOBp6b-
- https://colab.research.google.com/drive/17OJGjvxGsp21L0knvvm7NwiX-wIwnm21#scrollTo=viTl2uNDXTX5

## 2. Resultados

| Corrida | Implementación | Topología | Error inicial | Error final (época 500) |
|---|---|---|---|---|
| 1 | NumPy (a mano) | 4×3×3 | ≈ 0.80 | **≈ 0.00–0.04** (≈ 0; la celda solo grafica, valor leído de la curva) |
| 2 | NumPy (a mano) | 4×3×3×3×3 | 0.7158 | **0.6722** |
| 3 | Keras | 4×3×3 | 0.2508 | **≈ 0.2105** |
| 4 | Keras | 4×3×3×3×3 | 0.2704 | **0.2222** (`0.2221958190202713`, impreso) |

Keras — `model.summary()`:
- Original 4×3×3: `Dense layer1 (15 params)` + `Dense layer2 (12 params)` → **27 parámetros**.
- Profunda 4×3×3×3×3: 4 `Dense(3)` → **51 parámetros** (15 + 12 + 12 + 12).

Predicción de ejemplo `[3,3,1,1]`:
- Original: `[0.3517, 0.2826, 0.2860]` → argmax clase 0 (sétosa), decisión "clara".
- Profunda: `[0.3353, 0.3338, 0.3354]` → argmax clase 0, pero casi uniforme (≈ 1/3): la red profunda quedó **indecisa**, señal de saturación.

> Nota de unidades: la notebook 01 suma el error sobre las 3 salidas y divide entre 150 (`Σ_errores/150`); Keras `MeanSquaredError` promedia sobre 150×3. Por eso los números difieren por un factor ≈3: `0.6722/3 ≈ 0.224`, muy cerca del `0.2222` de Keras profunda. Mismas salidas, misma conclusión.

## 3. Análisis comparativo

### ¿Bajó el error al añadir dos capas? ¿Igual en NumPy y Keras?
**No; en ambos casos la red más profunda quedó estancada o peor.**
- NumPy: la red original convergió a **≈ 0** (baja rápida y se aplana en el fondo del eje ~época 200–250), mientras que la profunda apenas bajó de 0.7158 a **0.6722** y se quedó plana desde las primeras épocas.
- Keras: la profunda (0.2222) terminó **ligeramente por encima** de la original (0.2105); ninguna de las dos baja bien con sigmoide+MSE+SGD.

El contraste más fuerte está en NumPy: con solo dos capas el MLP casi "resuelve" Iris (error ≈ 0), y al apilar dos capas extra deja de aprender. La profundidad, sin cambios de activación/inicialización, **empeoró el problema** en vez de mejorarlo.

### ¿Las curvas de NumPy y Keras se parecen con la misma topología?
No en detalle, y las diferencias de implementación lo explican:

1. **Orden/actualización de los datos**: la notebook 01 actualiza los pesos **por ejemplo** (SGD online, recorre los 150 en orden fijo); Keras usa SGD con **lote completo** (todo Iris por paso). Dinámicas distintas de optimización.
2. **Inicialización**: NumPy usa pesos uniformes en `[-0.5, 0.5]`; Keras usa inicialización *Glorot* por defecto (rango mayor y dependiente del número de neuronas). Una buena inicialización puede hacer que la superficial escape de la zona de saturación (ocurrió en NumPy), y una desfavorable atascarla.
3. **Detalle del backprop**: en la notebook 01 original el acumulado de la capa 1 usa el índice `layer2[i][j+1]` (transpuesto respecto al correcto `layer2[j][i+1]`); en la versión profunda se corrigió. Esto altera ligeramente la dirección de las actualizaciones entre las dos topologías.
4. **Definición de error**: factor 3 entre las métricas (ver nota).

Aun así, hay un **patrón común**: en ambas implementaciones la versión **profunda** se estanca en un error alto y su curva queda casi horizontal muy pronto; ese es el fenómeno relevante del ejercicio.

### ¿Tiene sentido que una red más profunda no aprenda mejor en Iris con sigmoides apiladas y MSE?
**Sí**, por dos razones:

1. **Gradiente que se desvanece**: con sigmoide, δ se multiplica por `σ'(z) = σ(z)(1−σ(z)) ≤ 0.25` en cada capa. Con cuatro capas apiladas, el gradiente que llega a las capas tempranas se reduce en un orden de magnitud por capa; las actualizaciones de las capas 1–2 apenas mueven los pesos, la salida se satura cerca de 0.5 y el error se mantiene alto (curvas planas: 0.67 NumPy / 0.222 Keras).
2. **Iris no necesita más capacidad**: es un problema pequeño (150 ejemplos) y casi linealmente separable por pares de clases; un `4×3×3` ya tiene holgura. Añadir capas ocultas **no añade representación útil** si no se cambia la función de activación (p. ej. ReLU), la inicialización o el optimizador; solo complica la optimización y empeora el viaje del error. Las gráficas confirman que la profundidad no acerca el error a cero, sino que lo fija en un nivel alto.
