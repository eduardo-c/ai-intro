# Introducción a la Inteligencia Artificial
Repositorio para la materia "Introduccion a la Inteligencia Artificial"

**Facultad de Matemáticas — Universidad Autónoma de Yucatán**  
**Programa:** Maestría en Inteligencia Artificial (MIA)  
**Modalidad:** Presencial  

---

## I. Contenido Temático

| Semana | Unidad | Temas | Horas Totales |
| :---: | :--- | :--- | :---: |
| **1** | **Unidad 1.** Fundamentos de la Inteligencia Artificial | • Conceptos básicos de IA<br>• Agentes<br>• Búsqueda no informada<br>• Búsqueda informada | 8 |
| **2** | **Unidad 2.** Razonamiento y cómputo evolutivo | • Razonamiento lógico<br>• Razonamiento probabilístico<br>• Árboles de decisión<br>• Cómputo evolutivo | 8 |
| **3** | **Unidad 3.** Aprendizaje automático y visión computacional | • Perceptrón multicapa<br>• Clustering K-medias<br>• Q-learning<br>• Visión computacional | 8 |
| **4** | **Unidad 4.** Modelos de lenguaje y generación aumentada | • LLMs<br>• RAG<br>• Desarrollo del proyecto final I (estudio independiente)<br>• Desarrollo del proyecto final II y presentación (estudio independiente) | 4 |

---

## II. Secuencia Didáctica

### Unidad 1: Fundamentos de la Inteligencia Artificial
> **Competencia de la unidad:** Aplica los fundamentos conceptuales de la inteligencia artificial y el paradigma de agentes, así como estrategias de búsqueda no informada e informada, para la resolución de problemas computacionales básicos.

| Sem. | Tema | HMD | Actividad de Aprendizaje | Evidencia de Aprendizaje | HEI | Instrumento de Evaluación | Puntaje |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| **1** | Conceptos básicos de IA | 2 | Explorar qué es la IA y la prueba de Turing; revisar brevemente la historia de la IA y sus paradigmas (simbólico, conexionista y estadístico); distinguir IA débil y fuerte; configurar el entorno de desarrollo. | Mapa conceptual de paradigmas de IA y entorno de desarrollo configurado. | 5 | Lista de cotejo de laboratorio | — |
| **1** | Agentes | 2 | Analizar tipos de agentes (reflejo simple, basado en modelos, basado en objetivos y basado en utilidad); aplicar el marco PEAS y las propiedades del entorno; implementar un agente reactivo. | Agente de reflejo simple implementado para un entorno de cuadrícula (grid-world). | 5 | Lista de cotejo de laboratorio | — |
| **1** | Búsqueda no informada | 2 | Formular problemas en términos de estados, acciones y prueba de meta; comparar árboles y grafos de búsqueda; implementar búsqueda en anchura, en profundidad y de costo uniforme; analizar completitud, optimalidad y complejidad. | Implementación de BFS, DFS y UCS para resolver un rompecabezas de búsqueda de ruta (8-puzzle o laberinto). | 5 | Lista de cotejo de laboratorio | — |
| **1** | Búsqueda informada | 2 | Aplicar búsqueda voraz primero el mejor; implementar A* con heurísticas admisibles y consistentes; comparar el desempeño contra búsqueda no informada. | Implementación de A* con heurística personalizada, comparada contra búsqueda no informada. | 5 | Rúbrica | — |

---

### Unidad 2: Razonamiento y Cómputo Evolutivo
> **Competencia de la unidad:** Representa y razona sobre el conocimiento mediante lógica y modelos probabilísticos, e implementa árboles de decisión y algoritmos evolutivos para la resolución de problemas de clasificación y optimización.

| Sem. | Tema | HMD | Actividad de Aprendizaje | Evidencia de Aprendizaje | HEI | Instrumento de Evaluación | Puntaje |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| **2** | Razonamiento lógico | 2 | Aplicar la sintaxis y semántica de la lógica proposicional y de primer orden; construir bases de conocimiento; aplicar reglas de inferencia, unificación y tablas de verdad; introducir solucionadores SAT y el razonamiento al estilo Prolog. | Base de conocimiento consultada con un motor de inferencia simple (tablas de verdad o resolución). | 5 | Lista de cotejo de laboratorio | — |
| **2** | Razonamiento probabilístico | 2 | Repasar teoría de la probabilidad y la regla de Bayes; construir redes bayesianas (estructura e independencia); aplicar inferencia exacta y aproximada. | Red bayesiana construida y consultada con `pgmpy` o una biblioteca similar. | 5 | Lista de cotejo de laboratorio | — |
| **2** | Árboles de decisión | 2 | Analizar el aprendizaje supervisado y la partición train/test; construir árboles de decisión (ID3/CART); aplicar medidas de impureza (entropía, Gini); analizar sobreajuste y poda. | Clasificador de árbol de decisión entrenado sobre un dataset de referencia con `scikit-learn`, con visualización del árbol y métricas de evaluación. | 5 | Rúbrica | — |
| **2** | Cómputo evolutivo | 2 | Analizar los fundamentos de la computación evolutiva (población, selección, cruza y mutación); implementar un algoritmo genético; comparar con búsqueda local (ascenso de colinas y temple simulado). | Algoritmo genético implementado para un problema de optimización (por ejemplo, n-reinas o una función continua). | 5 | Rúbrica | — |

---

### Unidad 3: Aprendizaje Automático y Visión Computacional
> **Competencia de la unidad:** Implementa modelos introductorios de aprendizaje automático supervisado, no supervisado y por refuerzo, y aplica fundamentos de visión computacional a problemas de clasificación de imágenes.

| Sem. | Tema | HMD | Actividad de Aprendizaje | Evidencia de Aprendizaje | HEI | Instrumento de Evaluación | Puntaje |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| **3** | Perceptrón multicapa | 2 | Analizar el perceptrón y el perceptrón multicapa; aplicar funciones de activación; comprender la propagación hacia adelante y la intuición del descenso de gradiente; introducir la retropropagación. | Red neuronal feedforward simple entrenada con Keras/PyTorch sobre MNIST. | 5 | Lista de cotejo de laboratorio | — |
| **3** | Clustering K-medias | 2 | Distinguir el aprendizaje no supervisado; aplicar el algoritmo k-medias; analizar inicialización, elección de k (método del codo y silueta) y limitaciones. | Clustering k-medias sobre un dataset de referencia, con visualización de clusters y justificación del valor de k. | 5 | Lista de cotejo de laboratorio | — |
| **3** | Q-learning | 2 | Introducir el aprendizaje por refuerzo (agente, entorno, recompensa y política); formalizar procesos de decisión de Markov; implementar Q-learning tabular; analizar el equilibrio exploración-explotación. | Agente Q-learning que aprende una política en un grid-world o entorno simple. | 5 | Rúbrica | — |
| **3** | Visión computacional | 2 | Revisar fundamentos de visión por computadora (imagen digital, filtros y detección de características); aplicar clasificación de imágenes con un modelo introductorio o preentrenado; relacionar con redes convolucionales a nivel conceptual. | Pipeline de clasificación de imágenes sobre un dataset de muestra (por ejemplo, dígitos o un modelo preentrenado). | 5 | Rúbrica | — |

---

### Unidad 4: Modelos de Lenguaje y Generación Aumentada
> **Competencia de la unidad:** Aplica grandes modelos de lenguaje e integración RAG para construir soluciones de procesamiento de lenguaje, e integra un proyecto final con rigor técnico.

| Sem. | Tema | HMD | Actividad de Aprendizaje | Evidencia de Aprendizaje | HEI | Instrumento de Evaluación | Puntaje |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| **4** | LLMs | 2 | Aplicar representación de texto (tokenización y embeddings); introducir la arquitectura Transformer y el mecanismo de atención; revisar el panorama de los grandes modelos de lenguaje; aplicar ingeniería de prompts (zero-shot y few-shot) y evaluar salidas de LLM. | Experimento de prompting (zero-shot y few-shot) sobre una tarea de NLP usando una API de LLM, con evaluación de las salidas. | 5 | Lista de cotejo de laboratorio | — |
| **4** | RAG | 2 | Comparar fine-tuning con generación aumentada por recuperación (RAG); construir un índice de documentos y un pipeline de recuperación; aplicar el uso responsable de APIs de LLM. | Pipeline RAG simple construido sobre un corpus pequeño usando una API de LLM. | 5 | Rúbrica | — |
| **4** | Desarrollo del proyecto final I (estudio independiente) | 0 | Seleccionar de forma independiente un problema que integre búsqueda, razonamiento, aprendizaje automático y/o modelos de lenguaje; diseñar e iniciar la implementación; recibir apoyo asíncrono vía foros/asesorías; construir el portafolio digital. | Avance documentado del proyecto y del portafolio digital. | 15 | Rúbrica de avance de proyecto | — |
| **4** | Desarrollo del proyecto final II y presentación (estudio independiente) | 0 | Finalizar de forma independiente la implementación y los resultados; preparar la presentación oral y el portafolio digital; presentar y entregar el proyecto final. | Proyecto final entregado, presentado oralmente y documentado en el portafolio digital. | 15 | Rúbrica de proyecto final y presentación | 25% |

---

## III. Evaluación de Producto

| Semana | Evaluación de Producto | Instrumento de Evaluación | Puntaje |
| :---: | :--- | :--- | :---: |
| **1-4** | Prácticas de laboratorio semanales | Lista de entregables | **30%** |
| **1-4** | Portafolio digital | Repositorio GitHub | **20%** |
| **4** | Proyecto final | Rúbrica de proyecto final | **25%** |

---

## IV. Recursos de Apoyo

* **Lenguaje:** Python 3.10+
* **Bibliotecas principales:** NumPy, scikit-learn, Matplotlib, NetworkX y pgmpy.
* **Aprendizaje profundo, visión y refuerzo:** PyTorch o TensorFlow/Keras, OpenCV y Gymnasium.
* **Herramientas de LLM:** API de OpenAI u otras APIs de LLM de código abierto, Hugging Face Transformers y LangChain (para RAG).
* **Entorno de desarrollo:** Jupyter Notebook/JupyterLab o VS Code con extensión de Python.
* **Datasets:** UCI Machine Learning Repository, Kaggle y OpenML.

---

## V. Referencias

### Bibliografía Básica
1. Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4.ª ed.). Pearson.
2. Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2.ª ed.). MIT Press.
3. Ozdemir, S. (2024). *Quick Start Guide to Large Language Models: Strategies and Best Practices for Using ChatGPT and Other LLMs*. Addison-Wesley.

### Bibliografía Complementaria
1. Eiben, A. E., & Smith, J. E. (2015). *Introduction to Evolutionary Computing* (2.ª ed.). Springer.
2. Bouchard, L.-F., & Peters, L. (2024). *Building LLMs for Production: Enhancing LLM Abilities and Reliability with Prompting, Fine-Tuning, and RAG*. Publicación independiente.
3. Tunstall, L., Von Werra, L., & Wolf, T. (2022). *Natural Language Processing with Transformers: Building Language Applications with Hugging Face*. O'Reilly.
4. Aggarwal, C. C. (2023). *Neural Networks and Deep Learning: A Textbook*. Springer.
