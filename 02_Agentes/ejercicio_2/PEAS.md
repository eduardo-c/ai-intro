### 1. Asistente virtual de voz

- **Performance:** Precisión en el reconocimiento y comprensión de los comandos por voz (>95%), bajo lag de respuesta (<1.5 segundos) y minimizacion de activaciones no deseadas o falsos positivos por ruido de fondo.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico, continuo y multiagente.
- **Actuators:** Altavoz para reproduccion de voz, envío de comandos de control a dispositivos (IoT) y llamadas a servicios de terceros mediante API.
- **Sensors:** Arreglo de micrófonos para captura de audio, adaptadores Wi-Fi/Bluetooth e historial de interacciones previas del usuario.

**Justificación del entorno:** Es parcialmente observable porque el agente solo percibe/escucha su entorno hasta cierto alcance en metros. Es dinamico y continuo porque las señales de audio cambian en tiempo real de forma ininterrumpida y el ruido ambiental puede variar mientras procesa la orden.

---

### 2. Robot aspirador doméstico

- **Performance:** Porcentaje de área limpia cubierta por ciclo (>98%), consumo eficiente de batería, evación de impactos contra muebles y evasión exitosa de caídas o atascos.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico, continuo y monoagente.
- **Actuators:** Motores para las ruedas, motor de succión de aire y indicadores sonoros/lumínicos.
- **Sensors:** Sensores mecánicos de impacto, sensores infrarrojos, sensores de caída y sensor de nivel de batería.

**Justificación del entorno:** Es parcialmente observable porque los sensores locales del robot no permiten ver el estado completo de todas las habitaciones simultáneamente. Es estocástico y dinámico debido a que objetos, muebles o mascotas pueden moverse impredeciblemente modificando el estado del piso durante la navegación.

---

### 3. Sistema de recomendación de streaming (Netflix, Spotify)

- **Performance:** Maximización de la tasa de reproduccion por inicio de sesión, tiempo de retención y porcentaje de valoraciones positivas y minimización de cancelación de suscripciones.
- **Environment:** Parcialmente observable, estocástico, secuencial, semidinámico, discreto y multiagente.
- **Actuators:** UI/UX (carruseles de sugerencias, portadas personalizadas, banners) y envío de notificaciones push.
- **Sensors:** Registros del historial de reproducción, tiempo transcurrido en cada título y metadatos del catálogo.

**Justificación del entorno:** Es parcialmente observable porque la plataforma desconoce el estado de animoo, la compañía o el entorno físico real del usuario. Es secuencial ya que cada contenido visto o rechazado modifica el perfil histórico, lo que condiciona las recomendaciones futuras en un espacio de opciones discretas.

---

### 4. Vehículo autónomo en ciudad

- **Performance:** Transporte seguro al destino, tiempo de viaje optimizado, cero infracciones de tránsito o colisiones, maximización del confort del pasajero y eficiencia energética.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico, continuo y multiagente.
- **Actuators:** Control del volante, sistema de aceleración, sistema de frenado, luces e intermitentes, claxon e interfaz de pantalla/voz para comunicación con los pasajeros.
- **Sensors:** Cámaras de visión computacional, sensores Radar, GPS, velocímetro y sensores de estado mecánico del vehículo.

**Justificación del entorno:** Se clasifica como parcialmente observable por la presencia de puntos ciegos en la calle. Es dinámico y estocástico porque los peatones y demás vehículos toman decisiones imprevistas.

---

### 5. Agente de trading algorítmico en bolsa

- **Performance:** Maximizar el retorno sobre la inversión (ROI), minimización de la pérdida y tasa alta de operaciones ganadoras.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico, continuo y multiagente.
- **Actuators:** Transmisión de órdenes financieras (compra, venta, cancelación) mediante API, ajuste dinámico de ordenes límite (*stop-loss*, *take-profit*) y rebalanceo de portafolio.
- **Sensors:** Flujo de datos del libro de órdenes en tiempo real, cotizaciones históricas de precios, indicadores financieros y feeds de noticias financieras vía API.

**Justificación del entorno:** Es parcialmente observable y multiagente porque el agente no conoce las intenciones privadas de otros participantes del mercado. Es dinámico y continuo ya que que los precios cambian en milisegundos respondiendo a la oferta y demanda.

---

### 6. Sistema de diagnóstico médico asistido por IA

- **Performance:** Minimización crítica de falsos negativos en enfermedades graves, alto grado de justificacion médica de los resultados y tiempo reducido para emitir la evaluación.
- **Environment:** Parcialmente observable, estocástico, episódico (para la clasificación individual de una imagen) o secuencial (para el seguimiento clínico), estático (durante el análisis de una imagen fija), discreto y monoagente/multiagente.
- **Actuators:** Presentación de reportes clínicos en pantalla con probabilidades del diagnostico, delimitación visual de lesiones o anomalías y sugerencia de pruebas complementarias.
- **Sensors:** Archivos de imágenes médicas (tomografías, radiografías, etc.), datos de historia clínica electrónica, signos vitales y resultados de pruebas de laboratorio.

**Justificación del entorno:** Es parcialmente observable porque las imágenes son representaciones indirectas del estado interno del paciente. Estático durante el análisis de una radiografía fija.

---

### 7. Dron de inspección de infraestructura

- **Performance:** Porcentaje de superficie inspeccionada (>99%), precisión en la detección de grietas, fugas o corrosión y tasa nula de colisiones contra la estructura.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico, continuo y monoagente.
- **Actuators:** Control de velocidad y orientación de motores (navegación 3D), orientación del soporte estabilizador, activación de capturas fotográficas/térmicas y encendido de iluminación.
- **Sensors:** Cámara de alta resolución RGB, cámara térmica/infrarroja, GPS, giroscopio, acelerómetros, altímetro y sensor de nivel de batería.

**Justificación del entorno:** Es dinámico y estocástico debido a condiciones climáticas cambiantes como ráfagas de viento o variaciones bruscas de luz natural. Es continuo tanto en la posición tridimensional como en el control de sus actuadores mecánicos.

---

### 8. Agente jugador de ajedrez

- **Performance:** Maximizacion del porcentaje de partidas ganadas, minimizacion del número de jugadas requeridas y gestión eficiente del tiempo restante en el reloj.
- **Environment:** Totalmente observable, determinista, secuencial, semidinámico, discreto y multiagente competitivo.
- **Actuators:** Ejecución de movimientos válidos de piezas en la interfaz o control de un brazo robótico físico para mover piezas.
- **Sensors:** Representación digital de la posición del tablero o sistema de visión computacional del tablero si la partida es física.

**Justificación del entorno:** Es totalmente observable y determinista porque el tablero muestra de forma transparente todo el estado del juego. Es estatico porque el tablero no cambia mientras el agente piensa.
