"""
06_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Servidor Web HTTP y Micro-API REST desde cero con Sockets TCP

ESCENARIO REAL:
---------------
Todo framework web moderno (como Flask, FastAPI, Django, Express o Spring Boot)
se ejecuta en última instancia sobre un bucle de sockets TCP recibiendo y parseando
texto HTTP línea a línea.

En este script creamos un SERVIDOR WEB HTTP REAL utilizando únicamente la librería
estándar de sockets, sin dependencias externas.

CAPACIDADES DEL SERVIDOR:
-------------------------
  1. Escucha peticiones HTTP reales (desde navegadores web, curl o scripts).
  2. Parsea la línea de petición: extrae el Verbo (GET, POST) y la Ruta (/ o /api/...).
  3. Detecta la línea en blanco '\\r\\n\\r\\n' que marca el fin de las cabeceras.
  4. Rutas implementadas:
     • GET /            -> Devuelve una página HTML visualmente atractiva (200 OK).
     • GET /api/hora    -> Devuelve la hora del servidor en JSON (200 OK).
     • Cualquier otra   -> Devuelve una respuesta 404 Not Found con mensaje descriptivo.
  5. Calcula automáticamente la cabecera obligatoria 'Content-Length'.

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático (ejecuta servidor y cliente de prueba con sockets):
      python3 06_ejemplo_vida_real.py

2. Modo servidor interactivo (puedes abrir http://localhost:8080 en tu navegador):
      python3 06_ejemplo_vida_real.py --servidor
"""

import json
import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PUERTO = 8080

def generar_respuesta_http(codigo, texto_estado, contenido, content_type="text/html"):
    """Construye una respuesta HTTP/1.1 válida con formato estricto \\r\\n."""
    cuerpo_bytes = contenido.encode("utf-8")
    cabeceras = (
        f"HTTP/1.1 {codigo} {texto_estado}\r\n"
        f"Content-Type: {content_type}; charset=utf-8\r\n"
        f"Content-Length: {len(cuerpo_bytes)}\r\n"
        f"Server: PythonSocketsWeb/1.0\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return cabeceras.encode("utf-8") + cuerpo_bytes

def ejecutar_servidor_web(limite_peticiones=None):
    """
    Servidor web HTTP basado en sockets TCP puros.
    """
    print("\n" + "=" * 65)
    print(f"  [SERVIDOR WEB HTTP] Escuchando en http://{HOST}:{PUERTO}")
    print("=" * 65)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(5)
        print("[SERVIDOR WEB] Listo para recibir navegadores o clientes HTTP...\n")

        peticiones_atendidas = 0

        while True:
            try:
                conexion, direccion_cliente = servidor.accept()
                peticiones_atendidas += 1

                with conexion:
                    # Leemos la petición HTTP cruda
                    peticion_bytes = conexion.recv(4096)
                    if not peticion_bytes:
                        continue

                    peticion_texto = peticion_bytes.decode("utf-8", errors="replace")
                    primera_linea = peticion_texto.split("\r\n")[0]
                    print(f"[SERVIDOR WEB] Petición #{peticiones_atendidas} desde {direccion_cliente}: '{primera_linea}'")

                    # Parsear método y ruta (ej. 'GET /api/hora HTTP/1.1')
                    partes = primera_linea.split(" ")
                    metodo = partes[0] if len(partes) > 0 else "GET"
                    ruta = partes[1] if len(partes) > 1 else "/"

                    # Enrutamiento básico
                    if ruta == "/":
                        html = (
                            "<!DOCTYPE html>"
                            "<html><head><meta charset='utf-8'><title>Servidor Sockets</title></head>"
                            "<body style='font-family:sans-serif; text-align:center; padding:50px; background:#f4f4f9;'>"
                            "<h1 style='color:#2c3e50;'>🚀 ¡Hola desde un Servidor Web Socket Puro!</h1>"
                            "<p>Esta página fue servida por un socket TCP usando el protocolo HTTP crudo.</p>"
                            "<p><a href='/api/hora'>Ver API JSON de Hora</a></p>"
                            "</body></html>"
                        )
                        respuesta = generar_respuesta_http(200, "OK", html, "text/html")

                    elif ruta == "/api/hora":
                        datos_json = json.dumps({
                            "mensaje": "Sincronización horaria vía API HTTP",
                            "timestamp_unix": int(time.time()),
                            "hora_servidor": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "OK"
                        }, indent=2)
                        respuesta = generar_respuesta_http(200, "OK", datos_json, "application/json")

                    else:
                        # 404 Not Found
                        html_404 = (
                            f"<h1>404 Not Found</h1>"
                            f"<p>La ruta solicitada '{ruta}' no existe en este servidor de sockets.</p>"
                        )
                        respuesta = generar_respuesta_http(404, "Not Found", html_404, "text/html")

                    # Enviar respuesta y cerrar socket
                    conexion.sendall(respuesta)

                if limite_peticiones and peticiones_atendidas >= limite_peticiones:
                    print(f"\n[SERVIDOR WEB] Límite de demostración alcanzado ({limite_peticiones} peticiones).")
                    break

            except Exception as e:
                print(f"[SERVIDOR WEB] Error: {e}")

    print("[SERVIDOR WEB] Servidor apagado.")

def cliente_peticion_manual(ruta="/"):
    """Cliente HTTP construido sobre sockets que realiza una petición GET."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        s.connect((HOST, PUERTO))
        peticion = (
            f"GET {ruta} HTTP/1.1\r\n"
            f"Host: {HOST}:{PUERTO}\r\n"
            f"User-Agent: ClienteSockets/1.0\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode("utf-8")
        s.sendall(peticion)

        respuesta = b""
        while True:
            datos = s.recv(2048)
            if not datos:
                break
            respuesta += datos
        return respuesta.decode("utf-8", errors="replace")

def modo_demostracion():
    """Ejecuta demostración automática con consultas a varias rutas."""
    print("=" * 70)
    print("  06 - EJEMPLO DE LA VIDA REAL: SERVIDOR WEB HTTP Y API REST")
    print("       (Demostración con consultas GET a rutas HTML y JSON)")
    print("=" * 70)

    # Iniciar servidor web en segundo plano para atender 3 peticiones
    hilo_srv = threading.Thread(
        target=ejecutar_servidor_web,
        kwargs={"limite_peticiones": 3},
        daemon=True
    )
    hilo_srv.start()
    time.sleep(0.3)

    # 1. Petición a la raíz (Página HTML)
    print("\n--- [Prueba 1] Consultando ruta raíz GET / ---")
    resp_html = cliente_peticion_manual("/")
    linea_estado = resp_html.split("\r\n")[0]
    print(f"  ✔ Respuesta recibida: {linea_estado}")

    # 2. Petición a la API JSON
    print("\n--- [Prueba 2] Consultando endpoint GET /api/hora ---")
    resp_api = cliente_peticion_manual("/api/hora")
    print("  ✔ Cabeceras y cuerpo JSON:")
    cuerpo_api = resp_api.split("\r\n\r\n")[1]
    print(cuerpo_api)

    # 3. Petición a una ruta inexistente (404)
    print("\n--- [Prueba 3] Consultando ruta inexistente GET /pagina_inexistente ---")
    resp_404 = cliente_peticion_manual("/pagina_inexistente")
    linea_estado_404 = resp_404.split("\r\n")[0]
    print(f"  ✔ Código esperado capturado: {linea_estado_404}")

    hilo_srv.join(timeout=2.0)

    print("\n" + "=" * 70)
    print("  RESUMEN PEDAGÓGICO:")
    print("  1. Todo servidor web es un servidor socket TCP escuchando en un puerto.")
    print("  2. Lee la petición de texto plano y extrae el Verbo y la Ruta.")
    print("  3. Devuelve cabeceras HTTP terminadas en '\\r\\n\\r\\n' y el cuerpo en bytes.")
    print("  4. Gestiona códigos 200 OK y 404 Not Found.")
    print("=" * 70)

if __name__ == "__main__":
    if "--servidor" in sys.argv:
        ejecutar_servidor_web(limite_peticiones=None)
    else:
        modo_demostracion()

