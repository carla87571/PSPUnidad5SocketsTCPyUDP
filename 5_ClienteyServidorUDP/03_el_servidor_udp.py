"""
03_el_servidor_udp.py
=====================
Diapositivas de referencia:
  • Diapositiva 4 ("El servidor UDP: bind() y recvfrom(): nada más")
  • Diapositiva 5 y 6 ("Sin accept(), sin listen(): Servidor TCP contra servidor UDP")

LA SIMPLICIDAD RADICAL DEL SERVIDOR UDP:
----------------------------------------
El servidor UDP sólo necesita dos métodos:
  1. bind((HOST, PORT)) -> Reserva el puerto en el SO. Todo datagrama dirigido
                           a ese puerto llegará a este socket.
  2. recvfrom(1024)     -> Se queda esperando (bloqueante) hasta que entra un datagrama.
                           Devuelve (datos_recibidos, direccion_del_emisor).

¿CÓMO RESPONDE EL SERVIDOR? ("Devolver la pelota"):
---------------------------------------------------
Como en UDP NO hay una conexión establecida que recuerde quién es el cliente,
la ÚNICA forma de responder es tomar la tupla 'direccion' que te entregó recvfrom()
y pasársela a sendto():
    servidor.sendto(b"Respuesta", direccion)

TABLA COMPARATIVA (Diapositiva 5):
----------------------------------
  ┌───────────────────────────────────┬───────────────────────────────────────┐
  │ SERVIDOR TCP                      │ SERVIDOR UDP                          │
  ├───────────────────────────────────┼───────────────────────────────────────┤
  │ bind()                            │ bind()                                │
  │ listen()                          │ — (No existe)                         │
  │ accept() -> devuelve 'conn'       │ — (No existe)                         │
  │ conn.recv(1024)                   │ servidor.recvfrom(1024)               │
  │ La conexión ya sabe quién es cli  │ recvfrom() te dice de quién viene     │
  └───────────────────────────────────┴───────────────────────────────────────┘

CONSECUENCIA ASOMBROSA:
-----------------------
¡Un solo socket servidor UDP puede atender a miles de clientes distintos
sin necesidad de accept() y sin crear hilos!
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5011

def simular_dos_clientes():
    """Lanza dos clientes independientes que envían datagramas al servidor UDP."""
    time.sleep(0.3)
    
    # Cliente 1 (ej. jugador en Madrid)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c1:
        c1.sendto(b"Ping desde Jugador 1", (HOST, PORT))
        resp1, _ = c1.recvfrom(1024)
        print(f"    [Cliente 1] Recibió: '{resp1.decode()}'")

    # Cliente 2 (ej. jugador en Bogotá)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c2:
        c2.sendto(b"Ping desde Jugador 2", (HOST, PORT))
        resp2, _ = c2.recvfrom(1024)
        print(f"    [Cliente 2] Recibió: '{resp2.decode()}'")

def main():
    print("=" * 70)
    print("  03 - EL SERVIDOR UDP: bind() Y recvfrom() (Sin accept ni listen)")
    print("=" * 70)

    # Lanzamos los clientes de prueba
    threading.Thread(target=simular_dos_clientes, daemon=True).start()

    # --- INICIO DEL CÓDIGO DEL SERVIDOR DE LA DIAPOSITIVA 4 ---
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        # 1. bind() para escuchar en el puerto
        servidor.bind((HOST, PORT))
        print(f"\n[SERVIDOR] Servidor UDP escuchando en {HOST}:{PORT}")

        # Atendemos 2 datagramas de dos clientes distintos usando el MISMO socket
        for i in range(1, 3):
            # 2. recvfrom() bloquea hasta recibir un datagrama
            datos, direccion = servidor.recvfrom(1024)
            print(f"\n[SERVIDOR] Datagrama #{i} recibido desde {direccion}:")
            print(f"           Mensaje: '{datos.decode()}'")

            # 3. Devolver la pelota con sendto() hacia la dirección recibida
            respuesta = b"Recibido OK!"
            servidor.sendto(respuesta, direccion)
            print(f"[SERVIDOR] Respuesta devuelta a {direccion}")
    # --- FIN DEL CÓDIGO DE LA DIAPOSITIVA 4 ---

    print("\n" + "=" * 70)
    print("  RESUMEN:")
    print("  En TCP necesitábamos un socket nuevo por cada cliente (accept).")
    print("  En UDP, el MISMO socket del servidor recibe y responde a todos.")
    print("=" * 70)

if __name__ == "__main__":
    main()

