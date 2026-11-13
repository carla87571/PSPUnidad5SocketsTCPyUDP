"""
05_control_de_espera_nonblocking_y_select.py
============================================
Diapositiva de referencia: Diapositiva 7 ("Non-blocking y select: Tres formas de controlar la espera")

TRES FORMAS DE CONTROLAR LA ESPERA EN SOCKETS:
----------------------------------------------
Por defecto, los sockets en Python son BLOQUEANTES: una llamada a recv() o accept()
detiene el hilo por completo hasta que ocurra un evento.

La Diapositiva 7 presenta tres alternativas para controlar el bloqueo:

1. Opción 1: s.settimeout(5.0)
   -> Bloquea, pero como máximo durante 5 segundos. Si nadie responde, lanza socket.timeout.
   -> Es la opción más sencilla y recomendada para la mayoría de clientes.

2. Opción 2: s.setblocking(False)
   -> Modo no bloqueante puro: NUNCA se detiene a esperar.
   -> Si no hay datos disponibles en este instante exacto, lanza inmediatamente
      la excepción BlockingIOError.

3. Opción 3: select.select([sockets_lectura], [sockets_escritura], [errores], timeout)
   -> Es la herramienta más poderosa: permite supervisar DECENAS o CIENTOS de sockets
      simultáneamente sin consumir CPU y sin usar hilos (threading).
   -> El sistema operativo duerme al proceso y lo despierta en cuanto al menos uno
      de los sockets tiene datos listos para leer.
"""

import select
import socket
import threading
import time

HOST, PUERTO = "127.0.0.1", 5009

def servidor_eco_select():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PUERTO))
        srv.listen(1)
        conn, _ = srv.accept()
        with conn:
            time.sleep(0.5)  # Breve retardo antes de responder
            conn.sendall(b"Respuesta usando select")

def main():
    print("=" * 70)
    print("  05 - CONTROL DE ESPERAS: TIMEOUT, NON-BLOCKING Y select()")
    print("=" * 70)

    # 1. Opción 1: settimeout
    print("\n[OPCIÓN 1] s.settimeout(segundos) -> Timeout fijo:")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        s1.settimeout(1.0)
        print(f"    • Timeout configurado a: {s1.gettimeout()} segundos.")
        print("    • Si una operación tarda más de 1s, lanza socket.timeout.")

    # 2. Opción 2: setblocking(False) -> Modo no bloqueante
    print("\n[OPCIÓN 2] s.setblocking(False) -> Modo No Bloqueante:")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.bind(("127.0.0.1", 0))  # Puerto efímero
        s2.listen(1)
        s2.setblocking(False)  # No bloqueante
        print("    • Socket configurado en modo no bloqueante.")
        try:
            print("    • Intentando s2.accept() inmediatamente sin que nadie llame...")
            s2.accept()
        except BlockingIOError as e:
            print(f"    ✔ BlockingIOError capturado: '{e}'")
            print("       -> No esperó nada: avisó al instante de que no hay llamadas.")

    # 3. Opción 3: select.select() -> Multiplexación I/O
    print("\n[OPCIÓN 3] select.select() -> Supervisar múltiples sockets sin hilos:")
    threading.Thread(target=servidor_eco_select, daemon=True).start()
    time.sleep(0.1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
        s3.connect((HOST, PUERTO))

        print("    • Esperando con select.select() hasta 2.0 segundos...")
        # select vigila la lista de sockets de lectura: [s3]
        listos_para_leer, _, _ = select.select([s3], [], [], 2.0)

        if listos_para_leer:
            datos = s3.recv(1024)
            print(f"    ✔ Socket listo para lectura. Datos: '{datos.decode()}'")
        else:
            print("    ⏱ select terminó por tiempo (timeout): no hubo actividad.")

    print("\n" + "=" * 70)
    print("  CONCLUSIÓN PEDAGÓGICA:")
    print("  • settimeout:  Fácil para un socket individual.")
    print("  • select:      El estándar para gestionar muchos sockets a la vez (UD 06).")
    print("=" * 70)

if __name__ == "__main__":
    main()

