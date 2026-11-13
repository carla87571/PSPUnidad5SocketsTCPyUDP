"""
=============================================================================
EJERCICIO 11: COMPARATIVA DE RENDIMIENTO TCP VS UDP (10 INTERCAMBIOS)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Escribe un programa que mida cuánto tarda en completar 10 intercambios
de mensajes contra un servidor TCP y contra un servidor UDP en local.
Compara los tiempos.

💡 Pista: en TCP cada intercambio exige connect() (handshake);
en UDP basta un sendto() + recvfrom(). Mide con time.time() antes
y después de cada bucle."

CONCEPTOS CLAVE:
1. Sobrecarga del Three-Way Handshake en TCP:
   Cada nueva conexión TCP requiere un intercambio de 3 paquetes (SYN, SYN-ACK, ACK)
   y un cierre de conexión de 4 paquetes (FIN, ACK, FIN, ACK).
2. Agilidad de UDP:
   UDP envía los datos directamente en el primer paquete sin ninguna negociación
   previa, alcanzando una latencia significativamente menor.
3. El compromiso (Trade-off):
   UDP es más rápido, pero TCP garantiza fiabilidad, orden y control de flujo.
=============================================================================
"""

import socket
import time
import threading

HOST = "127.0.0.1"
PUERTO_TCP = 9040
PUERTO_UDP = 9041
NUM_INTERCAMBIOS = 10
BUFFER_SIZE = 1024


# -------------------------------------------------------------------------
# SERVIDORES EN SEGUNDO PLANO
# -------------------------------------------------------------------------
def servidor_tcp(puerto: int = PUERTO_TCP, repeticiones: int = NUM_INTERCAMBIOS):
    """Servidor TCP que atiende a 'repeticiones' clientes sucesivos."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, puerto))
        s.listen(repeticiones)
        for _ in range(repeticiones):
            conn, addr = s.accept()
            with conn:
                data = conn.recv(BUFFER_SIZE)
                conn.sendall(b"ACK_TCP")


def servidor_udp(puerto: int = PUERTO_UDP, repeticiones: int = NUM_INTERCAMBIOS):
    """Servidor UDP que responde a 'repeticiones' datagramas."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, puerto))
        for _ in range(repeticiones):
            data, addr = s.recvfrom(BUFFER_SIZE)
            s.sendto(b"ACK_UDP", addr)


# -------------------------------------------------------------------------
# BENCHMARK Y MEDICIÓN
# -------------------------------------------------------------------------
def medir_tcp(host: str, puerto: int, n: int) -> float:
    """Mide el tiempo total en segundos para completar n conexiones TCP completas."""
    print(f"[*] Ejecutando {n} conexiones TCP (con handshake connect() + close())...")
    
    # Pista: Mide con time.time() antes y después del bucle
    t_inicio = time.time()
    for i in range(1, n + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((host, puerto))
            c.sendall(b"HOLA_TCP")
            resp = c.recv(BUFFER_SIZE)
    t_fin = time.time()
    
    duracion = t_fin - t_inicio
    print(f"   [TCP] Completados {n} intercambios en {duracion:.5f} s")
    return duracion


def medir_udp(host: str, puerto: int, n: int) -> float:
    """Mide el tiempo total en segundos para completar n intercambios de datagramas UDP."""
    print(f"[*] Ejecutando {n} intercambios UDP (sendto() + recvfrom() directos)...")

    # Pista: Mide con time.time() antes y después del bucle
    t_inicio = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.settimeout(2.0)
        for i in range(1, n + 1):
            c.sendto(b"HOLA_UDP", (host, puerto))
            resp, _ = c.recvfrom(BUFFER_SIZE)
    t_fin = time.time()

    duracion = t_fin - t_inicio
    print(f"   [UDP] Completados {n} intercambios en {duracion:.5f} s")
    return duracion


def ejecutar_comparativa():
    print("=" * 70)
    print("        ⚡ EJERCICIO 11: BENCHMARK TCP VS UDP (10 INTERCAMBIOS)")
    print("=" * 70)

    # 1. Iniciar servidores en hilos daemon
    hilo_tcp = threading.Thread(target=servidor_tcp, args=(PUERTO_TCP, NUM_INTERCAMBIOS), daemon=True)
    hilo_udp = threading.Thread(target=servidor_udp, args=(PUERTO_UDP, NUM_INTERCAMBIOS), daemon=True)
    hilo_tcp.start()
    hilo_udp.start()
    time.sleep(0.2)  # Dejar que los puertos se abran

    # 2. Medir ambos protocolos
    tiempo_tcp = medir_tcp(HOST, PUERTO_TCP, NUM_INTERCAMBIOS)
    tiempo_udp = medir_udp(HOST, PUERTO_UDP, NUM_INTERCAMBIOS)

    # 3. Presentar informe comparativo
    media_tcp_ms = (tiempo_tcp / NUM_INTERCAMBIOS) * 1000
    media_udp_ms = (tiempo_udp / NUM_INTERCAMBIOS) * 1000
    ratio = tiempo_tcp / tiempo_udp if tiempo_udp > 0 else 1.0

    print("\n" + "=" * 70)
    print("📊 RESULTADOS DE LA COMPARATIVA:")
    print("=" * 70)
    print(f"  Métrica                  | TCP (con Handshake)    | UDP (sin conexión)")
    print("-" * 70)
    print(f"  Tiempo total (10 veces)  | {tiempo_tcp * 1000:10.3f} ms        | {tiempo_udp * 1000:10.3f} ms")
    print(f"  Tiempo medio por mensaje | {media_tcp_ms:10.3f} ms        | {media_udp_ms:10.3f} ms")
    print("-" * 70)
    print(f"  🚀 Factor de rapidez: UDP fue aproximadamente {ratio:.2f} veces más veloz en la conexión.")
    print("=" * 70)
    print("💡 CONCLUSIÓN PEDAGÓGICA:")
    print("   • TCP tarda más porque en CADA mensaje realiza la negociación de 3 vías (SYN, SYN-ACK, ACK)")
    print("     y la secuencia de desconexión (FIN/ACK).")
    print("   • UDP es casi instantáneo porque lanza el datagrama directamente a la red sin esperas.")
    print("   • Si en TCP se reutilizara la misma conexión establecida (Keep-Alive), la velocidad")
    print("     se aproximaría a UDP, pero con la garantía absoluta de entrega.")
    print("=" * 70)

    hilo_tcp.join(timeout=1.0)
    hilo_udp.join(timeout=1.0)
    print("[i] Ejercicio 11 finalizado con éxito.")


if __name__ == "__main__":
    ejecutar_comparativa()

