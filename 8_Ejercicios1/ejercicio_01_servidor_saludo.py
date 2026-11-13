"""
=============================================================================
EJERCICIO 1: SERVIDOR SALUDO (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor TCP que, cuando un cliente se conecte, le envíe
“Bienvenido al servidor” y luego cierre la conexión."

CONCEPTOS CLAVE:
1. socket.AF_INET: Familia de direcciones IPv4.
2. socket.SOCK_STREAM: Protocolo orientado a conexión confiable (TCP).
3. bind((IP, PUERTO)): Asocia el socket a una interfaz de red y puerto local.
4. listen(backlog): Pone el socket en modo escucha pasiva para recibir peticiones.
5. accept(): Bloquea hasta que llega un cliente. Devuelve (socket_cliente, direccion_cliente).
6. sendall(bytes): Envía todos los datos garantizando la entrega.
7. close(): Cierra el socket del cliente liberando el recurso.
=============================================================================
"""

import socket
import sys
import time
import threading

# Configuración del servidor
HOST = "127.0.0.1"  # localhost (interfaz de bucle invertido)
PUERTO = 9000       # Puerto acordado en los ejercicios
MENSAJE = "Bienvenido al servidor"


def ejecutar_servidor(puerto: int = PUERTO, una_sola_conexion: bool = True):
    """
    Inicia el servidor TCP de saludo.
    
    :param puerto: Puerto TCP donde escuchará el servidor.
    :param una_sola_conexion: Si es True, atiende a 1 cliente y finaliza (ideal para ejercicios).
                             Si es False, se mantiene en bucle infinito atendiendo clientes.
    """
    print("=" * 65)
    print("        🚀 EJERCICIO 1: SERVIDOR TCP DE SALUDO")
    print("=" * 65)
    print(f"[*] Configurando socket TCP en {HOST}:{puerto}...")

    # 1. Crear el socket TCP
    # AF_INET = IPv4, SOCK_STREAM = TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_REUSEADDR permite reiniciar el servidor de inmediato sin esperar el estado TIME_WAIT
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # 2. Asociar el socket a la IP y puerto
        servidor_socket.bind((HOST, puerto))
        print(f"[+] bind() exitoso en {HOST}:{puerto}")

        # 3. Poner el socket a la escucha (cola máxima de 5 conexiones pendientes)
        servidor_socket.listen(5)
        print(f"[+] listen() activado. Servidor listo esperando clientes...")
        print("-" * 65)
        print(f"💡 Para probarlo:")
        print(f"   - Ejecuta en otra terminal: python3 ejercicio_02_cliente_envia_recibe.py")
        print(f"   - O mediante netcat: nc 127.0.0.1 {puerto}")
        print("-" * 65)

        contador = 0
        while True:
            # 4. accept() espera y acepta la conexión entrante de un cliente
            # Devuelve un nuevo socket exclusivo para este cliente y su tupla (IP, puerto)
            cliente_socket, cliente_direccion = servidor_socket.accept()
            contador += 1
            print(f"\n[+] ¡Nueva conexión #{contador} aceptada desde {cliente_direccion}!")

            try:
                # 5. Enviar mensaje de bienvenida codificado en UTF-8 (bytes)
                mensaje_bytes = MENSAJE.encode("utf-8")
                print(f"[>] Enviando saludo: \"{MENSAJE}\" ({len(mensaje_bytes)} bytes)")
                cliente_socket.sendall(mensaje_bytes)
                print("[+] Saludo enviado correctamente.")

                # Breve lectura/espera para permitir al cliente recibir completamente el saludo
                # y procesar cualquier mensaje enviado por el cliente (ej. si se conecta con el Ejercicio 2)
                cliente_socket.settimeout(0.3)
                try:
                    datos_cliente = cliente_socket.recv(1024)
                    if datos_cliente:
                        print(f"[i] Datos adicionales recibidos del cliente: \"{datos_cliente.decode('utf-8', errors='replace')}\"")
                except (socket.timeout, OSError):
                    pass
            finally:
                # 6. Cerrar la conexión con el cliente según pide el enunciado
                cliente_socket.close()
                print(f"[-] Conexión con {cliente_direccion} cerrada.")

            if una_sola_conexion:
                print("\n[i] Ejercicio 1 completado con éxito tras atender al cliente.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario (Ctrl + C).")
    except OSError as err:
        print(f"\n[❌] Error en el servidor: {err}")
    finally:
        # 7. Cerrar el socket principal del servidor
        servidor_socket.close()
        print("[*] Socket del servidor cerrado.")


def cliente_prueba_demo(puerto: int = PUERTO):
    """Cliente de prueba que se conecta al servidor para verificar su funcionamiento."""
    time.sleep(0.3)  # Esperar a que el servidor haya iniciado listen()
    print("\n   [Cliente Demo] Conectándose al servidor...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            datos = c.recv(1024)
            print(f"   [Cliente Demo] Respuesta recibida: \"{datos.decode('utf-8')}\"")
    except Exception as e:
        print(f"   [Cliente Demo] Error de conexión: {e}")


if __name__ == "__main__":
    # Si se pasa el argumento --demo o se ejecuta de forma no interactiva,
    # lanza un hilo cliente para demostrar el funcionamiento completo sin bloquear.
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA ACTIVADO]")
        hilo_cliente = threading.Thread(target=cliente_prueba_demo, args=(PUERTO,), daemon=True)
        hilo_cliente.start()
        ejecutar_servidor(puerto=PUERTO, una_sola_conexion=True)
        hilo_cliente.join(timeout=1.0)
    else:
        # Modo interactivo estándar: escucha en el puerto hasta que se conecte un cliente
        ejecutar_servidor(puerto=PUERTO, una_sola_conexion=True)
