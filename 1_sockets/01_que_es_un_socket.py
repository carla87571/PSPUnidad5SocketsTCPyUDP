"""
01_que_es_un_socket.py
======================
Diapositiva de referencia: Diapositiva 2 ("Qué es un socket: La idea en una frase")

¿QUÉ ES UN SOCKET?
------------------
Un socket es el punto final (endpoint) de una conexión de red:
es la interfaz que tu programa usa para enviar y recibir datos a través de la red.

LA ANALOGÍA DE LA LLAMADA TELEFÓNICA:
-------------------------------------
Imagina que vas a hacer una llamada a una oficina:
  1. Tu teléfono físico  --> Es el SOCKET (el dispositivo que te permite hablar y escuchar).
  2. El número de teléfono --> Es la IP (identifica a qué edificio o máquina llamas).
  3. La extensión interna --> Es el PUERTO (identifica con qué departamento o programa quieres hablar).

Sin este trío (Socket + IP + Puerto) NO hay conversación posible.
"""

import socket

def main():
    print("=" * 60)
    print("  01 - ¿QUÉ ES UN SOCKET? (Conceptos fundamentales)")
    print("=" * 60)

    # 1. Analogía didáctica en consola
    print("\n[1] ANALOGÍA DEL TELÉFONO:")
    print("    • Teléfono  = SOCKET (la herramienta para transmitir datos)")
    print("    • Número    = DIRECCIÓN IP (ejemplo: 127.0.0.1)")
    print("    • Extensión = NÚMERO DE PUERTO (ejemplo: 5000)")

    # 2. Creación del objeto Socket en Python
    print("\n[2] CREANDO NUESTRO PRIMER SOCKET EN PYTHON:")
    # socket.socket() crea el "teléfono" en nuestro sistema operativo
    mi_primer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"    -> Objeto creado: {mi_primer_socket}")
    print(f"    -> Descriptor de archivo (fileno): {mi_primer_socket.fileno()}")
    print("       (El sistema operativo le asigna un número identificador interno)")

    # 3. ¿Cómo hablará el socket?
    print("\n[3] ¿CÓMO HABLA EL SOCKET?")
    print("    Dependiendo del protocolo elegido:")
    print("    • TCP: Como una 'carta certificada' (segura, confirmada, ordenada).")
    print("    • UDP: Como un 'avión de papel' (rápido, sin esperar confirmación).")

    # 4. Buena práctica: SIEMPRE cerrar el socket al terminar
    mi_primer_socket.close()
    print("\n[4] Socket cerrado correctamente con .close(). ¡Recursos liberados!")
    print("=" * 60)

if __name__ == "__main__":
    main()

