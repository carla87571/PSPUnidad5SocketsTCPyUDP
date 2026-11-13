"""
02_servidor_tcp_minimo.py
=========================
Diapositiva de referencia: Diapositiva 3 ("El servidor TCP mínimo: Con el with cerrando solo")

EL CÓDIGO EXACTO DE LA DIAPOSITIVA 3:
-------------------------------------
Este archivo implementa el servidor TCP mínimo.
Nota cómo se anidan dos bloques 'with':
  1. with socket.socket(...) as servidor:
     -> Administra el socket maestro de escucha.
  2. with conexion:
     -> Administra el socket específico de la llamada recibida.
     -> Al salir del bloque, se cuelga automáticamente la llamada del cliente.
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5000

def cliente_automatico_de_prueba():
    """Simula un cliente que llama al servidor tras 0.3 segundos para probarlo."""
    time.sleep(0.3)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((HOST, PORT))
        cli.sendall(b"Hola servidor!")
        respuesta = cli.recv(1024)

def main():
    print("=" * 70)
    print("  02 - EL SERVIDOR TCP MÍNIMO (Diapositiva 3)")
    print("=" * 70)

    # Lanzamos el cliente de prueba en segundo plano para que el servidor reciba una llamada
    threading.Thread(target=cliente_automatico_de_prueba, daemon=True).start()

    print("\n[EJECUTANDO EL CÓDIGO DEL SERVIDOR DE LA DIAPOSITIVA 3]:\n")

    # --- CÓDIGO EXACTO DE LA DIAPOSITIVA 3 ---
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))          # 1. reservar puerto
        servidor.listen()                    # 2. anunciar escucha
        print(f"Servidor escuchando en {HOST}:{PORT}")
        
        conexion, direccion = servidor.accept() # 3. esperar cliente (BLOQUEANTE)
        print(f"Conectado con {direccion}")
        
        with conexion:
            datos = conexion.recv(1024)      # 4. recibir
            print(f"Recibido: {datos.decode()}")
            conexion.sendall(b"Recibido: " + datos) # 5. responder
    # --- FIN DEL CÓDIGO DE LA DIAPOSITIVA 3 ---

    print("\n" + "=" * 70)
    print("  OBSERVACIÓN CLAVE:")
    print("  1. 'servidor' abrió la puerta.")
    print("  2. 'accept()' devolvió un NUEVO socket llamado 'conexion'.")
    print("  3. La conversación (recv y sendall) se hizo exclusivamente por 'conexion'.")
    print("=" * 70)

if __name__ == "__main__":
    main()

