# 🚀 Unidad 1: Fundamentos de Sockets en Python

Bienvenido a la unidad práctica de introducción a **Sockets** en Python. Esta carpeta contiene los ejemplos de código organizados progresivamente para aprender los conceptos clave presentados en las diapositivas.

---

## 📂 Contenido del Módulo

| Archivo | Diapositiva relacionada | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_que_es_un_socket.py`](./01_que_es_un_socket.py) | **Diapositiva 2** | Definición de socket, analogía del teléfono, objeto socket en Python. |
| [`02_ip_y_puerto.py`](./02_ip_y_puerto.py) | **Diapositiva 3** | El quién (IP) y el dónde (Puerto), localhost (127.0.0.1), rangos de puertos, tupla endpoint `(IP, puerto)`. |
| [`03_creacion_sockets_tcp_vs_udp.py`](./03_creacion_sockets_tcp_vs_udp.py) | **Diapositiva 4** | Parámetros `AF_INET`, `SOCK_STREAM` (TCP), `SOCK_DGRAM` (UDP), regla mnemotécnica, uso de `with`. |
| [`04_tcp_vs_udp_comparacion.py`](./04_tcp_vs_udp_comparacion.py) | **Diapositivas 5 y 6** | Analogía de Carta Certificada vs Avión de Papel, tabla comparativa, fiabilidad vs velocidad. |
| [`05_mini_chequeo.py`](./05_mini_chequeo.py) | **Diapositiva 7** | Mini autoevaluación interactiva con las 4 preguntas y respuestas de la diapositiva. |
| [`06_ejemplo_vida_real.py`](./06_ejemplo_vida_real.py) | *Aplicación práctica* | Sistema IoT de monitoreo climático / invernadero con arquitectura Cliente-Servidor TCP. |

---

## 🖼 Diapositivas

Todas las diapositivas originales se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: Temario y mapa del bloque.
* `2.PNG`: Qué es un socket y la analogía del teléfono.
* `3.PNG`: IP y puerto (el «quién» y el «dónde»).
* `4.PNG`: Creación de un socket en Python en una línea.
* `5.PNG`: La analogía: Carta certificada (TCP) vs Avión de papel (UDP).
* `6.PNG`: Tabla comparativa TCP vs UDP.
* `7.PNG`: Mini-chequeo conceptual con preguntas y respuestas.

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
# 1. Concepto básico y analogía
python3 01_que_es_un_socket.py

# 2. IP, puerto y tuplas
python3 02_ip_y_puerto.py

# 3. Creación de sockets TCP vs UDP
python3 03_creacion_sockets_tcp_vs_udp.py

# 4. Comparativa detallada y simulación
python3 04_tcp_vs_udp_comparacion.py

# 5. Autoevaluación interactiva
python3 05_mini_chequeo.py

# 6. Ejemplo de la vida real (Modo demo automático)
python3 06_ejemplo_vida_real.py
```

