"""
02_practica_eco_cara_a_cara.py
==============================
Diapositivas de referencia:
  • Diapositiva 4 ("Práctica eco: La idea en una frase")
  • Diapositiva 5 ("Eco en TCP: puerto 9000")
  • Diapositiva 6 ("Eco en UDP: puerto 9001")
  • Diapositiva 7 ("Las dos versiones, cara a cara")

¿QUÉ ES UN SERVIDOR ECO?
------------------------
Un servidor eco es el 'Hola Mundo' de las redes: recibe bytes del cliente
y los devuelve idénticos sin modificarlos (como el eco en una cueva).

COMPARATIVA CARA A CARA (Diapositiva 7):
----------------------------------------
  ┌─────────────────────────┬────────────────────────────┬───────────────────────────────────────┐
  │ Característica          │ Eco TCP (Puerto 9000)      │ Eco UDP (Puerto 9001)                 │
  ├─────────────────────────┼────────────────────────────┼───────────────────────────────────────┤
  │ Preparación servidor    │ bind() + listen()          │ bind() (¡sin listen!)                 │
  │ Espera del servidor     │ accept() + recv()          │ recvfrom() (¡sin accept!)             │
  │ Devolución del eco      │ conn.sendall(datos)        │ servidor.sendto(datos, direccion)     │
  │ ¿Quién es el cliente?   │ La conexión ya lo sabe     │ recvfrom() te entrega la dirección   │
  │ ¿Atención de clientes?  │ Secuencial o con hilos     │ Cualquier cliente, en el mismo socket │
  └─────────────────────────┴────────────────────────────┴───────────────────────────────────────┘
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PUERTO_TCP = 9000
PUERTO_UDP = 9001

# --- 1. ECO EN TCP (Diapositiva 5) ---
def servidor_eco_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PUERTO_TCP))
        srv.listen(1)
        conn, addr = srv.accept()
        with conn:
            datos = conn.recv(1024)
            # El truco: devuelves exactamente los mismos bytes recibidos
            conn.sendall(datos)

def cliente_eco_tcp(mensaje):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((HOST, PUERTO_TCP))
        cli.sendall(mensaje.encode("utf-8"))
        eco = cli.recv(1024)
        return eco.decode("utf-8")


# --- 2. ECO EN UDP (Diapositiva 6) ---
def servidor_eco_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
        srv.bind((HOST, PUERTO_UDP))
        datos, direccion = srv.recvfrom(1024)
        # El truco: devuelves los mismos bytes a la dirección que te entregó recvfrom()
        srv.sendto(datos, direccion)

def cliente_eco_udp(mensaje):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cli:
        cli.sendto(mensaje.encode("utf-8"), (HOST, PUERTO_UDP))
        eco, _ = cli.recvfrom(1024)
        return eco.decode("utf-8")


def main():
    print("=" * 75)
    print("  02 - PRÁCTICA ECO: TCP VS UDP CARA A CARA")
    print("=" * 75)

    # 1. Prueba de Eco TCP (Puerto 9000)
    print("\n[PARTE 1] EJECUTANDO ECO EN TCP (Puerto 9000):")
    hilo_tcp = threading.Thread(target=servidor_eco_tcp, daemon=True)
    hilo_tcp.start()
    time.sleep(0.1)

    mensaje_tcp = "Prueba de Eco Fiable en TCP"
    print(f"  • Cliente TCP enviando:  '{mensaje_tcp}'")
    eco_recibido_tcp = cliente_eco_tcp(mensaje_tcp)
    print(f"  ✔ Servidor TCP devolvió: '{eco_recibido_tcp}'")
    hilo_tcp.join(timeout=1.0)

    # 2. Prueba de Eco UDP (Puerto 9001)
    print("\n[PARTE 2] EJECUTANDO ECO EN UDP (Puerto 9001):")
    hilo_udp = threading.Thread(target=servidor_eco_udp, daemon=True)
    hilo_udp.start()
    time.sleep(0.1)

    mensaje_udp = "Prueba de Eco Rápido en UDP"
    print(f"  • Cliente UDP enviando:  '{mensaje_udp}'")
    eco_recibido_udp = cliente_eco_udp(mensaje_udp)
    print(f"  ✔ Servidor UDP devolvió: '{eco_recibido_udp}'")
    hilo_udp.join(timeout=1.0)

    # 3. Resumen comparativo de la Diapositiva 7
    print("\n[PARTE 3] RESUMEN DE DIFERENCIAS CLAVE:")
    print("  • TCP: Usa accept() para crear 'conn' y conn.sendall() para devolver.")
    print("  • UDP: Usa recvfrom() para obtener la tupla (datos, direccion) y sendto(datos, direccion).")
    print("=" * 75)

if __name__ == "__main__":
    main()

