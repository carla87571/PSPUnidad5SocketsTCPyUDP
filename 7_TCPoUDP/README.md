# 🚀 Unidad 7: ¿TCP o UDP? Práctica Eco, Retos y Preparación de Entrevistas

Bienvenido a la unidad final y de síntesis práctica sobre **¿TCP o UDP?**, la comparativa cara a cara de **Servidores Eco**, los **6 Retos Prácticos**, y la preparación técnica para **Entrevistas de Trabajo**.

---

## 📂 Contenido del Módulo

| Archivo | Diapositivas relacionadas | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_criterio_de_decision_tcp_vs_udp.py`](./01_criterio_de_decision_tcp_vs_udp.py) | **Diapositivas 1, 2 y 3** | Criterio de decisión ("¿Fiabilidad o Velocidad?"), tabla de casos reales (Web, Correo, DNS, VoIP, Juegos), streaming moderno HLS/DASH sobre TCP, y el protocolo QUIC (HTTP/3). |
| [`02_practica_eco_cara_a_cara.py`](./02_practica_eco_cara_a_cara.py) | **Diapositivas 4, 5, 6 y 7** | Práctica Eco TCP (puerto 9000) vs Eco UDP (puerto 9001), tabla comparativa cara a cara de métodos y comportamientos. |
| [`03_los_seis_retos_practicos.py`](./03_los_seis_retos_practicos.py) | **Diapositivas 8, 9 y 10** | Solución y ejecución de los 6 retos: Eco TCP, Eco UDP, Contador de letras, Servidor de hora, Cliente con timeout y Benchmark de velocidad en milisegundos. |
| [`04_se_el_socket_y_quien_soy.py`](./04_se_el_socket_y_quien_soy.py) | **Diapositivas 11 y 12** | La historia en primera persona ("Sé el socket") y juego interactivo "¿Quién soy?" con 10 adivinanzas conceptuales. |
| [`05_simulador_entrevista_tecnica.py`](./05_simulador_entrevista_tecnica.py) | **Diapositiva 13** | Las 6 preguntas reina de entrevistas técnicas de redes y backend con respuestas modelo y puntos clave. |
| [`06_ejemplo_vida_real.py`](./06_ejemplo_vida_real.py) | *Aplicación práctica* | Arquitectura Híbrida estilo Discord / Zoom: Chat de texto fiable por TCP (puerto 9200) y transmisión de voz por UDP (puerto 9201). |

---

## 🖼 Diapositivas

Todas las diapositivas originales del bloque se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: ¿TCP o UDP? La pregunta correcta (Carta certificada vs Avión de papel, y QUIC).
* `2.PNG`: Casos reales: La tabla que se repite en las entrevistas.
* `3.PNG`: Mini-chequeo: criterio de decisión (¿Dato intacto o fluidez?).
* `4.PNG`: Práctica eco: La idea en una frase.
* `5.PNG`: Eco en TCP (`eco_tcp.py` en 9000 y `cliente_tcp.py`).
* `6.PNG`: Eco en UDP (`eco_udp.py` en 9001 y `cliente_udp.py`).
* `7.PNG`: Las dos versiones cara a cara (tabla comparativa completa).
* `8.PNG`: Aprieta el lápiz: Seis retos sobre lo aprendido.
* `9.PNG`: Soluciones de los retos 1 al 3.
* `10.PNG`: Soluciones de los retos 4 al 6.
* `11.PNG`: Sé el socket: Consolida lo aprendido (el ciclo mental).
* `12.PNG`: ¿Quién soy? Adivina el concepto (10 preguntas rápidas).
* `13.PNG`: Entrevista de trabajo: Las seis preguntas que te harán.
* `14.PNG`: Resumen del Bloque 02 y siguiente parada: UD 06 (Servidores concurrentes).

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
cd /home/carla3/ANTIGRAVITY/socketsTCPyUDP/7_TCPoUDP

# 1. Criterio de decisión y casos reales
python3 01_criterio_de_decision_tcp_vs_udp.py

# 2. Práctica eco TCP vs UDP cara a cara
python3 02_practica_eco_cara_a_cara.py

# 3. Los 6 retos prácticos resueltos
python3 03_los_seis_retos_practicos.py

# 4. Sé el socket y juego de adivinanzas
python3 04_se_el_socket_y_quien_soy.py

# 5. Simulador de entrevista técnica
python3 05_simulador_entrevista_tecnica.py

# 6. Ejemplo de la vida real (Arquitectura híbrida Discord: Chat TCP + Voz UDP)
python3 06_ejemplo_vida_real.py
```

