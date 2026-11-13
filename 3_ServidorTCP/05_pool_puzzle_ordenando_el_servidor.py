"""
05_pool_puzzle_ordenando_el_servidor.py
=======================================
Diapositiva de referencia: Diapositiva 6 ("Pool puzzle: ordena el servidor")

EL RETO DEL POOL PUZZLE:
------------------------
Imagina que te dan estas líneas de código mezcladas:

  a) with socket.socket() as srv:
  b)     srv.listen()
  c)     conn, addr = srv.accept()
  d) import socket
  e)         conn.sendall(b"Bienvenido\\n")
  f)     srv.bind(("127.0.0.1", 5000))
  g)     with conn:
  h)         datos = conn.recv(1024)

¿CUÁL ES EL ORDEN CORRECTO?
---------------------------
Solución: d ➔ a ➔ f ➔ b ➔ c ➔ g ➔ h ➔ e

LOS 3 ERRORES TÍPICOS DE LA DIAPOSITIVA 6:
------------------------------------------
  1. listen() antes de bind():
     • Si intentas hacer srv.bind() después de srv.listen(), el sistema operativo lanza:
       OSError: [Errno 22] Invalid argument (no puedes asignar puerto a un socket que ya escucha).
  2. accept() fuera del with de srv:
     • El socket maestro srv se cerraría antes de poder recibir llamadas.
  3. sendall() antes de recv():
     • No es el protocolo típico (en cliente-servidor tradicional, el cliente habla primero y el servidor responde).
"""

import socket

def demostracion_error_listen_antes_de_bind():
    """Muestra qué pasa si cometes el error típico de alterar el orden entre bind() y listen()."""
    print("\n[EXPERIMENTO: ¿Qué ocurre si invertimos el orden y llamamos listen() antes de bind()?]")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        try:
            print("  1. Ejecutando srv.listen()...")
            srv.listen()
            print("  2. Intentando ahora ejecutar srv.bind(('127.0.0.1', 5000))...")
            srv.bind(("127.0.0.1", 5000))
        except OSError as e:
            print(f"\n  ❌ ¡OSError capturado tal como enseña la Diapositiva 6!")
            print(f"     Tipo de error: {type(e).__name__}")
            print(f"     Detalle:       {e}")
            print("\n  💡 EXPLICACIÓN PEDAGÓGICA:")
            print("     El sistema operativo no permite cambiar o fijar el puerto (bind)")
            print("     una vez que el socket ya fue puesto en modo escucha (listen).")

def main():
    print("=" * 70)
    print("  05 - POOL PUZZLE: ORDENANDO EL SERVIDOR TCP")
    print("=" * 70)

    # 1. El puzzle
    print("\n[1] LÍNEAS DESORDENADAS:")
    print("    a) with socket.socket() as srv:")
    print("    b)     srv.listen()")
    print("    c)     conn, addr = srv.accept()")
    print("    d) import socket")
    print("    e)         conn.sendall(b'Bienvenido\\n')")
    print("    f)     srv.bind(('127.0.0.1', 5000))")
    print("    g)     with conn:")
    print("    h)         datos = conn.recv(1024)")

    # 2. Solución razonada
    print("\n[2] SOLUCIÓN PASO A PASO (d -> a -> f -> b -> c -> g -> h -> e):")
    print("    1. [d] import socket                     (Importar librería)")
    print("    2. [a] with socket.socket() as srv:      (Crear socket maestro)")
    print("    3. [f]     srv.bind(('127.0.0.1', 5000)) (Reservar puerto ANTES de escuchar)")
    print("    4. [b]     srv.listen()                  (Habilitar escucha)")
    print("    5. [c]     conn, addr = srv.accept()     (Esperar cliente)")
    print("    6. [g]     with conn:                    (Gestionar conexión privada)")
    print("    7. [h]         datos = conn.recv(1024)   (Recibir datos del cliente)")
    print("    8. [e]         conn.sendall(b'Bienvenido\\n') (Responder al cliente)")

    # 3. Demostración práctica de error
    demostracion_error_listen_antes_de_bind()

    print("\n" + "=" * 70)
    print("  ¡Lección aprendida! El orden en la programación de sockets es sagrado.")
    print("=" * 70)

if __name__ == "__main__":
    main()
