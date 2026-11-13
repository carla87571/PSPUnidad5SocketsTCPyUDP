# 🚀 Unidad 2: Cliente TCP en Python

Bienvenido a la unidad práctica sobre el **Cliente TCP** en Python. Esta carpeta contiene los ejemplos didácticos numerados y orientados a comprender a fondo el funcionamiento, métodos y consideraciones clave al programar un cliente de red TCP.

---

## 📂 Contenido del Módulo

| Archivo | Diapositiva relacionada | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_el_rol_del_cliente.py`](./01_el_rol_del_cliente.py) | **Diapositiva 1** | El cliente como iniciador activo de la conexión. Captura didáctica de `ConnectionRefusedError`. |
| [`02_ciclo_de_vida_y_cliente_minimo.py`](./02_ciclo_de_vida_y_cliente_minimo.py) | **Diapositivas 2 y 3** | Los 4 pasos en orden estricto (`socket`, `connect`, `sendall`/`recv`, `close`), uso de bytes `b"..."` y el cliente TCP mínimo. |
| [`03_metodos_al_detalle.py`](./03_metodos_al_detalle.py) | **Diapositiva 4** | `sendall()` vs `send()`, el buffer de `recv(1024)` y cómo recibir mensajes largos por fragmentos. |
| [`04_el_bloqueo_y_timeouts.py`](./04_el_bloqueo_y_timeouts.py) | **Diapositiva 5** | Comportamiento bloqueante de `recv()`, peligro de congelamiento y la salida de emergencia con `settimeout()`. |
| [`05_mini_chequeo.py`](./05_mini_chequeo.py) | **Diapositiva 6** | Autoevaluación con las 3 preguntas clave de la diapositiva de chequeo. |
| [`06_ejemplo_vida_real.py`](./06_ejemplo_vida_real.py) | *Aplicación práctica* | Terminal Punto de Venta (POS) y Pasarela Bancaria con serialización JSON, timeouts y control de errores. |

---

## 🖼 Diapositivas

Todas las diapositivas originales del bloque se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: Cliente TCP: La idea en una frase y analogía del teléfono.
* `2.PNG`: El ciclo de vida del cliente: cuatro pasos siempre en orden.
* `3.PNG`: El cliente TCP mínimo: código resuelto de arriba a abajo.
* `4.PNG`: Cada método al detalle y advertencias importantes.
* `5.PNG`: Be the code: el cliente paso a paso y la alerta del bloqueo en `recv()`.
* `6.PNG`: Mini-chequeo conceptual con preguntas y respuestas.

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
cd /home/carla3/ANTIGRAVITY/socketsTCPyUDP/2_ClienteTCP

# 1. El rol activo del cliente y captura de ConnectionRefusedError
python3 01_el_rol_del_cliente.py

# 2. El cliente TCP mínimo y su ciclo de vida
python3 02_ciclo_de_vida_y_cliente_minimo.py

# 3. Métodos en detalle: sendall vs send y recepción en fragmentos
python3 03_metodos_al_detalle.py

# 4. Comportamiento bloqueante y timeouts de emergencia
python3 04_el_bloqueo_y_timeouts.py

# 5. Mini-chequeo interactivo
python3 05_mini_chequeo.py

# 6. Ejemplo de la vida real (Terminal de pagos POS)
python3 06_ejemplo_vida_real.py
```

