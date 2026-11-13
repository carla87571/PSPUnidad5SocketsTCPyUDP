# 📚 Unidad 05: Sockets TCP y UDP - Actividades No Evaluables 02 (CEEDCV / DAM)
### 📝 Boletín UD05 — Avanzado (Profesor: Sergi García Barea)

Esta carpeta contiene la resolución completa, didáctica y verificada de los **12 ejercicios avanzados** sobre sockets TCP y UDP en Python (clientes interactivos, multiplexación I/O con `select()`, timeouts, protocolo NTP manual, benchmarks de rendimiento, interfaces `0.0.0.0` y servidores web HTTP artesanales).

---

## 📂 Índice de Archivos y Ejercicios

| Archivo | Enunciado / Tema | Protocolo | Tipo |
| :--- | :--- | :---: | :---: |
| [ejercicio_01_servidor_cuenta_caracteres.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_01_servidor_cuenta_caracteres.py) | **Ejercicio 1**: Servidor que cuenta caracteres (`"hola"` → `"4"`) | TCP | Servidor |
| [ejercicio_02_cliente_interactivo.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_02_cliente_interactivo.py) | **Ejercicio 2**: Cliente interactivo con bucle `while True` hasta `"salir"` | TCP | Cliente |
| [ejercicio_03_servidor_mayusculas.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_03_servidor_mayusculas.py) | **Ejercicio 3**: Servidor que transforma texto a MAYÚSCULAS con `.upper()` | TCP | Servidor |
| [ejercicio_04_cliente_con_reconexion.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_04_cliente_con_reconexion.py) | **Ejercicio 4**: Cliente resiliente con reconexión (hasta 3 intentos con 2s) | TCP | Cliente |
| [ejercicio_05_servidor_select_sin_hilos.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_05_servidor_select_sin_hilos.py) | **Ejercicio 5**: Concurrencia mono-hilo con `select.select()` y `setblocking(False)` | TCP | Servidor |
| [ejercicio_06_servidor_timeout_personalizado.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_06_servidor_timeout_personalizado.py) | **Ejercicio 6**: Servidor con timeout de 10 segundos ante inactividad | TCP | Servidor |
| [ejercicio_07_cliente_ntp_manual.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_07_cliente_ntp_manual.py) | **Ejercicio 7**: Cliente NTP manual sobre UDP en puerto 123 y `struct.unpack('!I')` | UDP (NTP) | Cliente |
| [ejercicio_08_servidor_udp_multimensaje.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_08_servidor_udp_multimensaje.py) | **Ejercicio 8**: Servidor UDP multimensaje con `range(1, 4)` y `"OK #1"`, `"OK #2"`, `"OK #3"` | UDP | Servidor |
| [ejercicio_09_ping_udp.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_09_ping_udp.py) | **Ejercicio 9**: Ping UDP ("PING" → "PONG") con medición de latencia RTT | UDP | Ambos |
| [ejercicio_10_servidor_todas_las_interfaces.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_10_servidor_todas_las_interfaces.py) | **Ejercicio 10**: Servidor escuchando en todas las interfaces (`0.0.0.0`) | UDP | Servidor |
| [ejercicio_11_compara_tcp_y_udp.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_11_compara_tcp_y_udp.py) | **Ejercicio 11**: Benchmark de 10 intercambios TCP vs UDP con `time.time()` | Ambos | Benchmark |
| [ejercicio_12_mini_servidor_web.py](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/ejercicio_12_mini_servidor_web.py) | **Ejercicio 12**: Mini servidor web artesanal en `127.0.0.1:8080` con `HTTP/1.1 200 OK` | TCP (HTTP) | Servidor |
| [documentos/](file:///home/carla3/ANTIGRAVITY/socketsTCPyUDP/9_Ejercicios2/documentos/) | Documento PDF original de actividades avanzadas | - | PDF |

---

## 🛠️ Guía de Ejecución Rápida

Todos los ejercicios pueden probarse de dos maneras:
1. **Modo Automático (`--demo`)**: Lanza la prueba completa autónomamente en una sola orden.
2. **Modo Interactivo**: Abriendo dos terminales (una para el servidor y otra para el cliente).

### Ejercicios 1, 2 y 3 (Servidores de transformación y Cliente interactivo)
```bash
# Terminal 1: Iniciar servidor de conteo o de mayúsculas
python3 9_Ejercicios2/ejercicio_01_servidor_cuenta_caracteres.py
# (o: python3 9_Ejercicios2/ejercicio_03_servidor_mayusculas.py)

# Terminal 2: Conectar con el cliente interactivo
python3 9_Ejercicios2/ejercicio_02_cliente_interactivo.py
```

### Ejercicio 4: Cliente con reconexión
```bash
# Simula caída del servidor y reconexión automática tras 2 reintentos:
python3 9_Ejercicios2/ejercicio_04_cliente_con_reconexion.py --demo
```

### Ejercicio 5: Multiplexación I/O con `select.select()`
```bash
# Lanza 3 clientes simultáneos atendidos por un solo hilo de ejecución:
python3 9_Ejercicios2/ejercicio_05_servidor_select_sin_hilos.py --demo
```

### Ejercicio 6: Timeout por inactividad
```bash
# Demuestra el corte y mensaje de despedida ante clientes que no envían datos:
python3 9_Ejercicios2/ejercicio_06_servidor_timeout_personalizado.py --demo
```

### Ejercicio 7: Cliente NTP Manual
```bash
# Consulta la hora atómica oficial desempaquetando la cabecera binaria NTP:
python3 9_Ejercicios2/ejercicio_07_cliente_ntp_manual.py
```

### Ejercicio 8: Servidor UDP multimensaje
```bash
# Responde a 3 datagramas con "OK #1", "OK #2", "OK #3" y se cierra con with:
python3 9_Ejercicios2/ejercicio_08_servidor_udp_multimensaje.py --demo
```

### Ejercicio 9: Ping UDP y latencia RTT
```bash
# Mide en milisegundos y microsegundos el tiempo de ida y vuelta:
python3 9_Ejercicios2/ejercicio_09_ping_udp.py
```

### Ejercicio 10: Servidor en todas las interfaces (`0.0.0.0`)
```bash
# Escucha peticiones desde localhost y cualquier interfaz de red física/virtual:
python3 9_Ejercicios2/ejercicio_10_servidor_todas_las_interfaces.py --demo
```

### Ejercicio 11: Benchmark TCP vs UDP
```bash
# Compara el coste del handshake TCP frente a la inmediatez de datagramas UDP:
python3 9_Ejercicios2/ejercicio_11_compara_tcp_y_udp.py
```

### Ejercicio 12: Mini Servidor Web HTTP
```bash
# Iniciar servidor web artesanal:
python3 9_Ejercicios2/ejercicio_12_mini_servidor_web.py
# Luego abre en tu navegador: http://127.0.0.1:8080
```
*(O prueba automática en terminal: `python3 9_Ejercicios2/ejercicio_12_mini_servidor_web.py --demo`)*

