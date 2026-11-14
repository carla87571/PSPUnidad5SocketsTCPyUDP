# 🌐 Programación de Servicios y Procesos (PSP)
## Unidad 05: Sockets TCP y UDP en Python
**Ciclo Formativo de Grado Superior en Desarrollo de Aplicaciones Multiplataforma (CFGS DAM)**  
**Centro:** CEEDCV | **Profesor:** Sergi García Barea

---

## 📖 Descripción del Repositorio

Este repositorio contiene una suite completa, pedagógica y práctica sobre **comunicaciones en red mediante sockets en Python 3**, cubriendo tanto la teoría esencial como implementaciones reales de clientes y servidores bajo los protocolos de la capa de transporte **TCP (Transmission Control Protocol)** y **UDP (User Datagram Protocol)**, así como la capa de aplicación (**HTTP/1.1** y **NTP**).

Cada carpeta incluye:
- Scripts `.py` numerados, comentados paso a paso con analogías y conceptos clave.
- Ejemplos prácticos y de la vida real.
- Modos de autoverificación y demostración (`--demo`).
- Documentación detallada (`README.md`) y material de referencia/diapositivas.

---

## 🗺️ Mapa de Contenidos

```
socketsTCPyUDP/
├── 1_sockets/             # Fundamentos: Sockets, IPs, Puertos y Familias
├── 2_ClienteTCP/          # Clientes TCP: connect(), sendall(), recv(), close()
├── 3_ServidorTCP/         # Servidores TCP: bind(), listen(), accept(), concurrencia
├── 4_ThreeWayHandshake/   # Negociación en 3 vías (SYN, SYN-ACK, ACK) y estados
├── 5_ClienteyServidorUDP/ # Datagramas UDP: sendto(), recvfrom(), sin conexión
├── 6_ProtocoloHTTP/       # Protocolo HTTP/1.1 manual sobre sockets TCP
├── 7_TCPoUDP/             # Análisis comparativo, criterios y simulador de decisión
├── 8_Ejercicios1/         # Actividades No Evaluables 01 (8 ejercicios resueltos)
└── 9_Ejercicios2/         # Actividades No Evaluables 02 (12 ejercicios avanzados)
```

---

## 📚 Detalle de Módulos

### 1️⃣ [1_sockets/](1_sockets/) — Fundamentos de Sockets en Red
- **01_que_es_un_socket_conceptos_clave.py**: Definición formal y analogía del enchufe/teléfono.
- **02_la_ip_y_el_puerto_quien_es_quien.py**: Dirección IP (Capa 3 - Máquina) vs Puerto (Capa 4 - Proceso).
- **03_familias_y_tipos_de_socket.py**: `AF_INET`, `AF_INET6`, `SOCK_STREAM` (TCP) y `SOCK_DGRAM` (UDP).
- **04_ciclo_de_vida_socket.py**: Estados de un socket desde su creación hasta su cierre.
- **05_mini_chequeo.py**: Cuestionario interactivo con autoevaluación.
- **06_ejemplo_vida_real.py**: Monitor de conectividad y escáner de puertos local.

### 2️⃣ [2_ClienteTCP/](2_ClienteTCP/) — Arquitectura y Desarrollo de Clientes TCP
- **01_anatomia_del_cliente_tcp.py**: Los 5 pasos obligatorios de un cliente TCP.
- **02_conectar_con_el_servidor.py**: Uso de `connect()` y captura de `ConnectionRefusedError`.
- **03_enviar_datos_por_la_red.py**: Codificación de bytes con `.encode('utf-8')` y `sendall()`.
- **04_recibir_y_decodificar.py**: Recepción por bloques con `recv(1024)` y `.decode('utf-8')`.
- **05_cerrar_la_conexion_limpiamente.py**: Liberación de descriptores y uso del gestor `with`.
- **06_ejemplo_vida_real.py**: Cliente interactivo de mensajería con servidor en segundo plano.

### 3️⃣ [3_ServidorTCP/](3_ServidorTCP/) — Arquitectura y Desarrollo de Servidores TCP
- **01_anatomia_del_servidor_tcp.py**: Flujo maestro: `socket` → `bind` → `listen` → `accept`.
- **02_el_metodo_bind.py**: Vinculación de interfaz y puerto (`SO_REUSEADDR`).
- **03_el_metodo_listen_y_la_cola.py**: Puesta en escucha y gestión de la cola de espera (*backlog*).
- **04_el_metodo_accept_y_el_nuevo_socket.py**: Separación crucial entre socket de bienvenida y socket de datos.
- **05_pool_puzzle_ordenando_el_servidor.py**: Reto didáctico de ensamblado de código.
- **06_servidor_concurrente_multihilo.py**: Concurrencia real con `threading.Thread` para atender múltiples clientes.
- **07_ejemplo_vida_real.py**: Servidor de cotizaciones financieras y comandos en tiempo real.

### 4️⃣ [4_ThreeWayHandshake/](4_ThreeWayHandshake/) — Negociación en Tres Vías TCP
- **01_el_acuerdo_de_tres_pasos.py**: Demostración y paquete a paquete: SYN → SYN-ACK → ACK.
- **02_las_tres_banderas_syn_ack_fin.py**: Banderas (*flags*) de la cabecera TCP y sus funciones.
- **03_los_numeros_de_secuencia_y_acuse.py**: ISN, numeración de bytes y acuses de recibo.
- **04_estados_de_la_conexion_tcp.py**: Máquina de estados: `LISTEN`, `SYN_SENT`, `ESTABLISHED`, `TIME_WAIT`, `CLOSED`.
- **05_wireshark_detective_de_red.py**: Simulación forense de captura de paquetes en formato Wireshark.
- **06_el_cierre_de_conexion_four_way_handshake.py**: Desconexión ordenada en 4 pasos (FIN, ACK, FIN, ACK).
- **07_ejemplo_vida_real.py**: Simulador de handshake con inyección de paquetes, pérdidas y retransmisiones.

### 5️⃣ [5_ClienteyServidorUDP/](5_ClienteyServidorUDP/) — Protocolo de Datagramas UDP
- **01_filosofia_udp_el_servicio_postal.py**: UDP como servicio sin conexión (*best-effort*).
- **02_cliente_udp_sendto.py**: Envío de datagramas con `sendto(bytes, (ip, puerto))` sin `connect()`.
- **03_servidor_udp_recvfrom.py**: Recepción directa con `recvfrom()` sin `listen()` ni `accept()`.
- **04_cliente_servidor_udp_conversacion.py**: Diálogo bidireccional cliente-servidor en UDP.
- **05_mini_chequeo_udp.py**: Test interactivo sobre diferencias fundamentales entre TCP y UDP.
- **06_ejemplo_vida_real.py**: Sistema de telemetría de sensores IoT y GPS en tiempo real.

### 6️⃣ [6_ProtocoloHTTP/](6_ProtocoloHTTP/) — Protocolo HTTP/1.1 sobre Sockets TCP
- **01_anatomia_http_y_verbos.py**: Estructura de peticiones (GET, POST, PUT, DELETE) y cabeceras CRLF.
- **02_cliente_http_artesanal_get.py**: Construcción manual de peticiones HTTP/1.1 con sockets TCP puros.
- **03_servidor_http_artesanal.py**: Servidor web básico que sirve HTML y procesa cabeceras.
- **04_codigos_de_estado_http.py**: Códigos 200, 301, 400, 404, 500 y su semántica.
- **05_mini_chequeo_http.py**: Chequeo interactivo sobre cabeceras, métodos y formato HTTP.
- **06_ejemplo_vida_real.py**: API REST artesanal con endpoints JSON (`/api/hora`, `/api/sistema`, `/api/eco`).

### 7️⃣ [7_TCPoUDP/](7_TCPoUDP/) — Comparativa y Toma de Decisiones
- **01_criterio_de_decision_tcp_vs_udp.py**: Árbol de decisión basado en fiabilidad vs latencia.
- **02_practica_eco_cara_a_cara.py**: Comparación directa de un servidor eco en TCP vs UDP.
- **03_los_seis_retos_practicos.py**: 6 ejercicios de clasificación de casos de uso reales.
- **04_se_el_socket_y_quien_soy.py**: Juego interactivo de rol identificando características de protocolo.
- **05_simulador_entrevista_tecnica.py**: Simulador de preguntas técnicas de entrevista de trabajo.
- **06_ejemplo_vida_real.py**: Arquitectura híbrida: Streaming UDP de coordenadas + Autenticación TCP.

### 8️⃣ [8_Ejercicios1/](8_Ejercicios1/) — Actividades No Evaluables 01 (CEEDCV)
- **ejercicio_01_servidor_saludo.py**: Servidor TCP que envía *"Bienvenido al servidor"* y cierra.
- **ejercicio_02_cliente_envia_recibe.py**: Cliente TCP que envía *"Hola"* a `127.0.0.1:9000` y muestra respuesta.
- **ejercicio_03_servidor_eco.py**: Servidor TCP que devuelve exactamente los mismos bytes recibidos.
- **ejercicio_04_ip_y_puerto.py**: Respuestas teóricas sobre IP vs Puerto, `127.0.0.1` y constantes Python.
- **ejercicio_05_cliente_udp_input.py**: Cliente UDP con entrada interactiva por `input()`.
- **ejercicio_06_servidor_udp_eco_personalizado.py**: Servidor UDP que responde `"Recibido: <mensaje>"`.
- **ejercicio_07_tcp_vs_udp_clasifica.py**: Clasificación justificada de 6 aplicaciones y tabla comparativa.
- **ejercicio_08_cliente_http_manual.py**: Cliente HTTP TCP manual a `example.com:80` mostrando primeros 500 caracteres.

### 9️⃣ [9_Ejercicios2/](9_Ejercicios2/) — Actividades No Evaluables 02 - Avanzado (CEEDCV)
- **ejercicio_01_servidor_cuenta_caracteres.py**: Cuenta caracteres recibidos y devuelve longitud (`"hola"` → `"4"`).
- **ejercicio_02_cliente_interactivo.py**: Bucle interactivo con `input()` hasta que el usuario teclea `"salir"`.
- **ejercicio_03_servidor_mayusculas.py**: Transforma el texto recibido a mayúsculas con `.upper()`.
- **ejercicio_04_cliente_con_reconexion.py**: Reintentos automáticos (hasta 3 intentos con 2s) ante caídas de servidor.
- **ejercicio_05_servidor_select_sin_hilos.py**: Multiplexación I/O mono-hilo con `select.select()` y `setblocking(False)`.
- **ejercicio_06_servidor_timeout_personalizado.py**: Cierre por inactividad a los 10s con `conn.settimeout(10)`.
- **ejercicio_07_cliente_ntp_manual.py**: Cliente NTP manual sobre UDP en puerto 123 y desempaquetado con `struct.unpack`.
- **ejercicio_08_servidor_udp_multimensaje.py**: Ciclo de vida finito con `range(1, 4)` respondiendo `"OK #1"`, `"OK #2"`, `"OK #3"`.
- **ejercicio_09_ping_udp.py**: Ping UDP ("PING" → "PONG") con medición de latencia RTT y estadísticas.
- **ejercicio_10_servidor_todas_las_interfaces.py**: Escucha global en `0.0.0.0` (`INADDR_ANY`).
- **ejercicio_11_compara_tcp_y_udp.py**: Benchmark empírico de 10 conexiones TCP vs 10 intercambios UDP.
- **ejercicio_12_mini_servidor_web.py**: Mini servidor web HTTP en `127.0.0.1:8080` con `SO_REUSEADDR`.

---

## 🚀 Requisitos y Ejecución

### Requisitos Previos
- Python 3.8 o superior (probado en Python 3.12).
- Módulos estándar únicamente (`socket`, `threading`, `time`, `struct`, `select`, `datetime`). No requiere dependencias externas (`pip`).

### Ejecución de Pruebas Rápidas
Cualquier archivo puede ejecutarse de manera directa:
```bash
# Ejemplo: Servidor y cliente interactivo en una sola orden
python3 9_Ejercicios2/ejercicio_05_servidor_select_sin_hilos.py --demo

# Ejemplo: Cliente NTP oficial
python3 9_Ejercicios2/ejercicio_07_cliente_ntp_manual.py

# Ejemplo: Benchmark de rendimiento TCP vs UDP
python3 9_Ejercicios2/ejercicio_11_compara_tcp_y_udp.py
```

---

## 📊 Cuadro Resumen: TCP vs UDP

| Característica | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
| :--- | :--- | :--- |
| **Conexión** | Sí (*Three-Way Handshake*) | No (*Connectionless*) |
| **Fiabilidad** | Alta (Garantizada por ACKs y retransmisión) | Mejor esfuerzo (*Best-effort*, sin garantías) |
| **Orden** | Garantizado (Números de secuencia) | No garantizado (Pueden desordenarse) |
| **Control de Flujo / Congestión** | Sí (Ventana deslizante) | No |
| **Sobrecarga de Cabecera** | 20 a 60 bytes | 8 bytes fijos |
| **Casos de Uso Típicos** | Web (HTTP/S), Correo (SMTP), Archivos (FTP), SSH | Videollamadas (VoIP), Juegos online, DNS, Streaming en vivo |

---

## 👩‍💻 Autora y Licencia
- **Autora:** Carla Mendía (`@carla87571`)
- **Módulo:** Programación de Servicios y Procesos (PSP)
- **Licencia:** Reconocimiento - No comercial - CompartirIgual (CC BY-NC-SA)

