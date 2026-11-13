# 🚀 Unidad 5: Cliente y Servidor UDP en Python

Bienvenido a la unidad práctica sobre el **Protocolo UDP (User Datagram Protocol)** en Python. Esta carpeta contiene los ejemplos didácticos numerados y orientados a comprender las diferencias clave frente a TCP, el uso de datagramas independientes, sus ventajas y limitaciones.

---

## 📂 Contenido del Módulo

| Archivo | Diapositiva relacionada | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_la_filosofia_udp.py`](./01_la_filosofia_udp.py) | **Diapositivas 1 y 3** | Filosofía de los aviones de papel: sin `connect()`, sin `listen()`, sin `accept()`. El peligro del silencio y `settimeout()`. |
| [`02_el_cliente_udp.py`](./02_el_cliente_udp.py) | **Diapositiva 2** | Implementación del cliente UDP mínimo con `sendto(datos, (HOST, PORT))` y `recvfrom(1024)`. |
| [`03_el_servidor_udp.py`](./03_el_servidor_udp.py) | **Diapositivas 4, 5 y 6** | Servidor UDP con `bind()` y `recvfrom()`. Cómo devolver la pelota a la dirección recibida y atención a múltiples clientes en un solo socket. |
| [`04_los_males_de_udp_y_limite_tamano.py`](./04_los_males_de_udp_y_limite_tamano.py) | **Diapositiva 7** | Los 4 males de UDP (pérdida, desorden, duplicados, límite de carga útil de 65.507 bytes) y captura de `OSError: Message too long`. |
| [`05_mini_chequeo.py`](./05_mini_chequeo.py) | **Diapositiva 8** | Autoevaluación guiada con las 4 preguntas esenciales de UDP. |
| [`06_ejemplo_vida_real.py`](./06_ejemplo_vida_real.py) | *Aplicación práctica* | Servidor de videojuegos multijugador online con sincronización de coordenadas a alta velocidad y snapshots de mundo. |

---

## 🖼 Diapositivas

Todas las diapositivas originales del bloque se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: Cliente y servidor UDP: La idea en una frase (sin connect, sin accept, sin listen).
* `2.PNG`: El cliente UDP: `sendto()` y `recvfrom()`.
* `3.PNG`: Sendto contra send: La diferencia visual con TCP.
* `4.PNG`: El servidor UDP: `bind()` y `recvfrom()` (nada más).
* `5.PNG` y `6.PNG`: Sin accept(), sin listen(): Servidor TCP contra servidor UDP.
* `7.PNG`: Datagramas: cada envío es un mundo aparte (`cinco_aviones.py` y los 4 males).
* `8.PNG`: Mini-chequeo conceptual de UDP.

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
cd /home/carla3/ANTIGRAVITY/socketsTCPyUDP/5_ClienteyServidorUDP

# 1. Filosofía de UDP y ausencia de conexión
python3 01_la_filosofia_udp.py

# 2. Cliente UDP mínimo
python3 02_el_cliente_udp.py

# 3. Servidor UDP y devolución de paquetes
python3 03_el_servidor_udp.py

# 4. Los males de UDP y el límite de 65.507 bytes
python3 04_los_males_de_udp_y_limite_tamano.py

# 5. Mini-chequeo interactivo
python3 05_mini_chequeo.py

# 6. Ejemplo de la vida real (Servidor de videojuegos multijugador)
python3 06_ejemplo_vida_real.py
```

