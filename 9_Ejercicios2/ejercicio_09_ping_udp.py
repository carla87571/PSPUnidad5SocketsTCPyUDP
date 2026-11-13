"""
=============================================================================
EJERCICIO 9: PING UDP CON MEDICIÓN DE LATENCIA (RTT)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Cliente manda “PING”, servidor responde “PONG”. Mide cuánto tarda.

💡 Pista: necesitas dos funciones (servidor y cliente) ejecutándose en paralelo.
Usa threading.Thread con daemon=True para lanzar el servidor.
Mide el tiempo con time.time() antes y después del intercambio de mensajes."

CONCEPTOS CLAVE:
1. RTT (Round-Trip Time):
   Tiempo total que tarda un paquete en viajar de ida y vuelta (origen -> destino -> origen).
2. Protocolo Ping a nivel de transporte:
   El ping clásico usa ICMP (Capa 3 de red). Implementar un ping con UDP en Capa 4
   permite medir la latencia real que experimentan los juegos y aplicaciones en tiempo real.
3. Concurrencia con threading:
   Permite emular cliente y servidor en el mismo script para pruebas automáticas.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9025
BUFFER_SIZE = 1024


def funcion_servidor(host: str = HOST, puerto: int = PUERTO, num_pings: int = 4):
    """
    Función del servidor UDP: espera 'PING' y responde 'PONG'.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, puerto))
        print(f"[Servidor UDP] Escuchando en {host}:{puerto} listo para responder PING...")

        for _ in range(num_pings):
            try:
                datos, addr = s.recvfrom(BUFFER_SIZE)
                mensaje = datos.decode("utf-8", errors="replace").strip()
                if mensaje == "PING":
                    s.sendto(b"PONG", addr)
                else:
                    s.sendto(f"ECO:{mensaje}".encode("utf-8"), addr)
            except Exception:
                break


def funcion_cliente(host: str = HOST, puerto: int = PUERTO, repeticiones: int = 4):
    """
    Función del cliente UDP: envía 'PING', espera 'PONG' y mide el tiempo exacto.
    """
    time.sleep(0.15)  # Breve margen para que el servidor haya iniciado
    print("=" * 70)
    print("        🏓 EJERCICIO 9: PING UDP Y MEDICIÓN DE LATENCIA")
    print("=" * 70)
    print(f"[*] Enviando {repeticiones} paquetes PING a {host}:{puerto}...\n")

    tiempos_ms = []

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.settimeout(2.0)

        for i in range(1, repeticiones + 1):
            # Pista: Mide el tiempo con time.time() antes y después del intercambio
            inicio = time.time()

            # 1. Enviar "PING"
            c.sendto(b"PING", (host, puerto))

            # 2. Recibir "PONG"
            try:
                respuesta, servidor = c.recvfrom(BUFFER_SIZE)
                fin = time.time()

                rtt_segundos = fin - inicio
                rtt_milisegundos = rtt_segundos * 1000.0
                rtt_microsegundos = rtt_segundos * 1_000_000.0
                tiempos_ms.append(rtt_milisegundos)

                texto = respuesta.decode("utf-8")
                print(f"   [Ping #{i}] Enviado 'PING' -> Recibido '{texto}' desde {servidor}")
                print(f"            RTT: {rtt_milisegundos:.4f} ms ({rtt_microsegundos:.1f} µs)")

            except socket.timeout:
                print(f"   [Ping #{i}] ⚠️ TIMEOUT: El paquete se perdió o no hubo respuesta.")

            time.sleep(0.1)

    # Estadísticas finales
    if tiempos_ms:
        print("\n" + "-" * 70)
        print("📊 ESTADÍSTICAS DEL PING UDP:")
        print(f"   • Paquetes transmitidos: {repeticiones}, Recibidos: {len(tiempos_ms)} (0% pérdidas)")
        print(f"   • Latencia Mínima:       {min(tiempos_ms):.4f} ms")
        print(f"   • Latencia Media:        {sum(tiempos_ms) / len(tiempos_ms):.4f} ms")
        print(f"   • Latencia Máxima:       {max(tiempos_ms):.4f} ms")
        print("-" * 70)


def ejecutar_ping_completo():
    """Lanza el servidor en segundo plano con threading y ejecuta el cliente."""
    # Pista: Usa threading.Thread con daemon=True para lanzar el servidor
    hilo_servidor = threading.Thread(
        target=funcion_servidor,
        args=(HOST, PUERTO, 4),
        daemon=True
    )
    hilo_servidor.start()

    # Ejecutar cliente en el hilo principal
    funcion_cliente(HOST, PUERTO, repeticiones=4)
    hilo_servidor.join(timeout=1.0)
    print("[i] Ejercicio 9 finalizado con éxito.")


if __name__ == "__main__":
    ejecutar_ping_completo()

