"""
01_anatomia_http_y_verbos.py
============================
Diapositivas de referencia:
  • Diapositiva 1 ("HTTP: el protocolo que mueve la web")
  • Diapositiva 2 ("Verbos y respuesta HTTP")

LA WEB SOBRE TCP:
-----------------
TCP y UDP son solo la "tubería" de transporte.
Los protocolos de aplicación (Capa 7) deciden QUÉ se escribe dentro de la tubería.
HTTP (HyperText Transfer Protocol) es un protocolo basado en TEXTO PLANO sobre TCP.

ANATOMÍA DE UNA PETICIÓN HTTP (Diapositiva 1):
----------------------------------------------
  GET /ruta HTTP/1.1\\r\\n          <- Línea de petición: Verbo, Recurso y Versión
  Host: ejemplo.com\\r\\n           <- Cabecera OBLIGATORIA en HTTP/1.1
  User-Agent: MiNavegador\\r\\n     <- Identificación del cliente
  Accept: text/html\\r\\n           <- Qué formato espera el cliente
  \\r\\n                            <- LÍNEA EN BLANCO: Marca el fin de las cabeceras

LOS 4 VERBOS PRINCIPALES (Diapositiva 2):
-----------------------------------------
  • GET:    Leer o consultar un recurso (sin enviar cuerpo).
  • POST:   Enviar datos nuevos al servidor (ej. formulario, login).
  • PUT:    Crear o reemplazar completamente un recurso.
  • DELETE: Eliminar un recurso del servidor.

ANATOMÍA DE UNA RESPUESTA HTTP (Diapositiva 2):
-----------------------------------------------
  HTTP/1.1 200 OK\\r\\n              <- Línea de estado: Código 200 (Éxito), 404 (No encontrado), 500 (Error)
  Content-Type: text/html\\r\\n      <- Tipo de contenido del cuerpo (HTML, JSON, texto)
  Content-Length: 1234\\r\\n         <- Tamaño exacto del cuerpo en bytes (para saber cuándo termina)
  \\r\\n                            <- Línea en blanco separadora
  <html>...cuerpo...</html>        <- Cuerpo con los datos reales
"""

def parsear_peticion_http_didactica(peticion_cruda_texto):
    """Desglosa una petición HTTP de texto para entender sus componentes."""
    lineas = peticion_cruda_texto.strip().split("\r\n")
    linea_peticion = lineas[0]
    partes = linea_peticion.split(" ")
    
    metodo = partes[0]
    ruta = partes[1]
    version = partes[2]

    cabeceras = {}
    for l in lineas[1:]:
        if ":" in l:
            clave, valor = l.split(":", 1)
            cabeceras[clave.strip()] = valor.strip()

    return metodo, ruta, version, cabeceras

def construir_respuesta_http(codigo, texto_estado, cuerpo_texto, tipo="text/html"):
    """Construye una respuesta HTTP estándar con formato estricto \\r\\n."""
    cuerpo_bytes = cuerpo_texto.encode("utf-8")
    cabeceras = (
        f"HTTP/1.1 {codigo} {texto_estado}\r\n"
        f"Content-Type: {tipo}; charset=utf-8\r\n"
        f"Content-Length: {len(cuerpo_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return cabeceras.encode("utf-8") + cuerpo_bytes

def main():
    print("=" * 70)
    print("  01 - ANATOMÍA DEL PROTOCOLO HTTP Y SUS VERBOS")
    print("=" * 70)

    # 1. Ejemplo de petición GET cruda
    peticion_ejemplo = (
        "GET /index.html HTTP/1.1\r\n"
        "Host: www.ejemplo.com\r\n"
        "User-Agent: Python-Sockets/1.0\r\n"
        "Accept: text/html\r\n"
        "\r\n"
    )

    print("\n[1] PETICIÓN HTTP CRUDA (Como viaja por el socket TCP):")
    for linea in peticion_ejemplo.split("\r\n"):
        print(f"    {repr(linea)}")

    metodo, ruta, version, cabeceras = parsear_peticion_http_didactica(peticion_ejemplo)
    print("\n[2] DESGLOSE PEDAGÓGICO:")
    print(f"    • Verbo / Método:        {metodo} (Pide leer un recurso)")
    print(f"    • Ruta / Recurso:        {ruta}")
    print(f"    • Versión del Protocolo: {version}")
    print(f"    • Cabecera 'Host:':      {cabeceras.get('Host')} (¡Obligatoria en HTTP/1.1!)")

    # 2. Construcción de una respuesta 200 OK
    print("\n[3] GENERACIÓN DE RESPUESTA HTTP 200 OK:")
    html = "<h1>¡Hola Mundo desde Sockets TCP!</h1><p>HTTP es texto plano.</p>"
    respuesta_bytes = construir_respuesta_http(200, "OK", html)

    print(f"    Bytes totales generados: {len(respuesta_bytes)}")
    print("    Texto de la respuesta:\n")
    for linea in respuesta_bytes.decode("utf-8").split("\r\n"):
        print(f"    | {linea}")

    print("\n" + "=" * 70)
    print("  DETALLES DE ORO:")
    print("  • La línea en blanco '\\r\\n\\r\\n' le dice al receptor: 'Terminaron las cabeceras'.")
    print("  • 'Content-Length' le dice exactamente cuántos bytes esperar en el cuerpo.")
    print("=" * 70)

if __name__ == "__main__":
    main()

