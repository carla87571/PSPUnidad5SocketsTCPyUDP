# 🚀 Unidad 3: Servidor TCP en Python

Bienvenido a la unidad práctica sobre el **Servidor TCP** en Python. Esta carpeta contiene los scripts numerados, explicaciones pedagógicas de las diapositivas y un ejemplo de arquitectura real de administración de sistemas.

---

## 📂 Contenido del Módulo

| Archivo | Diapositiva relacionada | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_el_rol_del_servidor_y_ciclo_de_vida.py`](./01_el_rol_del_servidor_y_ciclo_de_vida.py) | **Diapositivas 1 y 2** | El servidor como receptor pasivo ("descolgó primero"), los 6 pasos obligatorios en orden (`socket`, `bind`, `listen`, `accept`, `recv`/`sendall`, `close`). |
| [`02_servidor_tcp_minimo.py`](./02_servidor_tcp_minimo.py) | **Diapositiva 3** | Implementación del servidor mínimo con bloques `with` anidados (`with servidor` y `with conexion`). |
| [`03_los_dos_sockets_servidor_vs_conexion.py`](./03_los_dos_sockets_servidor_vs_conexion.py) | **Diapositiva 4** | El socket maestro (`servidor`) vs el socket de llamada privada (`conexion`). Por qué no se puede hacer `servidor.recv()`. |
| [`04_el_bucle_de_atencion.py`](./04_el_bucle_de_atencion.py) | **Diapositiva 5** | Patrón `while True` para atender múltiples clientes, la cola de espera de `listen()` y la limitación secuencial. |
| [`05_pool_puzzle_ordenando_el_servidor.py`](./05_pool_puzzle_ordenando_el_servidor.py) | **Diapositiva 6** | Resolución del puzzle `d ➔ a ➔ f ➔ b ➔ c ➔ g ➔ h ➔ e` y demostración de errores típicos (`OSError` con `listen()` antes de `bind()`). |
| [`06_mini_chequeo.py`](./06_mini_chequeo.py) | **Diapositiva 7** | Autoevaluación interactiva con las 3 preguntas conceptuales de la diapositiva. |
| [`07_ejemplo_vida_real.py`](./07_ejemplo_vida_real.py) | *Aplicación práctica* | Demonio de diagnóstico y métricas del sistema (DevOps Health Agent) con comandos `PING`, `METRICAS` y `AYUDA`. |

---

## 🖼 Diapositivas

Todas las diapositivas originales del bloque se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: Servidor TCP: La idea en una frase ("descolgó primero").
* `2.PNG`: Ciclo de vida del servidor: seis pasos: descolgar y atender.
* `3.PNG`: El servidor TCP mínimo resuelto con `with`.
* `4.PNG`: Cada método del servidor al detalle y el concepto de `conexion` vs `servidor`.
* `5.PNG`: El bucle de atención (`while True`) y la cola de espera.
* `6.PNG`: Pool puzzle: ordena el servidor y errores típicos.
* `7.PNG`: Mini-chequeo conceptual del servidor TCP.

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
cd /home/carla3/ANTIGRAVITY/socketsTCPyUDP/3_ServidorTCP

# 1. El rol del servidor y su ciclo de vida
python3 01_el_rol_del_servidor_y_ciclo_de_vida.py

# 2. Servidor TCP mínimo
python3 02_servidor_tcp_minimo.py

# 3. Diferencia entre 'servidor' y 'conexion'
python3 03_los_dos_sockets_servidor_vs_conexion.py

# 4. Bucle de atención secuencial
python3 04_el_bucle_de_atencion.py

# 5. Pool puzzle y errores típicos
python3 05_pool_puzzle_ordenando_el_servidor.py

# 6. Mini-chequeo interactivo
python3 06_mini_chequeo.py

# 7. Ejemplo de la vida real (Daemon de métricas DevOps)
python3 07_ejemplo_vida_real.py
```

