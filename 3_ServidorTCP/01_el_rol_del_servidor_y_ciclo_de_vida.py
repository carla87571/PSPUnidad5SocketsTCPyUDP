"""
01_el_rol_del_servidor_y_ciclo_de_vida.py
=========================================
Diapositivas de referencia:
  • Diapositiva 1 ("Servidor TCP: La idea en una frase")
  • Diapositiva 2 ("El ciclo de vida del servidor: Seis pasos: descolgar y atender")

LA IDEA EN UNA FRASE:
---------------------
"El servidor TCP descolgó primero: reserva un puerto con bind(),
 avisa con listen() y se queda esperando con accept() a que un cliente llame."

EL SERVIDOR EN LA ANALOGÍA DEL TELÉFONO:
----------------------------------------
El servidor es la empresa o recepcionista que espera llamadas:
  1. Compra una línea telefónica con un número y extensión pública -> bind()
  2. Activa el timbre para recibir llamadas -> listen()
  3. Espera a que suene el teléfono y dice "¿Diga?" -> accept()

¿POR QUÉ CADA PASO ES INDISPENSABLE?
------------------------------------
  • Sin bind():   El servidor no tiene puerto asignado; nadie sabe a qué extensión llamar.
  • Sin listen(): El sistema operativo no sabe que debe poner las llamadas entrantes en espera.
  • Sin accept(): El servidor nunca atiende al cliente que está llamando.

LOS 6 PASOS DEL CICLO DE VIDA (SIEMPRE EN ORDEN):
-------------------------------------------------
  1. socket()              -> Nace el socket del servidor.
  2. bind((HOST, PORT))    -> Reserva la dirección IP y el puerto.
  3. listen()              -> Anuncia que espera conexiones entrantes.
  4. accept()              -> El «¿diga?»: espera a que suene el timbre (bloqueante).
  5. recv() / sendall()    -> Hablar con el cliente conectado.
  6. close() / with        -> Cerrar la llamada y liberar recursos.
"""

import socket

def main():
    print("=" * 70)
    print("  01 - EL ROL DEL SERVIDOR TCP Y SU CICLO DE VIDA")
    print("=" * 70)

    # 1. Analogía del teléfono
    print("\n[1] EL SERVIDOR: EL QUE ESCUCHA Y ATIENDE:")
    print("    • Cliente:  Inicia la llamada activamente (connect).")
    print("    • Servidor: Descolgó primero y espera pacientemente (bind + listen + accept).")

    # 2. Los 6 pasos en orden
    print("\n[2] LOS 6 PASOS OBLIGATORIOS EN ORDEN:")
    print("    1. socket()    -> Crea el punto de entrada maestro.")
    print("    2. bind()      -> Fija la IP y el Puerto en el sistema operativo.")
    print("    3. listen()    -> Habilita la cola de llamadas entrantes.")
    print("    4. accept()    -> Atiende al cliente (¡BLOQUEANTE hasta que alguien llame!).")
    print("    5. recv/send   -> Conversación bidireccional de bytes.")
    print("    6. close()     -> Cuelga el teléfono.")

    # 3. Demostración en código de la preparación inicial (Pasos 1, 2 y 3)
    HOST = "127.0.0.1"
    PUERTO = 5003

    print(f"\n[3] DEMOSTRACIÓN DE PREPARACIÓN (Pasos 1 a 3):")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        # Buena práctica: permitir reutilizar la dirección sin esperar el TIME_WAIT
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Paso 2: bind()
        servidor.bind((HOST, PUERTO))
        print(f"    ✔ bind(({HOST}, {PUERTO})) ejecutado: Puerto reservado.")

        # Paso 3: listen()
        servidor.listen()
        print("    ✔ listen() ejecutado: Servidor en modo escucha activa.")
        print("    (Listo para recibir llamadas con accept()).")

    print("\n" + "=" * 70)
    print("  REGLA DE ORO: bind() reserva el puerto; listen() abre la escucha;")
    print("                accept() atiende la llamada concreta.")
    print("=" * 70)

if __name__ == "__main__":
    main()

