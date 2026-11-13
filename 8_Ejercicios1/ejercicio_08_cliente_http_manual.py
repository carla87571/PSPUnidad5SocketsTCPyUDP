"""
=============================================================================
EJERCICIO 8: CLIENTE HTTP MANUAL CON SOCKET TCP
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Conéctate con un socket TCP a www.example.com:80, haz un GET a / y muestra
los primeros 500 caracteres de la respuesta.

💡 Pista: envía "GET / HTTP/1.1\\r\\nHost: www.example.com\\r\\nConnection: close\\r\\n\\r\\n"
con sendall(). Recibe en bucle con recv(4096) acumulando bytes hasta que
devuelva b"", y entonces decodifica."

CONCEPTOS CLAVE:
1. HTTP sobre TCP: HTTP es un protocolo de la Capa de Aplicación que viaja sobre
   un flujo de transporte TCP en el puerto 80 (HTTP estándar).
2. Formato de la petición HTTP/1.1:
   - Línea de petición: GET / HTTP/1.1\\r\\n
   - Cabecera Host (OBLIGATORIA en HTTP/1.1): Host: www.example.com\\r\\n
   - Cabecera de cierre: Connection: close\\r\\n
   - Fin de cabeceras: \\r\\n (línea en blanco imprescindible).
3. Lectura en bucle:
   Dado que TCP es un flujo continuo, recv(4096) no garantiza recibir toda la respuesta
   de golpe. Se acumulan los trozos hasta que el servidor cierra la conexión (devuelve b"").
=============================================================================
"""

import socket
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST_DESTINO = "www.example.com"
PUERTO_DESTINO = 80
RUTA = "/"


class ServidorLocalMock(BaseHTTPRequestHandler):
    """Servidor HTTP de respaldo para cuando no hay conexión a internet externa."""
    def do_GET(self):
        cuerpo = (
            "<!doctype html>\n"
            "<html>\n"
            "<head>\n"
            "    <title>Example Domain</title>\n"
            "    <meta charset=\"utf-8\" />\n"
            "    <meta http-equiv=\"Content-type\" content=\"text/html; charset=utf-8\" />\n"
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
            "</head>\n"
            "<body>\n"
            "<div>\n"
            "    <h1>Example Domain</h1>\n"
            "    <p>This domain is for use in illustrative examples in documents. You may use this\n"
            "    domain in literature without prior coordination or asking for permission.</p>\n"
            "    <p><a href=\"https://www.iana.org/domains/example\">More information...</a></p>\n"
            "</div>\n"
            "</body>\n"
            "</html>\n"
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, format, *args):
        # Silenciar logs internos del servidor mock
        pass


def ejecutar_cliente_http(host: str = HOST_DESTINO, puerto: int = PUERTO_DESTINO, host_header: str = HOST_DESTINO):
    """
    Ejecuta la petición HTTP manual con socket TCP puro.
    
    :param host: Dirección IP o nombre de dominio del servidor.
    :param puerto: Puerto TCP (habitualmente 80).
    :param host_header: Nombre del Host a incluir en la cabecera HTTP/1.1.
    """
    print("=" * 70)
    print("        🌐 EJERCICIO 8: CLIENTE HTTP MANUAL CON SOCKET TCP")
    print("=" * 70)
    print(f"[*] Conectando a {host}:{puerto}...")

    # 1. Crear el socket TCP (AF_INET, SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(6.0)

    try:
        # 2. Conectar al host y puerto
        sock.connect((host, puerto))
        print(f"[+] Conexión TCP establecida con éxito con {host}:{puerto}")

        # 3. Construir la petición HTTP/1.1 estricta
        # Nota pedagógica: Cada línea debe terminar en \r\n (CRLF)
        peticion = (
            f"GET {RUTA} HTTP/1.1\r\n"
            f"Host: {host_header}\r\n"
            f"Connection: close\r\n\r\n"
        )

        print("\n[>] Petición HTTP enviada:")
        print("-" * 40)
        print(peticion.strip())
        print("-" * 40)

        # Enviar petición completa con sendall()
        sock.sendall(peticion.encode("ascii"))

        # 4. Recibir en bucle con recv(4096) acumulando bytes hasta que devuelva b""
        print("[*] Recibiendo datos en trozos de hasta 4096 bytes...")
        respuesta_bytes = b""
        numero_trozos = 0

        while True:
            chunk = sock.recv(4096)
            if not chunk:  # b"" indica que el servidor cerró la conexión
                break
            respuesta_bytes += chunk
            numero_trozos += 1

        print(f"[+] Recepción completada: {len(respuesta_bytes)} bytes recibidos en {numero_trozos} lectura(s).")

        # 5. Decodificar la respuesta
        respuesta_texto = respuesta_bytes.decode("utf-8", errors="replace")

        # 6. Mostrar los primeros 500 caracteres tal y como pide el enunciado
        print("\n" + "=" * 70)
        print("📄 PRIMEROS 500 CARACTERES DE LA RESPUESTA HTTP RECIBIDA:")
        print("=" * 70)
        primeros_500 = respuesta_texto[:500]
        print(primeros_500)
        print("=" * 70)
        print(f"ℹ️ (Longitud del extracto mostrado: {len(primeros_500)} caracteres)")

    finally:
        # Cerrar el socket
        sock.close()
        print("[*] Socket cerrado correctamente.")


def ejecutar_con_respaldo():
    """
    Intenta conectar a www.example.com:80 en internet real.
    Si el entorno está aislado o sin internet, levanta un servidor HTTP local
    de respaldo para que el ejercicio funcione de forma didáctica y garantizada.
    """
    try:
        # Intentar resolución DNS y conexión real
        ejecutar_cliente_http(HOST_DESTINO, PUERTO_DESTINO, HOST_DESTINO)
    except (socket.gaierror, socket.timeout, OSError) as err:
        print(f"\n[ℹ️ Aviso de Red]: No hay conexión a internet externa ({err}).")
        print("[*] Activando servidor HTTP local de respaldo para demostrar el funcionamiento del socket...")

        puerto_local = 8088
        httpd = HTTPServer(("127.0.0.1", puerto_local), ServidorLocalMock)
        hilo_servidor = threading.Thread(target=httpd.handle_request, daemon=True)
        hilo_servidor.start()

        # Ejecutamos el cliente conectándolo al servidor local pero enviando el Host de example.com
        ejecutar_cliente_http("127.0.0.1", puerto_local, "www.example.com")


if __name__ == "__main__":
    ejecutar_con_respaldo()

