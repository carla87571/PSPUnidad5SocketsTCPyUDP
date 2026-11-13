"""
04_se_el_socket_y_quien_soy.py
==============================
Diapositivas de referencia:
  • Diapositiva 11 ("Sé el socket: Consolida lo aprendido")
  • Diapositiva 12 ("¿Quién soy? Adivina el concepto")

PARTE 1: SÉ EL SOCKET (La historia en primera persona):
-------------------------------------------------------
  Paso 1: Haces bind(("127.0.0.1", 9000)) -> Reservas el puerto. Ya eres la centralita.
  Paso 2: Haces listen() -> El SO ya sabe que esperas llamadas. Te quedas en accept() durmiendo.
  Paso 3: Un cliente hace connect() -> El handshake (SYN ➔ SYN+ACK ➔ ACK) suena como el timbre.
          accept() despierta y crea un NUEVO socket privado para esa llamada.
  Paso 4: Haces recv(1024) -> Esperas otra vez. Cuando el cliente manda datos, despiertas y
          respondes con sendall().
  Paso 5: Al salir del with -> La despedida FIN/ACK cuelga la llamada... y tú vuelves a accept()
          a esperar al siguiente.
  ¿Y si otro cliente llama mientras estás ocupado?
  Queda en la cola de listen() (el backlog). Por eso un solo hilo atiende de uno en uno.

PARTE 2: JUEGO DIDÁCTICO "¿QUIÉN SOY?":
---------------------------------------
10 adivinanzas conceptuales de la Diapositiva 12.
"""

import sys
import time

ADIVINANZAS = [
    ("Soy el punto final de una conexión de red", "El socket"),
    ("Soy el método del cliente TCP que estrecha la mano antes de hablar", "connect()"),
    ("Soy el método del servidor UDP que dice de quién vienen los datagramas", "recvfrom()"),
    ("Soy el estado que retiene el puerto tras cerrar", "TIME_WAIT"),
    ("Soy la opción que evita el 'Address already in use'", "SO_REUSEADDR"),
    ("Soy el protocolo de texto sobre TCP que mueve la web", "HTTP"),
    ("Soy el grupo de servidores de tiempo del puerto 123", "pool.ntp.org (NTP)"),
    ("Soy el protocolo fiable sobre UDP de HTTP/3", "QUIC"),
    ("Soy la llamada que espera en varios sockets a la vez sin hilos", "select()"),
    ("Soy la tupla que devuelve recvfrom()", "(datos, direccion)")
]

def main():
    print("=" * 75)
    print("  04 - SÉ EL SOCKET Y JUEGO '¿QUIÉN SOY?'")
    print("=" * 75)

    # 1. Narrativa pedagógica de la Diapositiva 11
    print("\n[PARTE 1] SÉ EL SOCKET (El ciclo mental):")
    print("  1. bind()     -> Compras el número. Te conviertes en la centralita.")
    print("  2. listen()   -> Enciendes el timbre.")
    print("  3. accept()   -> Suena el teléfono (Handshake). Despiertas y abres sala privada.")
    print("  4. recv/send  -> Conversas por el canal privado.")
    print("  5. with/close -> Cuelgas (FIN/ACK) y vuelves a accept() a esperar al próximo.")

    # 2. Juego "¿Quién soy?" (Diapositiva 12)
    print("\n[PARTE 2] JUEGO CONCEPTUAL: '¿QUIÉN SOY?' (Diapositiva 12):")
    es_interactivo = "--interactivo" in sys.argv

    for i, (pista, solucion) in enumerate(ADIVINANZAS, 1):
        print(f"\n  Pista {i:02d}: \"{pista}\"")
        if es_interactivo:
            input("           👉 Presiona [ENTER] para revelar la respuesta...")
        else:
            time.sleep(0.3)
        print(f"           ✔ Soy: {solucion}")

    print("\n" + "=" * 75)
    print("  ¡Excelente repaso! Has consolidado todo el vocabulario técnico.")
    print("=" * 75)

if __name__ == "__main__":
    main()

