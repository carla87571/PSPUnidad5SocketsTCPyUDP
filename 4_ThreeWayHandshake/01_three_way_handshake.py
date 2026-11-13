"""
01_three_way_handshake.py
=========================
Diapositiva de referencia: Diapositiva 1 ("Three-way handshake: El saludo que abre toda conexión TCP")

EL SALUDO DE 3 VÍAS EN TCP:
---------------------------
Antes de transmitir un solo byte de datos reales, TCP necesita garantizar que:
  a) El cliente puede enviar y el servidor puede recibir.
  b) El servidor puede enviar y el cliente puede recibir.
  c) Ambos acuerdan números de secuencia iniciales para ordenar futuros paquetes.

EL DIAGRAMA DEL HANDSHAKE (Diapositiva 1):
------------------------------------------
     CLIENTE                                          SERVIDOR
        │                                                │
        │ ── 1. SYN (Synchronize) ─────────────────────> │  "Hola, ¿podemos hablar?"
        │                                                │
        │ <─ 2. SYN + ACK (Sync + Acknowledge) ───────── │  "¡Hola! Te escucho (ACK) y yo también
        │                                                │   quiero hablar contigo (SYN)."
        │                                                │
        │ ── 3. ACK (Acknowledge) ─────────────────────> │  "Perfecto, recibido (ACK)."
        ▼                                                ▼
     [CONEXIÓN ESTABLECIDA: Los datos ya pueden fluir en ambas direcciones]

¿DÓNDE OCURRE ESTO EN PYTHON?
-----------------------------
En Python no envías paquetes SYN o ACK manualmente:
  • En el Cliente:  Ocurre dentro de 'cliente.connect((HOST, PORT))'.
  • En el Servidor: Ocurre cuando el SO procesa la cola y te entrega el socket en 'servidor.accept()'.
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5006

def servidor_handshake():
    """Servidor que muestra cuándo se completa el handshake a nivel de aplicación."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        
        # accept() se desbloquea únicamente cuando el handshake de 3 vías ha finalizado
        conn, addr = srv.accept()
        with conn:
            conn.recv(1024)

def main():
    print("=" * 70)
    print("  01 - THREE-WAY HANDSHAKE: EL SALUDO QUE ABRE TODA CONEXIÓN TCP")
    print("=" * 70)

    # 1. Explicación didáctica
    print("\n[1] LOS TRES PASOS DEL SALUDO:")
    print("    Paso 1: SYN     (Cliente  -> Servidor) : 'Quiero iniciar conexión'")
    print("    Paso 2: SYN+ACK (Servidor -> Cliente)  : 'Te escucho y acepto la conexión'")
    print("    Paso 3: ACK     (Cliente  -> Servidor) : 'Confirmado. Empecemos a hablar'")

    # 2. Simulación en tiempo real
    threading.Thread(target=servidor_handshake, daemon=True).start()
    time.sleep(0.2)

    print("\n[2] TRAZA EN PYTHON:")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        print("    • Llamando a cliente.connect()...")
        print("      -> El kernel envía SYN al servidor...")
        print("      <- El kernel recibe SYN+ACK del servidor...")
        print("      -> El kernel responde ACK...")
        
        cliente.connect((HOST, PORT))
        print("    ✔ connect() ha retornado: ¡Handshake completado con éxito!")
        print("    ✔ Canal bidireccional fiable listo para enviar y recibir datos.")
        
        cliente.sendall(b"Primeros datos reales")

    print("\n" + "=" * 70)
    print("  REGLA CLAVE: En Python, todo el Three-Way Handshake ocurre")
    print("  de forma transparente dentro de la llamada a connect().")
    print("=" * 70)

if __name__ == "__main__":
    main()

