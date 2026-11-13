"""
03_los_dos_sockets_servidor_vs_conexion.py
==========================================
Diapositiva de referencia: Diapositiva 4 ("Cada método del servidor, al detalle")

EL CONCEPTO CLAVE: ¿POR QUÉ HAY DOS SOCKETS?
--------------------------------------------
La Diapositiva 4 resalta una advertencia fundamental:
"Fíjate: a partir de accept() todo se hace con conexion, no con servidor.
 El socket servidor solo escucha; conexion es el canal de esa llamada concreta."

ANALOGÍA DE LA EMPRESA Y EL RECEPCIONISTA:
------------------------------------------
  • El socket 'servidor':
    Es el RECEPCIONISTA en la puerta de entrada. No hace el trabajo con el cliente;
    su único rol es recibir al cliente que llega y pasarlo a una sala privada.

  • El socket 'conexion':
    Es la SALA PRIVADA donde el especialista atiende a ese cliente en particular.
    Ahí es donde se habla (sendall) y se escucha (recv).

¿QUÉ PASA SI INTENTAS ENVIAR O RECIBIR CON 'servidor'?
------------------------------------------------------
Si intentas llamar a servidor.recv(1024), Python lanzará OSError (Transport endpoint
is not connected), porque el socket servidor no está conectado a nadie, ¡está en modo escucha!
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5004

def cliente_auxiliar():
    time.sleep(0.2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((HOST, PORT))
        c.sendall(b"Mensaje de prueba")

def main():
    print("=" * 70)
    print("  03 - LOS DOS SOCKETS: 'servidor' VS 'conexion'")
    print("=" * 70)

    # Iniciar cliente auxiliar
    threading.Thread(target=cliente_auxiliar, daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()

        print("\n[1] ESTADO DEL SOCKET MAESTRO ('servidor'):")
        print(f"    • Descriptor de archivo (fileno): {servidor.fileno()}")
        print(f"    • Rol: Solo escucha en {HOST}:{PORT}")

        # Intento pedagógico erróneo: intentar recibir con 'servidor'
        print("\n[2] ¿QUÉ PASA SI INTENTAMOS servidor.recv()? (Error típico)")
        try:
            servidor.recv(1024)
        except OSError as e:
            print(f"    ❌ OSError capturado: {e}")
            print("       -> 'servidor' NO puede recibir datos directamente. Solo escucha.")

        # Atendemos la llamada
        conexion, direccion_cliente = servidor.accept()
        print(f"\n[3] ¡NUEVO SOCKET NACIDO TRAS accept()! ('conexion'):")
        print(f"    • Descriptor de 'conexion' (fileno): {conexion.fileno()} (¡Es otro número!)")
        print(f"    • Dirección del cliente remoto:      {direccion_cliente}")
        print("    • Rol: Canal exclusivo y privado para hablar con este cliente.")

        with conexion:
            # Ahora sí: usamos 'conexion' para hablar
            datos = conexion.recv(1024)
            print(f"\n[4] DATOS RECIBIDOS USANDO 'conexion':")
            print(f"    ✔ '{datos.decode()}'")

    print("\n" + "=" * 70)
    print("  REGLA DE ORO DE LA DIAPOSITIVA 4:")
    print("  • 'servidor'  -> Solo para bind(), listen() y accept().")
    print("  • 'conexion'  -> Solo para recv() y sendall().")
    print("=" * 70)

if __name__ == "__main__":
    main()

