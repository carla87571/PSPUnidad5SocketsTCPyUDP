"""
=============================================================================
EJERCICIO 5: SERVIDOR CON SELECT - MÚLTIPLES CONEXIONES SIN HILOS (I/O MULTIPLEXING)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Usa select.select() para atender a varios clientes en un solo hilo.

💡 Pista: configura el socket servidor como no bloqueante con setblocking(False).
select.select() te devuelve los sockets que tienen datos listos para leer.
Si el socket listo es el servidor, acepta una nueva conexión; si es un cliente, recibe datos."

CONCEPTOS CLAVE:
1. I/O Multiplexing (Multiplexación de Entrada/Salida):
   Técnica que permite a un único hilo de ejecución supervisar decenas o cientos
   de sockets a la vez sin necesidad de crear hilos (threads) ni procesos pesados.
2. setblocking(False):
   Hace que las llamadas accept(), recv() y send() no detengan el hilo si no hay
   datos disponibles inmediatamente.
3. select.select(rlist, wlist, xlist, timeout):
   Función del sistema operativo que duerme el proceso de forma eficiente hasta
   que al menos uno de los descriptores de fichero/sockets esté listo para operar.
=============================================================================
"""

import socket
import select
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9010
BUFFER_SIZE = 1024


def ejecutar_servidor_select(host: str = HOST, puerto: int = PUERTO, max_conexiones_demo: int = 0):
    """
    Ejecuta el servidor con select.select() para concurrencia mono-hilo.
    
    :param host: IP de escucha.
    :param puerto: Puerto TCP.
    :param max_conexiones_demo: Si > 0, termina tras procesar ese número de conexiones (para tests).
    """
    print("=" * 70)
    print("    ⚡ EJERCICIO 5: SERVIDOR MULTI-CONEXIÓN SIN HILOS (select.select)")
    print("=" * 70)
    print(f"[*] Configurando servidor en {host}:{puerto}...")

    # 1. Crear el socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen(10)

    # 2. Pista: Configurar socket como no bloqueante
    servidor_socket.setblocking(False)
    print(f"[+] setblocking(False) activado en el servidor.")

    # 3. Lista de sockets a supervisar para lectura (rlist)
    # Inicialmente solo contiene el socket de escucha del servidor
    sockets_lectura = [servidor_socket]
    clientes_atendidos = 0

    print(f"[+] Servidor escuchando en {host}:{puerto} (Mono-hilo concurrente listo)")
    print("-" * 70)

    try:
        while sockets_lectura:
            # 4. Pista: select.select() devuelve los sockets que tienen datos listos para leer
            # Timeout de 1.0 segundo para permitir interrupciones limpias con Ctrl+C
            listos_para_leer, _, _ = select.select(sockets_lectura, [], [], 1.0)

            for s in listos_para_leer:
                # Caso A: El socket listo es el SERVIDOR -> Hay una NUEVA CONEXIÓN entrante
                if s is servidor_socket:
                    conn, addr = servidor_socket.accept()
                    conn.setblocking(False)  # El nuevo socket cliente también debe ser no bloqueante
                    sockets_lectura.append(conn)
                    clientes_atendidos += 1
                    print(f"\n[+] ¡Nueva conexión aceptada desde {addr}!")
                    print(f"    Sockets activos bajo supervisión de select: {len(sockets_lectura)}")

                # Caso B: El socket listo es un CLIENTE -> Hay DATOS para leer
                else:
                    try:
                        datos = s.recv(BUFFER_SIZE)
                        if datos:
                            mensaje = datos.decode("utf-8", errors="replace").strip()
                            remitente = s.getpeername()
                            print(f"📥 Datos de {remitente}: \"{mensaje}\"")

                            # Responder al cliente
                            respuesta = f"Servidor Select OK: Recibido '{mensaje}'\n"
                            s.sendall(respuesta.encode("utf-8"))
                        else:
                            # Si recv devuelve 0 bytes, el cliente cerró la conexión
                            remitente = s.getpeername()
                            print(f"[-] Cliente {remitente} desconectado.")
                            sockets_lectura.remove(s)
                            s.close()
                    except (ConnectionResetError, BrokenPipeError):
                        sockets_lectura.remove(s)
                        s.close()

            # En modo demo, si ya se procesaron los clientes objetivo y se cerraron, terminamos
            if max_conexiones_demo > 0 and clientes_atendidos >= max_conexiones_demo and len(sockets_lectura) == 1:
                print(f"\n[i] Demostración completada: {clientes_atendidos} clientes atendidos concurrentemente.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor select interrumpido por el usuario.")
    finally:
        # Cerrar todos los sockets abiertos
        for s in sockets_lectura:
            s.close()
        print("[*] Servidor y todos los sockets cerrados.")


def cliente_simultaneo(id_cliente: int, puerto: int = PUERTO):
    """Cliente que envía mensajes para probar la concurrencia."""
    time.sleep(0.1 * id_cliente)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            msg = f"Mensaje del Cliente #{id_cliente}"
            c.sendall(msg.encode("utf-8"))
            resp = c.recv(BUFFER_SIZE).decode("utf-8")
            print(f"   [Cliente #{id_cliente}] Recibió respuesta: {resp.strip()}")
            time.sleep(0.05)
    except Exception as e:
        print(f"   [Cliente #{id_cliente}] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN: Lanzando 3 clientes simultáneos contra 1 solo hilo]")
        hilos = []
        for i in range(1, 4):
            h = threading.Thread(target=cliente_simultaneo, args=(i, PUERTO), daemon=True)
            hilos.append(h)

        # Iniciar los clientes casi a la vez
        for h in hilos:
            h.start()

        # Ejecutar servidor select atendiendo a los 3
        ejecutar_servidor_select(max_conexiones_demo=3)

        for h in hilos:
            h.join(timeout=1.0)
    else:
        ejecutar_servidor_select()

