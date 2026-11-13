"""
=============================================================================
EJERCICIO 10: SERVIDOR EN TODAS LAS INTERFACES (0.0.0.0 - INADDR_ANY)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"El servidor escucha en todas las interfaces y responde a cualquiera.

💡 Pista: el servidor debe escuchar en "0.0.0.0" para aceptar conexiones
de cualquier interfaz. Usa un bucle infinito con recvfrom() y responde con
sendto() a la dirección de cada cliente.

Nota del profesor: no es broadcast (eso exigiría SO_BROADCAST y enviar
a 255.255.255.255); es un servidor que escucha en todas las interfaces."

CONCEPTOS CLAVE:
1. "0.0.0.0" (INADDR_ANY):
   Indica al sistema operativo que vincule el socket a TODAS las interfaces de red
   presentes en la máquina (loopback 127.0.0.1, Ethernet 192.168.x.x, Wi-Fi, VPNs, etc.).
2. Diferencia con 127.0.0.1:
   - 127.0.0.1: Solo escucha peticiones originadas en la misma máquina local.
   - 0.0.0.0:   Escucha peticiones locales y también las que lleguen desde cualquier
                otro equipo de la red de área local o de internet.
3. Diferencia con Broadcast (255.255.255.255):
   - Escuchar en 0.0.0.0 es unicast pasivo en múltiples interfaces.
   - Broadcast es enviar un paquete activo a todos los equipos de la subred a la vez.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST_TODAS_INTERFACES = "0.0.0.0"
PUERTO = 9030
BUFFER_SIZE = 1024


def ejecutar_servidor_todas_interfaces(puerto: int = PUERTO, un_solo_paquete: bool = True):
    """
    Ejecuta el servidor UDP escuchando en 0.0.0.0.
    
    :param puerto: Puerto de escucha UDP.
    :param un_solo_paquete: Si es True, atiende 1 datagrama y finaliza (ideal para ejercicios).
    """
    print("=" * 70)
    print("        🌐 EJERCICIO 10: SERVIDOR EN TODAS LAS INTERFACES (0.0.0.0)")
    print("=" * 70)
    print(f"[*] Creando socket UDP (SOCK_DGRAM)...")

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Pista: Vincular a "0.0.0.0" para escuchar en todas las interfaces físicas y virtuales
        servidor_socket.bind((HOST_TODAS_INTERFACES, puerto))
        print(f"[+] bind() exitoso en {HOST_TODAS_INTERFACES}:{puerto}")
        print("-" * 70)
        print("💡 Explicación pedagógica de '0.0.0.0':")
        print("   • Permite recibir paquetes desde '127.0.0.1' (localhost).")
        print("   • Permite recibir paquetes desde tu IP de red local (ej. 192.168.1.X).")
        print("   • Si tuviéramos tarjeta Wi-Fi y cable Ethernet, escucharía por ambas.")
        print("-" * 70)

        contador = 0
        while True:
            print(f"[*] Esperando datagrama en cualquier interfaz (puerto {puerto})...")

            # Pista: bucle con recvfrom() y responde con sendto() a la dirección de cada cliente
            datos, addr_cliente = servidor_socket.recvfrom(BUFFER_SIZE)
            contador += 1
            mensaje = datos.decode("utf-8", errors="replace").strip()
            print(f"\n[+] Datagrama #{contador} recibido desde {addr_cliente}:")
            print(f"    Contenido: \"{mensaje}\"")

            # Construir respuesta
            respuesta = f"Servidor(0.0.0.0): Saludos {addr_cliente[0]}:{addr_cliente[1]}, procese tu mensaje '{mensaje}'"
            print(f"[>] Enviando respuesta unicast a {addr_cliente}...")
            servidor_socket.sendto(respuesta.encode("utf-8"), addr_cliente)
            print("[+] Respuesta enviada correctamente.")

            if un_solo_paquete:
                print("\n[i] Ejercicio 10 completado con éxito tras responder al cliente.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario.")
    finally:
        servidor_socket.close()
        print("[*] Socket UDP cerrado.")


def cliente_demo_interfaces(puerto: int = PUERTO):
    """Cliente que envía un datagrama conectando a localhost para verificar la recepción en 0.0.0.0."""
    time.sleep(0.2)
    print("\n   [Cliente Test] Enviando datagrama a 127.0.0.1 (el servidor en 0.0.0.0 lo capturará)...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
            c.settimeout(3.0)
            msg = "Hola servidor en 0.0.0.0"
            c.sendto(msg.encode("utf-8"), ("127.0.0.1", puerto))
            resp, _ = c.recvfrom(BUFFER_SIZE)
            print(f"   [Cliente Test] Respuesta recibida:\n   \"{resp.decode('utf-8')}\"")
            print("   [Cliente Test] ✅ ¡Verificación de escucha en 0.0.0.0 completada!")
    except Exception as e:
        print(f"   [Cliente Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_demo_interfaces, daemon=True)
        hilo.start()
        ejecutar_servidor_todas_interfaces(un_solo_paquete=True)
        hilo.join(timeout=1.0)
    else:
        ejecutar_servidor_todas_interfaces(un_solo_paquete=False)

