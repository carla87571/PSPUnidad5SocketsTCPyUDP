# 🚀 Unidad 4: Three-Way Handshake, Cierre y Manejo de Errores en TCP

Bienvenido a la unidad práctica sobre el **Ciclo de Vida TCP, Handshake de 3 vías, Despedida de 4 vías, TIME_WAIT y Gestión de Errores y Excepciones** en Python.

---

## 📂 Contenido del Módulo

| Archivo | Diapositiva relacionada | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_three_way_handshake.py`](./01_three_way_handshake.py) | **Diapositiva 1** | El saludo de 3 vías (`SYN` ➔ `SYN+ACK` ➔ `ACK`), sincronización de números de secuencia y ejecución en `connect()`. |
| [`02_cierre_cuatro_vias_y_time_wait.py`](./02_cierre_cuatro_vias_y_time_wait.py) | **Diapositivas 2 y 3** | Cierre de 4 vías (`FIN`/`ACK`), el estado `TIME_WAIT` (protección de paquetes rezagados) y el error `Address already in use`. |
| [`03_solucion_so_reuseaddr.py`](./03_solucion_so_reuseaddr.py) | **Diapositiva 4** | La solución `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` para reiniciar servidores inmediatamente sin esperar. |
| [`04_gestion_de_errores_y_reintentos.py`](./04_gestion_de_errores_y_reintentos.py) | **Diapositivas 5 y 6** | Función `conectar_seguro()`, mapa de excepciones (`ConnectionRefused`, `timeout`, `ConnectionReset`, `BrokenPipe`, `OSError`). |
| [`05_control_de_espera_nonblocking_y_select.py`](./05_control_de_espera_nonblocking_y_select.py) | **Diapositiva 7** | Tres formas de controlar esperas: `settimeout()`, `setblocking(False)` con `BlockingIOError`, y multiplexación con `select.select()`. |
| [`06_mini_chequeo.py`](./06_mini_chequeo.py) | **Diapositiva 8** | Autoevaluación con "Las cuatro de la entrevista" técnica. |
| [`07_ejemplo_vida_real.py`](./07_ejemplo_vida_real.py) | *Aplicación práctica* | Arquitectura cliente-servidor tolerante a fallos con reintentos progresivos, recuperación ante reinicios y acuse de recibo. |

---

## 🖼 Diapositivas

Todas las diapositivas originales del bloque se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: Three-way handshake: El saludo que abre toda conexión TCP (SYN, SYN+ACK, ACK).
* `2.PNG`: El cierre de la conexión: La despedida: FIN y ACK.
* `3.PNG`: TIME_WAIT y «Address already in use»: El puerto que queda retenido.
* `4.PNG`: SO_REUSEADDR: Reinicia tu servidor sin esperar.
* `5.PNG`: Las redes fallan: try/except y timeouts como red de seguridad (`conectar_seguro`).
* `6.PNG`: El mapa de excepciones: cada error con su tratamiento adecuado.
* `7.PNG`: Non-blocking y select: Tres formas de controlar la espera.
* `8.PNG`: Mini-chequeo: ciclo de vida y errores (las cuatro de la entrevista).
* `9.PNG`: Resumen del bloque 01 (Socket, Cliente, Servidor, Ciclo y Errores).

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
cd /home/carla3/ANTIGRAVITY/socketsTCPyUDP/4_ThreeWayHandshake

# 1. El saludo de tres vías (Handshake)
python3 01_three_way_handshake.py

# 2. Cierre de 4 vías y el estado TIME_WAIT
python3 02_cierre_cuatro_vias_y_time_wait.py

# 3. La solución indispensable: SO_REUSEADDR
python3 03_solucion_so_reuseaddr.py

# 4. Mapa de excepciones y reintentos seguros
python3 04_gestion_de_errores_y_reintentos.py

# 5. Non-blocking y multiplexación con select()
python3 05_control_de_espera_nonblocking_y_select.py

# 6. Mini-chequeo interactivo (Las 4 de la entrevista)
python3 06_mini_chequeo.py

# 7. Ejemplo de la vida real (Arquitectura resiliente)
python3 07_ejemplo_vida_real.py
```

