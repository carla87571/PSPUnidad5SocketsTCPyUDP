"""
01_la_filosofia_udp.py
======================
Diapositivas de referencia:
  • Diapositiva 1 ("Cliente y servidor UDP: La idea en una frase")
  • Diapositiva 3 ("Sendto contra send: La diferencia visual con TCP")

LA FILOSOFÍA DE LOS AVIONES DE PAPEL:
-------------------------------------
"UDP no se conecta: el cliente manda un datagrama con sendto() y espera
 con recvfrom(); el servidor solo hace bind() y escucha.
 Sin connect(), sin accept(), sin listen()... y sin garantía de que el mensaje llegue."

DIFERENCIA VISUAL CON TCP (Diapositiva 3):
------------------------------------------
  ┌─────────────────────────────────┬─────────────────────────────────────────┐
  │ CLIENTE TCP                     │ CLIENTE UDP                             │
  ├─────────────────────────────────┼─────────────────────────────────────────┤
  │ s.connect((HOST, PORT))         │ — (¡No existe! No hay conexión previa)  │
  │ s.sendall(datos)                │ s.sendto(datos, (HOST, PORT))           │
  │ s.recv(1024)                    │ s.recvfrom(1024)                        │
  └─────────────────────────────────┴─────────────────────────────────────────┘

EN TCP:  Primero te conectas (handshake) y luego envías por ese canal.
EN UDP:  El «a quién» (HOST, PORT) viaja DENTRO de cada llamada a sendto().

EL PELIGRO DEL SILENCIO EN UDP:
-------------------------------
Si lanzas un avión de papel (sendto) hacia una casa vacía (sin servidor),
¡el sistema operativo NO lanza ningún error al enviar! El datagrama simplemente se esfuma.
Pero si luego llamas a recvfrom(), el cliente esperará eternamente a menos que uses settimeout().
"""

import socket
import time

def main():
    print("=" * 70)
    print("  01 - LA FILOSOFÍA DE UDP: SIN CONEXIÓN, SIN LISTEN, SIN ACCEPT")
    print("=" * 70)

    # 1. Analogía y diferencias
    print("\n[1] LAS TRES AUSENCIAS DE UDP:")
    print("    • Sin connect() -> No hay saludo previo (Three-Way Handshake).")
    print("    • Sin listen()  -> El servidor no mantiene colas de conexión.")
    print("    • Sin accept()  -> No se crean sockets nuevos por cada cliente.")

    # 2. Experimento: Enviar por UDP a un puerto donde nadie escucha
    HOST = "127.0.0.1"
    PUERTO_SIN_SERVIDOR = 59998

    print(f"\n[2] EXPERIMENTO: Lanzar un datagrama al puerto {PUERTO_SIN_SERVIDOR} (sin servidor)")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        # Configuramos un timeout breve para no quedarnos congelados esperando
        cliente.settimeout(1.0)

        # 1. sendto() no falla aunque no haya servidor
        mensaje = b"Hola al vacio!"
        bytes_enviados = cliente.sendto(mensaje, (HOST, PUERTO_SIN_SERVIDOR))
        print(f"    ✔ sendto() envió {bytes_enviados} bytes sin ningún error.")
        print("       (En TCP, connect() habría lanzado ConnectionRefusedError de inmediato).")

        # 2. recvfrom() intentará esperar una respuesta que nunca llegará
        print("    • Esperando respuesta con recvfrom(1024)...")
        try:
            datos, remitente = cliente.recvfrom(1024)
            print(f"    Respuesta: {datos}")
        except TimeoutError:
            print("\n    ⏱ ¡TimeoutError capturado!")
            print("    💡 EXPLICACIÓN PEDAGÓGICA:")
            print("       En UDP, como nadie te avisa si el paquete llegó o se perdió,")
            print("       SIEMPRE debes proteger tus llamadas con settimeout().")

    print("\n" + "=" * 70)
    print("  REGLA DE ORO: sendto() lanza el avión; recvfrom() atrapa la respuesta.")
    print("=" * 70)

if __name__ == "__main__":
    main()

