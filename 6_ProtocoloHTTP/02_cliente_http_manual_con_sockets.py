"""
02_cliente_http_manual_con_sockets.py
=====================================
Diapositiva de referencia: Diapositiva 3 ("El cliente HTTP manual")

EL CÓDIGO EXACTO DE LA DIAPOSITIVA 3:
-------------------------------------
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("www.example.com", 80))
        s.sendall(b"GET / HTTP/1.1\\r\\nHost: www.example.com\\r\\n"
                  b"Connection: close\\r\\n\\r\\n")
        respuesta = b""
        while True:
            datos = s.recv(4096)
            if not datos:
                break
            respuesta += datos
    print(respuesta.decode()[:500])

LOS DOS DETALLES CLAVE DE LA DIAPOSITIVA 3:
-------------------------------------------
  1. 'Connection: close':
     -> Por defecto, HTTP/1.1 mantiene la conexión abierta ("keep-alive") para reutilizarla.
     -> Enviar 'Connection: close' le ordena al servidor: "En cuanto termines de mandarme
        el documento, cierra el socket con FIN/ACK".
  2. Bucle 'while True' de lectura:
     -> Una página web puede medir cientos de kilobytes.
     -> La respuesta llega en trozos (chunks). El bucle acumula los bytes hasta que
        s.recv() devuelve b'' (lo que significa que el servidor cerró el socket).
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PUERTO = 8080

def mini_servidor_web_local():
    """Servidor web de apoyo local para garantizar que la prueba funcione siempre sin requerir internet."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PUERTO))
        srv.listen(1)
        conn, _ = srv.accept()
        with conn:
            peticion = conn.recv(1024)
            cuerpo = "<html><body><h1>Example Domain</h1><p>Esta es una respuesta HTTP simulada para pruebas locales.</p></body></html>"
            respuesta = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(cuerpo.encode())}\r\n"
                "Connection: close\r\n"
                "\r\n" + cuerpo
            )
            conn.sendall(respuesta.encode("utf-8"))

def ejecutar_cliente_http(host, puerto, nombre_host):
    """Ejecuta el cliente HTTP manual de la Diapositiva 3."""
    print(f"\n[CLIENTE HTTP] Conectando a ({host}:{puerto})...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3.0)
        s.connect((host, puerto))

        # 1. Enviar la petición HTTP en bytes
        peticion = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {nombre_host}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode("utf-8")

        print("  -> Petición HTTP enviada con cabecera 'Connection: close'.")
        s.sendall(peticion)

        # 2. Bucle para acumular todos los fragmentos
        respuesta = b""
        numero_trozos = 0
        while True:
            datos = s.recv(4096)
            if not datos:
                # recv() devuelve b'' cuando el servidor cierra el socket al terminar
                break
            respuesta += datos
            numero_trozos += 1

        print(f"  -> Respuesta recibida en {numero_trozos} fragmento(s). Total: {len(respuesta)} bytes.")
        return respuesta.decode("utf-8", errors="replace")

def main():
    print("=" * 70)
    print("  02 - EL CLIENTE HTTP MANUAL CON SOCKETS TCP (Diapositiva 3)")
    print("=" * 70)

    # Iniciamos el servidor web local para pruebas autónomas
    threading.Thread(target=mini_servidor_web_local, daemon=True).start()
    time.sleep(0.2)

    # Ejecutamos el cliente manual
    salida = ejecutar_cliente_http(HOST, PUERTO, "localhost")

    print("\n[RESULTADO RECIBIDO POR EL SOCKET TCP (Primeros 500 caracteres)]:\n")
    print("-" * 60)
    print(salida[:500])
    print("-" * 60)

    print("\n" + "=" * 70)
    print("  ¡Felicidades! Acabas de recrear lo que hace tu navegador web por dentro:")
    print("  Abre un socket TCP en el puerto 80, escribe texto HTTP y lee hasta b''.")
    print("=" * 70)

if __name__ == "__main__":
    main()

