# 📚 Unidad 05: Sockets TCP y UDP - Actividades No Evaluables 01 (CEEDCV / DAM)

Esta carpeta contiene la resolución completa, didáctica y comentada paso a paso de los **8 ejercicios prácticos y teóricos** correspondientes al documento oficial del ciclo formativo de Desarrollo de Aplicaciones Multiplataforma (DAM).

---

## 📂 Estructura de Archivos

| Archivo | Enunciado / Tema | Protocolo | Tipo |
| :--- | :--- | :---: | :---: |
| [ejercicio_01_servidor_saludo.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_01_servidor_saludo.py) | **Ejercicio 1**: Servidor TCP de saludo ("Bienvenido al servidor") | TCP | Servidor |
| [ejercicio_02_cliente_envia_recibe.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_02_cliente_envia_recibe.py) | **Ejercicio 2**: Cliente TCP que envía "Hola" y muestra respuesta | TCP | Cliente |
| [ejercicio_03_servidor_eco.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_03_servidor_eco.py) | **Ejercicio 3**: Servidor TCP eco (devuelve exactamente lo recibido) | TCP | Servidor |
| [ejercicio_04_ip_y_puerto.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_04_ip_y_puerto.py) | **Ejercicio 4**: Respuestas teóricas (IP vs Puerto, 127.0.0.1, constantes) | Ambos | Teoría |
| [ejercicio_05_cliente_udp_input.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_05_cliente_udp_input.py) | **Ejercicio 5**: Cliente UDP con entrada interactiva por `input()` | UDP | Cliente |
| [ejercicio_06_servidor_udp_eco_personalizado.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_06_servidor_udp_eco_personalizado.py) | **Ejercicio 6**: Servidor UDP con eco `"Recibido: <mensaje>"` | UDP | Servidor |
| [ejercicio_07_tcp_vs_udp_clasifica.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_07_tcp_vs_udp_clasifica.py) | **Ejercicio 7**: Clasificación de 6 apps y tabla comparativa de transporte | Ambos | Teoría |
| [ejercicio_08_cliente_http_manual.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/ejercicio_08_cliente_http_manual.py) | **Ejercicio 8**: Cliente HTTP manual mediante socket TCP a `example.com:80` | TCP (HTTP) | Cliente |
| [documentos/](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/8_Ejercicios1/documentos/) | PDF original de enunciados de la unidad | - | Documento |

---

## 🚀 Guía de Ejecución y Pruebas

Todos los ejercicios incluyen un **modo de demostración autónomo** para que puedas ejecutarlos directamente sin necesidad de abrir varias terminales, y al mismo tiempo admiten el **modo interactivo estándar** abriendo dos terminales.

### 🔹 Pareja 1: Ejercicio 1 (Servidor) y Ejercicio 2 (Cliente)
**Objetivo**: Probar la comunicación básica orientada a conexión en TCP.
- **Terminal 1 (Servidor)**:
  ```bash
  python3 ejercicio_01_servidor_saludo.py
  ```
- **Terminal 2 (Cliente)**:
  ```bash
  python3 ejercicio_02_cliente_envia_recibe.py
  ```
*O prueba rápida autónoma:*
```bash
python3 ejercicio_01_servidor_saludo.py --demo
python3 ejercicio_02_cliente_envia_recibe.py --demo
```

---

### 🔹 Ejercicio 3: Servidor TCP Eco
**Objetivo**: Verificar que el servidor recibe una secuencia de bytes y la retransmite íntegra y sin alteraciones.
- **Terminal 1**:
  ```bash
  python3 ejercicio_03_servidor_eco.py
  ```
- **Terminal 2**:
  ```bash
  python3 ejercicio_02_cliente_envia_recibe.py
  # O mediante netcat:
  nc 127.0.0.1 9000
  ```
*O prueba autónoma:*
```bash
python3 ejercicio_03_servidor_eco.py --demo
```

---

### 🔹 Ejercicio 4: Teoría de IP y Puerto
**Objetivo**: Inspeccionar la resolución teórica y los valores nativos de las constantes en Python (`SOCK_STREAM`, `SOCK_DGRAM`, `AF_INET`).
```bash
python3 ejercicio_04_ip_y_puerto.py
```

---

### 🔹 Pareja 2: Ejercicio 5 (Cliente UDP) y Ejercicio 6 (Servidor UDP)
**Objetivo**: Demostrar el funcionamiento de datagramas sin conexión usando `sendto()` y `recvfrom()`.
- **Terminal 1 (Servidor UDP)**:
  ```bash
  python3 ejercicio_06_servidor_udp_eco_personalizado.py
  ```
- **Terminal 2 (Cliente UDP)**:
  ```bash
  python3 ejercicio_05_cliente_udp_input.py
  ```
*O prueba rápida autónoma:*
```bash
python3 ejercicio_05_cliente_udp_input.py --demo
python3 ejercicio_06_servidor_udp_eco_personalizado.py --demo
```

---

### 🔹 Ejercicio 7: TCP vs UDP (Clasificación y Tabla)
**Objetivo**: Comparar las características técnicas (conexión, garantía, orden, velocidad) y justificar la elección de protocolo para Web, Zoom, Correo, Fortnite, FTP y DNS.
```bash
python3 ejercicio_07_tcp_vs_udp_clasifica.py
```

---

### 🔹 Ejercicio 8: Cliente HTTP Manual
**Objetivo**: Comprender que HTTP/1.1 viaja sobre un socket TCP estándar. Envía una petición `GET / HTTP/1.1` con cabeceras `Host` y `Connection: close`, acumulando la respuesta con `recv(4096)` hasta recibir `b""` e imprimiendo los primeros 500 caracteres.
```bash
python3 ejercicio_08_cliente_http_manual.py
```
*(Nota didáctica: Cuenta con detección de entorno; si la máquina no dispone de conexión a internet o DNS externo, levanta automáticamente un servidor HTTP mock para que la práctica funcione al 100% de manera garantizada).*

---

## 🧠 Resumen Conceptual Rápido

```
                 ┌────────────────────────────────────────────────────────┐
                 │                CAPA DE APLICACIÓN                      │
                 │   HTTP (80), HTTPS (443), SMTP (25), DNS (53), etc.    │
                 └───────────────────────┬────────────────────────────────┘
                                         │
                 ┌───────────────────────┴────────────────────────────────┐
                 │                CAPA DE TRANSPORTE                      │
                 ├──────────────────────────┬─────────────────────────────┤
                 │           TCP            │             UDP             │
                 ├──────────────────────────┼─────────────────────────────┤
                 │ socket.SOCK_STREAM       │ socket.SOCK_DGRAM           │
                 │ Orientado a conexión     │ Sin conexión                │
                 │ connect() / listen()     │ sendto() / recvfrom()       │
                 │ Entrega garantizada      │ Best-effort (sin garantías) │
                 │ Flujo continuo ordenado  │ Datagramas independientes   │
                 └──────────────────────────┴─────────────────────────────┘
```

