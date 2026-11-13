"""
05_simulador_entrevista_tecnica.py
==================================
Diapositiva de referencia: Diapositiva 13 ("Entrevista de trabajo: Las seis preguntas que te harán")

LAS 6 PREGUNTAS REINA DE ENTREVISTAS DE REDES Y BACKEND:
--------------------------------------------------------
Estas son las preguntas obligatorias que cualquier empresa o entrevistador senior
te hará para medir si realmente entiendes redes o solo usas librerías a ciegas.
"""

import sys
import time

PREGUNTAS_ENTREVISTA = [
    {
        "num": 1,
        "titulo": "¿Qué diferencia hay entre TCP y UDP? ¿Cuándo usarías cada uno?",
        "respuesta": (
            "• TCP (Orientado a conexión / Fiable): Garantiza entrega, orden y retransmisión\n"
            "  mediante un handshake previo de 3 vías. Lo uso cuando cada byte importa:\n"
            "  Web (HTTP), correos (SMTP), archivos (FTP), transacciones bancarias.\n"
            "• UDP (Sin conexión / Rápido): No garantiza entrega ni orden; lanza datagramas con mínimo retardo.\n"
            "  Lo uso cuando prima la latencia sobre la pérdida de algún paquete:\n"
            "  Streaming en directo, videojuegos online, DNS, telemetría IoT y NTP."
        )
    },
    {
        "num": 2,
        "titulo": "Escribe de memoria la estructura de un servidor TCP que reciba un mensaje y lo devuelva",
        "respuesta": (
            "Estructura en 6 pasos:\n"
            "  1. with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:\n"
            "  2.     srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n"
            "  3.     srv.bind(('127.0.0.1', 9000))\n"
            "  4.     srv.listen(5)\n"
            "  5.     conn, addr = srv.accept()\n"
            "  6.     with conn:\n"
            "             datos = conn.recv(1024)\n"
            "             conn.sendall(datos)  # Eco"
        )
    },
    {
        "num": 3,
        "titulo": "¿Cómo funciona el Three-Way Handshake? Explícalo conceptualmente",
        "respuesta": (
            "Se compone de 3 mensajes entre Cliente y Servidor:\n"
            "  1. SYN     (Cliente  -> Servidor): 'Quiero conectar contigo; mi seq inicial es X'.\n"
            "  2. SYN+ACK (Servidor -> Cliente):  'Acepto tu conexión (ACK=X+1); mi seq inicial es Y'.\n"
            "  3. ACK     (Cliente  -> Servidor): 'Recibido tu seq (ACK=Y+1). Conexión lista'.\n"
            "En Python, ocurre internamente durante la llamada a cliente.connect()."
        )
    },
    {
        "num": 4,
        "titulo": "¿Qué errores pueden ocurrir al comunicar por sockets y cómo los gestionas?",
        "respuesta": (
            "Se gestionan con bloques try/except específicos antes de caer en OSError:\n"
            "  • socket.timeout: Cuando recv o connect tardan más de settimeout().\n"
            "  • ConnectionRefusedError: Nadie escucha en el puerto remoto al llamar.\n"
            "  • ConnectionResetError: El servidor remoto cortó bruscamente la conexión.\n"
            "  • BrokenPipeError: Intentamos escribir (sendall) en un socket que ya colgó."
        )
    },
    {
        "num": 5,
        "titulo": "¿Qué es SO_REUSEADDR y cuándo lo necesitas?",
        "respuesta": (
            "Es una opción del socket configurada con setsockopt() antes del bind().\n"
            "Permite al sistema operativo reutilizar el puerto inmediatamente aunque queden\n"
            "conexiones previas en estado TIME_WAIT. Es fundamental en servidores para poder\n"
            "reiniciarlos de inmediato sin recibir 'OSError: Address already in use'."
        )
    },
    {
        "num": 6,
        "titulo": "¿Cómo funciona HTTP a nivel de socket? Describe una petición y una respuesta",
        "respuesta": (
            "HTTP es texto plano formateado sobre una conexión TCP (puerto 80 o 443 con TLS).\n"
            "• Petición: 'GET / HTTP/1.1\\r\\nHost: ejemplo.com\\r\\nConnection: close\\r\\n\\r\\n'\n"
            "• Respuesta: 'HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\nContent-Length: N\\r\\n\\r\\n<cuerpo>'\n"
            "La línea en blanco '\\r\\n\\r\\n' marca el fin de las cabeceras tanto al enviar como al recibir."
        )
    }
]

def main():
    print("=" * 75)
    print("  05 - SIMULADOR DE ENTREVISTA TÉCNICA: LAS SEIS PREGUNTAS CLAVE")
    print("  (Basado en la Diapositiva 13)")
    print("=" * 75)

    es_interactivo = "--interactivo" in sys.argv

    for item in PREGUNTAS_ENTREVISTA:
        print(f"\n[PREGUNTA {item['num']}]: {item['titulo']}")
        if es_interactivo:
            input("  👉 Presiona [ENTER] para consultar la respuesta modelo...")
        else:
            time.sleep(0.4)
            print("  💡 RESPUESTA ESPERADA:")
        
        for linea in item['respuesta'].split("\n"):
            print(f"     {linea}")
        print("-" * 65)

    print("\n" + "=" * 75)
    print("  ¡Si dominas estas 6 respuestas con fluidez, estás listo para cualquier")
    print("  entrevista técnica de desarrollo de software y backend!")
    print("=" * 75)

if __name__ == "__main__":
    main()

