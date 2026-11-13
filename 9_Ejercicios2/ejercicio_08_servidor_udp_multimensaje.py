"""
=============================================================================
EJERCICIO 8: SERVIDOR UDP MULTIMENSAJE CON CONTADOR
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor UDP que reciba y responda a 3 mensajes consecutivos
en un bucle antes de cerrarse. Cada respuesta debe incluir el número de orden:
'OK #1', 'OK #2', 'OK #3'.

💡 Pista: usa for i in range(1, 4) en lugar de while True: así el servidor
se cierra solo tras la tercera respuesta. El with libera el socket al salir."

CONCEPTOS CLAVE:
1. Servidor de ciclo de vida finito:
   A menudo los ejercicios o microservicios de tareas específicas no requieren
   un bucle infinito while True. Un bucle con contador definido permite finalizar
   el programa de forma predecible y limpia.
2. Gestor de contexto with:
   Garantiza que al finalizar el bucle o si ocurre alguna excepción, el método
   __exit__() invocará close() liberando el puerto del sistema operativo.
3. Respuestas correlacionadas:
   En UDP no hay número de secuencia de transporte; el servidor implementa la
   secuencia en la capa de aplicación enviando "OK #1", "OK #2", etc.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9020
BUFFER_SIZE = 1024


def ejecutar_servidor_multimensaje(host: str = HOST, puerto: int = PUERTO):
    """
    Ejecuta el servidor UDP que procesa exactamente 3 mensajes antes de finalizar.
    """
    print("=" * 70)
    print("        🔢 EJERCICIO 8: SERVIDOR UDP MULTIMENSAJE")
    print("=" * 70)
    print(f"[*] Vinculando socket UDP a {host}:{puerto}...")

    # Pista: El with libera el socket al salir automáticamente
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, puerto))
        print(f"[+] Servidor UDP activo. Esperando exactamente 3 datagramas...")
        print("-" * 70)

        # Pista: usa for i in range(1, 4) en lugar de while True
        for i in range(1, 4):
            print(f"[*] [{i}/3] Esperando datagrama #{i}...")

            datos, addr_cliente = s.recvfrom(BUFFER_SIZE)
            mensaje_cliente = datos.decode("utf-8", errors="replace").strip()
            print(f"📥 Datagrama #{i} recibido de {addr_cliente}: \"{mensaje_cliente}\"")

            # Construir la respuesta con el número de orden solicitado
            respuesta = f"OK #{i}"
            print(f"📤 Enviando respuesta correlacionada: \"{respuesta}\"...")
            s.sendto(respuesta.encode("utf-8"), addr_cliente)
            print(f"[+] Respuesta #{i} enviada con éxito.\n")

    # Al salir del bloque with, el socket se cierra automáticamente
    print("=" * 70)
    print("[*] Bloque 'with' finalizado. Socket UDP cerrado y liberado automáticamente.")
    print("[i] Ejercicio 8 completado con éxito tras 3 mensajes.")


def cliente_demo_multimensaje(puerto: int = PUERTO):
    """Cliente que envía 3 mensajes consecutivos y muestra las respuestas OK #1..#3."""
    time.sleep(0.2)
    print("\n   [Cliente UDP Test] Iniciando ráfaga de 3 mensajes...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
            c.settimeout(3.0)
            mensajes = ["Primer mensaje", "Segundo mensaje", "Tercer mensaje"]
            for m in mensajes:
                c.sendto(m.encode("utf-8"), (HOST, puerto))
                resp, _ = c.recvfrom(BUFFER_SIZE)
                texto = resp.decode("utf-8")
                print(f"   [Cliente UDP Test] Enviado: '{m}' -> Recibido: '{texto}'")
            print("   [Cliente UDP Test] ✅ ¡Verificación de 3 mensajes completada exitosamente!")
    except Exception as e:
        print(f"   [Cliente UDP Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_demo_multimensaje, daemon=True)
        hilo.start()
        ejecutar_servidor_multimensaje()
        hilo.join(timeout=1.0)
    else:
        ejecutar_servidor_multimensaje()

