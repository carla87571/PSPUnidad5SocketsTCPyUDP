"""
01_el_rol_del_cliente.py
========================
Diapositiva de referencia: Diapositiva 1 ("Cliente TCP: La idea en una frase")

LA IDEA EN UNA FRASE:
---------------------
"El cliente TCP marca el número: crea el socket, se conecta con connect(),
envía con sendall(), recibe con recv() y cierra."

¿QUIÉN ES EL CLIENTE?
---------------------
En la arquitectura Cliente-Servidor:
  • El CLIENTE es el lado que INICIA la conversación (toma la iniciativa).
  • En la analogía del teléfono, eres tú descolgando, marcando el número y esperando a que contesten.
  • Sin un cliente que llame, el servidor se quedaría esperando pasivamente en su puerto para siempre.

¿QUÉ OCURRE SI LLAMAS Y NO HAY NADIE?
-------------------------------------
Si intentas conectar con un puerto donde no hay ningún programa escuchando,
el sistema operativo rechaza la conexión y Python lanza la excepción:
    ConnectionRefusedError: [Errno 111] Connection refused
"""

import socket

def main():
    print("=" * 70)
    print("  01 - EL ROL DEL CLIENTE TCP (Quien inicia la conversación)")
    print("=" * 70)

    # 1. Analogía didáctica
    print("\n[1] EL CLIENTE EN LA ANALOGÍA DEL TELÉFONO:")
    print("    • El Servidor: Espera pacientemente junto al teléfono.")
    print("    • El Cliente:  Descuelga, marca el número y dice '¡Hola!'.")
    print("    • Conclusión:  El cliente siempre da el primer paso.")

    # 2. Intentando conectar a un puerto sin servidor
    HOST = "127.0.0.1"
    PUERTO_INEXISTENTE = 59999

    print(f"\n[2] EXPERIMENTO: ¿Qué pasa si llamamos al puerto {PUERTO_INEXISTENTE} y nadie contesta?")
    print("    Intentando: cliente.connect(('127.0.0.1', 59999))...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PUERTO_INEXISTENTE))
            print("    -> Conexión establecida (inesperado).")
        except ConnectionRefusedError as e:
            print("\n    ❌ ¡ERROR CAPTURADO!")
            print(f"    Tipo de excepción: {type(e).__name__}")
            print(f"    Mensaje del SO:    {e}")
            print("\n    💡 EXPLICACIÓN PEDAGÓGICA:")
            print("       'ConnectionRefusedError' significa que la máquina existe (127.0.0.1),")
            print("       pero ningún programa está haciendo listen() en el puerto 59999.")

    print("\n" + "=" * 70)
    print("  REGLA CLAVE: Un cliente siempre debe manejar 'ConnectionRefusedError'.")
    print("=" * 70)

if __name__ == "__main__":
    main()

