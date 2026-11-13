# 🚀 Unidad 6: Protocolo HTTP, Network Byte Order y NTP en Python

Bienvenido a la unidad práctica sobre **Protocolos de Aplicación (Capa 7)**: cómo viajar con texto sobre TCP con **HTTP**, cómo transmitir números binarios con **Network Byte Order (`struct`)**, y cómo sincronizar la hora mundial con **NTP** sobre UDP.

---

## 📂 Contenido del Módulo

| Archivo | Diapositiva relacionada | Conceptos Clave |
| :--- | :--- | :--- |
| [`01_anatomia_http_y_verbos.py`](./01_anatomia_http_y_verbos.py) | **Diapositivas 1 y 2** | HTTP como texto sobre TCP, estructura de petición GET, cabecera `Host:`, línea en blanco `\r\n\r\n`, verbos (GET, POST, PUT, DELETE) y respuestas 200/404/500 con `Content-Length`. |
| [`02_cliente_http_manual_con_sockets.py`](./02_cliente_http_manual_con_sockets.py) | **Diapositiva 3** | Cliente HTTP manual con sockets TCP, forzado de cierre con `Connection: close` y lectura acumulativa en fragmentos hasta recibir `b''`. |
| [`03_network_byte_order_y_struct.py`](./03_network_byte_order_y_struct.py) | **Diapositiva 4** | El orden de bytes Big-Endian en redes, módulo `struct`, prefijo `!`, formato `!I` (entero 4 bytes) y `!H` (entero 2 bytes). |
| [`04_cliente_ntp_hora_internet.py`](./04_cliente_ntp_hora_internet.py) | **Diapositivas 5 y 6** | Protocolo NTP en UDP puerto 123, paquete binario de 48 bytes (`b"\x1b"`), extracción con `!I` en bytes 40:44 y conversión de época 1900 a 1970 (-2.208.988.800s). |
| [`05_mini_chequeo.py`](./05_mini_chequeo.py) | **Diapositiva 7** | Autoevaluación interactiva con las 3 preguntas clave del chequeo (HTTP, struct y NTP). |
| [`06_ejemplo_vida_real.py`](./06_ejemplo_vida_real.py) | *Aplicación práctica* | Servidor Web HTTP y Micro-API REST completo construido 100% con sockets TCP puros (soporta HTML, JSON y 404). |

---

## 🖼 Diapositivas

Todas las diapositivas originales del bloque se encuentran archivadas en la carpeta:
👉 [`diapositivas/`](./diapositivas/)

* `1.PNG`: HTTP: el protocolo que mueve la web (petición GET, cabecera Host, línea en blanco).
* `2.PNG`: Verbos (GET, POST, PUT, DELETE) y estructura de respuesta HTTP con `Content-Length`.
* `3.PNG`: El cliente HTTP manual (`http_manual.py`, `Connection: close` y fragmentos).
* `4.PNG`: El orden de los bytes: network byte order (big-endian) y el prefijo `!` de `struct`.
* `5.PNG`: NTP: sincronizar relojes con UDP (puerto 123, servidores de tiempo).
* `6.PNG`: Cómo funciona el cliente NTP: los tres detalles que importan (`0x1b`, `settimeout`, `!I`).
* `7.PNG`: Mini-chequeo conceptual: HTTP, bytes y NTP.

---

## 🛠 Cómo ejecutar los scripts

Puedes ejecutar cada archivo individualmente desde tu terminal:

```bash
cd /home/carla3/ANTIGRAVITY/socketsTCPyUDP/6_ProtocoloHTTP

# 1. Anatomía y verbos HTTP
python3 01_anatomia_http_y_verbos.py

# 2. Cliente HTTP manual puro
python3 02_cliente_http_manual_con_sockets.py

# 3. Network Byte Order y struct
python3 03_network_byte_order_y_struct.py

# 4. Cliente NTP y sincronización horaria
python3 04_cliente_ntp_hora_internet.py

# 5. Mini-chequeo interactivo
python3 05_mini_chequeo.py

# 6. Ejemplo de la vida real (Servidor Web HTTP / API REST)
python3 06_ejemplo_vida_real.py
```

