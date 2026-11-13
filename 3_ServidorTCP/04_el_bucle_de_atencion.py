"""
04_el_bucle_de_atencion.py
==========================
Diapositiva de referencia: Diapositiva 5 ("El bucle de atención: Atender a más de un cliente")

EL PATRÓN 'while True':
-----------------------
Un servidor real nunca se apaga tras atender a un solo cliente.
Para atender clientes sucesivos, envolvemos accept() dentro de un bucle 'while True':

    while True:
        conexion, direccion = servidor.accept()
        with conexion:
            ... atender al cliente ...

LA LIMITACIÓN: ATENCIÓN SECUENCIAL (UNO A LA VEZ)
-------------------------------------------------
Como indica la advertencia de la Diapositiva 5:
  "Con este código básico el servidor atiende un cliente cada vez:
   si llega un segundo mientras el primero habla, se queda en la cola de listen().
   Para atender varios a la vez hacen falta hilos o select() (UD 06: Servidores concurrentes)."
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5005

def lanzar_clientes_secuenciales(cantidad=3):
    """Lanza N clientes con pausas breves entre sí."""
    time.sleep(0.3)
    for i in range(1, cantidad + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, PORT))
            mensaje = f"Hola, soy el Cliente #{i}"
            c.sendall(mensaje.encode("utf-8"))
            respuesta = c.recv(1024)
            print(f"    [Cliente #{i}] Respuesta del servidor: '{respuesta.decode()}'")
        time.sleep(0.2)

def main():
    print("=" * 70)
    print("  04 - EL BUCLE DE ATENCIÓN: ATENDER CLIENTES CON 'while True'")
    print("=" * 70)

    # Lanzamos el generador de clientes de prueba
    threading.Thread(target=lanzar_clientes_secuenciales, kwargs={"cantidad": 3}, daemon=True).start()

    print("\n[INICIANDO SERVIDOR CON BUCLE DE ATENCIÓN]:")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen(5)  # El número 5 es el 'backlog' (cola de espera del SO)
        print(f"Servidor escuchando en {HOST}:{PORT}. Esperando clientes...")

        clientes_atendidos = 0
        MAX_CLIENTES = 3  # Para que el script didáctico termine limpiamente tras 3 clientes

        while clientes_atendidos < MAX_CLIENTES:
            # 1. Espera al siguiente cliente (bloqueante)
            conexion, direccion = servidor.accept()
            clientes_atendidos += 1
            print(f"\n[Servidor] -> Atendiendo conexión #{clientes_atendidos} desde {direccion}")

            # 2. Atiende a este cliente en su socket propio
            with conexion:
                datos = conexion.recv(1024)
                print(f"[Servidor]    Datos recibidos: '{datos.decode()}'")
                
                # 3. Responde
                respuesta = b"Recibido: " + datos
                conexion.sendall(respuesta)
            
            print(f"[Servidor]    Llamada #{clientes_atendidos} finalizada con éxito.")

    print("\n" + "=" * 70)
    print("  RESUMEN PEDAGÓGICO:")
    print("  • 'while True' permite al servidor volver a accept() y esperar al próximo cliente.")
    print("  • Los clientes que llegan mientras se atiende a otro esperan en la cola de listen().")
    print("=" * 70)

if __name__ == "__main__":
    main()

