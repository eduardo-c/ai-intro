# Solución — Ejercicio 1: Cambiar la imagen de predicción en YOLO

## 1. Archivos y evidencias

Se trabajó sobre una **copia** de `13 YOLO ultralytics.ipynb` ejecutada en **Google Colab** con runtime **GPU (Tesla T4)**. En la copia se conservó la corrida original (celdas de predicción con `zidane.jpg` y `bus.jpg`) y se **duplicaron** las celdas de predicción apuntando a una **imagen propia** (misma URL en ambas).

- Copia de la notebook modificada y ejecutada: `13_YOLO_ultralytics.ipynb`
- Enlace de Colab: https://colab.research.google.com/drive/1ljmL6ur01zbawPXlERpbf-meijFFb_jb#scrollTo=A3CFdMbnN67T
- Evidencia de ejecución en Colab (entorno/runtime con GPU): `colab-evidencia.pdf`

**Único cambio de código:** el argumento `source='...'` de la celda CLI y el argumento de `model('...', save=True)` de la celda Python, ambos apuntando a `https://stilloutriding.com/wp-content/uploads/2025/06/X1005967-1920x1280.jpg`. Se mantuvieron `yolov8n.pt`, `epochs=3` y `coco128.yaml`.

## 2. Resultados

### Predicciones originales (imágenes de Ultralytics)

| Imagen | Clases detectadas | Cajas | Entrada procesada | Inferencia | Salida |
|---|---|---|---|---|---|
| `zidane.jpg` (CLI) | **2 person, 1 tie** | 3 | 384×640 | 6.9 ms | `runs/detect/predict` |
| `bus.jpg` (model()) | **4 person, 1 bus, 1 stop sign** | 6 | 640×480 | 6.5 ms | `runs/detect/predict-2` |

### Predicciones sobre mi imagen

| Imagen | Clases detectadas | Cajas | Entrada procesada | Inferencia | Salida |
|---|---|---|---|---|---|
| `X1005967-1920x1280.jpg` (CLI) | **1 person, 1 bicycle** | 2 | 448×640 | 8.1 ms | `runs/detect/predict-3` |
| `X1005967-1920x1280.jpg` (model()) | **1 person, 1 bicycle** | 2 | 448×640 | 6.3 ms | `runs/detect/predict-4` |

Capturas: `zidane-result.png`, `bus-result.png`, `my-image-result-cli.png` y `my-image-result-yolo.png`.

### Entrenamiento (fine-tune de 3 épocas en coco128)

Las dos corridas de entrenamiento arrojaron resultados idénticos. Mejor época (3/3): **mAP50 = 0.658, mAP50-95 = 0.488, P = 0.698, R = 0.564**. Validación de `best.pt`: mAP50 = 0.659, mAP50-95 = 0.487 sobre las 128 imágenes de validación (929 instancias).

## 3. Análisis comparativo

### ¿Qué clases detectó YOLO en las fotos de Ultralytics y cuáles en la tuya?

- **Zidane**: `person` (2) y `tie` (1) — una persona y otra persona con corbata anudada.
- **Bus**: `person` (4), `bus` (1) y `stop sign` (1) — escena callejera típica de COCO.
- **Mi imagen**: `person` (1) y `bicycle` (1) — ciclista sobre su bicicleta; la foto es COCO-friendly porque tanto la persona como la bicicleta son clases del dataset.

### ¿Algún objeto evidente de tu foto no salió etiquetado?

No; en la foto no quedó ningún objeto evidente sin etiqueta: el ciclista y la bicicleta se detectaron correctamente. Aun así conviene anotar las causas por las que YOLO *podría* fallar en fotos similares: accesorios típicos de ciclista (casco, botella de agua, lentes) **no son clases de COCO** (solo 80 clases), y el umbral por defecto `conf=0.25` descarta cajas de baja confianza. En este caso ninguna de esas situaciones aplicó.

### ¿Coincide la predicción de la celda CLI con la de `model(...)` sobre tu misma imagen?

**Sí.** Ambas corridas (CLI y Python) detectaron exactamente lo mismo: **1 `person` y 1 `bicycle`**, sobre el mismo archivo descargado en `/content/`. Solo difieren los tiempos de preprocesado/cómputo reportados (8.1 vs 6.3 ms de inferencia), dentro de la variabilidad normal entre ejecuciones del mismo modelo; el resultado (cajas y etiquetas) es idéntico.