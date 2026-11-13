"""
04_el_bloqueo_y_timeouts.py
===========================
Diapositiva de referencia: Diapositiva 5 ("Be the code: el cliente, paso a paso")

EL COMPORTAMIENTO BLOQUEANTE DE recv():
--------------------------------------
En la Diapositiva 5 vimos:
  "recv() se queda esperando hasta que lleguen datos: si el servidor nunca responde,
   el programa queda colgado. La salida de emergencia son los timeouts."

¿QUÉ SIGNIFICA QUE UN MÉTODO SEA 'BLOQUEANTE'?
----------------------------------------------
Significa que el hilo de ejecución de Python se detiene por completo en esa línea.
No avanzará a la siguiente instrucción hasta que:
  a) Lleguen datos del servidor.
  b) El servidor cierre la conexión limpiamente (recv devuelve b'').
  c) Ocurra un error en la conexión.

¿CUÁL ES EL PELIGRO?
--------------------
Si el servidor remoto se cuelga, pierde conexión o tiene un bug y nunca responde,
¡tu programa cliente se quedará congelado para siempre!

LA SOLUCIÓN: socket.settimeout(segundos)
----------------------------------------
Le dice al socket: "Si pasan N segundos sin que nadie hable, interrumpe la espera
y lanza la excepción TimeoutError (o socket.timeout)".
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5002

def servidor_silencioso():
    """Servidor que acepta la conexión pero NUNCA responde (simula un servidor colgado)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            conn.recv(1024)  # Lee la petición pero no envía nada de vuelta
            time.sleep(4.0)  # Se queda mudo

def main():
    print("=" * 70)
    print("  04 - COMPORTAMIENTO BLOQUEANTE Y LA SALIDA DE EMERGENCIA: TIMEOUTS")
    print("=" * 70)

    # Iniciamos el servidor que se queda mudo
    t = threading.Thread(target=servidor_silencioso, daemon=True)
    t.start()
    time.sleep(0.2)

    print("\n[1] EL PROBLEMA:")
    print("    Si llamáramos a cliente.recv(1024) sin timeout, el script esperaría")
    print("    indefinidamente porque el servidor no responde.")

    print("\n[2] LA SALIDA DE EMERGENCIA:")
    print("    Configuramos un timeout de 2.0 segundos:")
    print("    Código: cliente.settimeout(2.0)")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        # Configuramos el tiempo máximo de espera
        cliente.settimeout(2.0)

        cliente.connect((HOST, PORT))
        cliente.sendall(b"Hola? Hay alguien ahi?")
        print("\n    ⏳ Petición enviada. Esperando respuesta (máximo 2 segundos)...")

        tiempo_inicio = time.time()
        try:
            # Aquí recv() intentará leer, pero el servidor no contestará
            respuesta = cliente.recv(1024)
            print(f"    Respuesta: {respuesta.decode()}")
        except TimeoutError:
            tiempo_transcurrido = time.time() - tiempo_inicio
            print(f"\n    ⏱ ¡TIMEOUT ACTIVADO tras {tiempo_transcurrido:.2f} segundos!")
            print("    Excepción capturada: TimeoutError")
            print("    ✔ El programa NO se quedó congelado. Podemos avisar al usuario o reintentar.")

    print("\n" + "=" * 70)
    print("  BUENA PRÁCTICA PROFESIONAL:")
    print("  Todo cliente TCP en producción debe definir siempre un timeout razonable.")
    print("=" * 70)

if __name__ == "__main__":
    main()

