"""
02_ciclo_de_vida_y_cliente_minimo.py
====================================
Diapositivas de referencia:
  • Diapositiva 2 ("El ciclo de vida del cliente: Cuatro pasos, siempre en orden")
  • Diapositiva 3 ("El cliente TCP mínimo: Resuelto, de arriba a abajo")

LOS 4 PASOS DEL CICLO DE VIDA (SIEMPRE EN ORDEN):
-------------------------------------------------
  Paso 1: socket()               -> Crear el punto final de la conexión.
  Paso 2: connect((HOST, PORT))  -> Conectar: Dispara el Three-Way Handshake TCP (SYN, SYN-ACK, ACK).
  Paso 3: sendall() / recv()     -> Hablar: Enviar bytes con sendall() y recibir bytes con recv().
  Paso 4: close() / with         -> Cerrar: Desconectar y liberar los recursos.

EL CÓDIGO MÍNIMO EXACTO DE LA DIAPOSITIVA 3:
--------------------------------------------
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        cliente.sendall(b"Hola servidor!")
        respuesta = cliente.recv(1024)
        print(f"Respuesta: {respuesta.decode()}")
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5000

def mini_servidor_eco():
    """Servidor de apoyo que responde exactamente como en la diapositiva."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            datos = conn.recv(1024)
            # Responde 'Recibido: <mensaje>'
            conn.sendall(b"Recibido: " + datos)

def main():
    print("=" * 70)
    print("  02 - CICLO DE VIDA Y EL CLIENTE TCP MÍNIMO")
    print("=" * 70)

    # Iniciamos el servidor de soporte en segundo plano para que el cliente tenga con quién hablar
    t = threading.Thread(target=mini_servidor_eco, daemon=True)
    t.start()
    time.sleep(0.2)  # Pequeña pausa para asegurar que el servidor esté listo

    print("\n[EJECUTANDO EL CÓDIGO DE LA DIAPOSITIVA 3]:\n")

    # --- INICIO DEL CÓDIGO DE LA DIAPOSITIVA 3 ---
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        print("  Paso 1: socket() creado -> (IPv4, TCP)")
        
        cliente.connect((HOST, PORT))          # 1. conectar
        print(f"  Paso 2: connect(({HOST}, {PORT})) completado (Handshake OK)")

        cliente.sendall(b"Hola servidor!")     # 2. enviar (prefijo b indica bytes)
        print("  Paso 3a: sendall(b'Hola servidor!') enviado")

        respuesta = cliente.recv(1024)         # 3. recibir
        print(f"  Paso 3b: recv(1024) recibido")

        print(f"\n  👉 Respuesta: {respuesta.decode()}")
    
    print("\n  Paso 4: close() ejecutado automáticamente al salir del bloque 'with'")
    # --- FIN DEL CÓDIGO DE LA DIAPOSITIVA 3 ---

    print("\n" + "=" * 70)
    print("  DETALLES CLAVE APRENDIDOS:")
    print("  • b'Hola servidor!' -> El prefijo 'b' crea un objeto de tipo BYTES.")
    print("  • respuesta.decode() -> Convierte los BYTES recibidos a texto legible (str).")
    print("=" * 70)

if __name__ == "__main__":
    main()

