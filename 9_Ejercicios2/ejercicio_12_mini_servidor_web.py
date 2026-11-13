"""
=============================================================================
EJERCICIO 12: MINI SERVIDOR WEB HTTP CON SOCKETS TCP PUROS
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor TCP que escuche en 127.0.0.1:8080, acepte una conexión,
lea la petición (ignorándola) y responda con HTTP/1.1 200 OK y un HTML
con "<h1>Hola mundo</h1>".

💡 Pista: usa SO_REUSEADDR con setsockopt() para poder relanzar el
servidor sin esperar. Abre http://127.0.0.1:8080 en el navegador para verlo."

CONCEPTOS CLAVE:
1. La Web sobre Sockets:
   Todo servidor web (Apache, Nginx, uvicorn) es, en el fondo, un socket TCP
   que escucha en un puerto (80, 443, 8080) y habla el texto plano del protocolo HTTP.
2. Anatomía de la Respuesta HTTP/1.1:
   - Línea de estado:   HTTP/1.1 200 OK\\r\\n
   - Cabeceras:        Content-Type: text/html; charset=utf-8\\r\\n
                       Content-Length: <longitud>\\r\\n
                       Connection: close\\r\\n
   - Línea en blanco:  \\r\\n (CRLF obligatorio que separa cabeceras del cuerpo)
   - Cuerpo (Body):    <h1>Hola mundo</h1>
3. SO_REUSEADDR:
   Evita el error 'Address already in use' durante el estado TIME_WAIT del socket.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 8080
BUFFER_SIZE = 2048


def ejecutar_mini_servidor_web(host: str = HOST, puerto: int = PUERTO, una_sola_peticion: bool = False):
    """
    Ejecuta el mini servidor web artesanal con sockets TCP.
    
    :param host: Dirección IP (127.0.0.1).
    :param puerto: Puerto TCP (8080).
    :param una_sola_peticion: Si es True, atiende una petición y finaliza (modo demo/test).
    """
    print("=" * 70)
    print("        🌐 EJERCICIO 12: MINI SERVIDOR WEB HTTP ARTESANAL")
    print("=" * 70)
    print(f"[*] Configurando socket TCP en http://{host}:{puerto}/")

    # 1. Crear socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Pista: Usar SO_REUSEADDR con setsockopt() para relanzar sin esperar
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(5)
        print(f"[+] Servidor web escuchando en http://{host}:{puerto}")
        print("-" * 70)
        print(f"🌍 Abre tu navegador en: http://{host}:{puerto}")
        print(f"   O mediante curl:     curl -i http://{host}:{puerto}")
        print("-" * 70)

        contador = 0
        while True:
            print("[*] Esperando petición HTTP...")
            conn, addr = servidor_socket.accept()
            contador += 1
            print(f"\n[+] Petición #{contador} recibida desde {addr}!")

            with conn:
                # 3. Pista: Leer la petición entrante del navegador (e ignorarla)
                peticion_cruda = conn.recv(BUFFER_SIZE)
                if peticion_cruda:
                    linea_peticion = peticion_cruda.decode("utf-8", errors="replace").split("\r\n")[0]
                    print(f"📥 Línea de petición: \"{linea_peticion}\"")

                # 4. Construir cuerpo HTML solicitado
                cuerpo_html = "<h1>Hola mundo</h1>\n"
                cuerpo_bytes = cuerpo_html.encode("utf-8")

                # 5. Pista: Responder con HTTP/1.1 200 OK y las cabeceras HTTP necesarias
                respuesta_http = (
                    "HTTP/1.1 200 OK\r\n"
                    "Server: MiniServidorTCP-DAM/1.0\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(cuerpo_bytes)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                # 6. Enviar cabeceras + cuerpo HTML con sendall()
                paquete_completo = respuesta_http.encode("utf-8") + cuerpo_bytes
                conn.sendall(paquete_completo)
                print(f"📤 Respuesta HTTP 200 OK enviada ({len(paquete_completo)} bytes).")

            if una_sola_peticion:
                print("\n[i] Ejercicio 12 completado con éxito tras servir la página HTML.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor web detenido por el usuario.")
    finally:
        servidor_socket.close()
        print("[*] Socket del servidor web cerrado.")


def cliente_navegador_demo(puerto: int = PUERTO):
    """Cliente simulando una petición HTTP GET de navegador."""
    time.sleep(0.2)
    print("\n   [Navegador Simulado] Conectando a http://127.0.0.1:8080/...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            peticion = (
                "GET / HTTP/1.1\r\n"
                f"Host: {HOST}:{puerto}\r\n"
                "User-Agent: MiniNavegador/1.0\r\n"
                "Connection: close\r\n\r\n"
            )
            c.sendall(peticion.encode("ascii"))
            
            respuesta = b""
            while True:
                chunk = c.recv(1024)
                if not chunk:
                    break
                respuesta += chunk

            texto_resp = respuesta.decode("utf-8", errors="replace")
            print("   [Navegador Simulado] Respuesta recibida del servidor:")
            print("   " + "-" * 50)
            for linea in texto_resp.splitlines():
                print(f"   | {linea}")
            print("   " + "-" * 50)
            assert "<h1>Hola mundo</h1>" in texto_resp, "El HTML no contiene el encabezado esperado"
            print("   [Navegador Simulado] ✅ ¡Verificación web 100% exitosa!")
    except Exception as e:
        print(f"   [Navegador Simulado] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_navegador_demo, daemon=True)
        hilo.start()
        ejecutar_mini_servidor_web(una_sola_peticion=True)
        hilo.join(timeout=1.0)
    else:
        # Modo continuo para que el usuario pueda abrirlo en el navegador
        ejecutar_mini_servidor_web(una_sola_peticion=False)

