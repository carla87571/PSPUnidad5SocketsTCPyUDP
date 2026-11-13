"""
=============================================================================
EJERCICIO 4: TEORÍA DE IP Y PUERTO (PREGUNTAS Y RESPUESTAS)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Responde por escrito:
 1. ¿Qué identifica la IP y qué identifica el puerto en una comunicación de red?
 2. ¿Qué significa 127.0.0.1 y para qué se usa?
 3. ¿Qué constante de Python crea un socket TCP y cuál un socket UDP?
 
 💡 Pista: repasa el punto 1 de la unidad: la IP identifica la máquina, el puerto
    identifica el programa; 127.0.0.1 es localhost; y los tipos de socket son
    SOCK_STREAM (TCP) y SOCK_DGRAM (UDP)."
=============================================================================
"""

import socket
import sys

RESPUESTAS = {
    "pregunta_1": {
        "titulo": "1. ¿Qué identifica la IP y qué identifica el puerto en una comunicación de red?",
        "respuesta_corta": "La dirección IP identifica la MÁQUINA (host/dispositivo), mientras que el PUERTO identifica el PROGRAMA o SERVICIO (proceso específico dentro de esa máquina).",
        "explicacion_detallada": (
            "• Dirección IP (Internet Protocol):\n"
            "  - Es una etiqueta numérica asignada a cada interfaz de red conectada a la red (ej. 192.168.1.45 o 142.250.200.46).\n"
            "  - Su función es direccionar los paquetes a nivel de Capa de Red (Capa 3 de OSI / Capa Internet de TCP/IP),\n"
            "    llevando los datos de un host origen a un host destino en el mundo.\n\n"
            "• Puerto (Port Number):\n"
            "  - Es un número entero de 16 bits (rango: 0 a 65535) en la Capa de Transporte (Capa 4 OSI).\n"
            "  - Su función es la multiplexación: permite que múltiples programas utilicen la misma conexión de red simultáneamente.\n"
            "  - Por ejemplo, un mismo servidor puede ejecutar un servidor Web (puerto 80), un servidor seguro HTTPS (puerto 443)\n"
            "    y un servidor SSH (puerto 22). Gracias al número de puerto, el sistema operativo sabe a qué proceso entregar los datos.\n\n"
            "🏢 ANALOGÍA DE LA VIDA REAL:\n"
            "  - Dirección IP = La dirección postal de un gran edificio de apartamentos (Calle Mayor, 10).\n"
            "  - Puerto       = El número de apartamento o buzón específico dentro del edificio (Puerta 4B)."
        )
    },
    "pregunta_2": {
        "titulo": "2. ¿Qué significa 127.0.0.1 y para qué se usa?",
        "respuesta_corta": "127.0.0.1 es la dirección IP de bucle invertido (loopback), conocida universalmente como 'localhost'.",
        "explicacion_detallada": (
            "• ¿Qué significa?:\n"
            "  - Pertenece al rango reservado 127.0.0.0/8 por el estándar de direccionamiento IPv4 (RFC 1122).\n"
            "  - Apunta directamente a la propia máquina local en la que se está ejecutando el código.\n\n"
            "• ¿Para qué se usa?:\n"
            "  1. Pruebas y Desarrollo Local: Permite probar clientes y servidores en la misma máquina sin necesidad\n"
            "     de tener conexión a una red física ni internet.\n"
            "  2. Comunicación Interprocesos (IPC): Aplicaciones locales que necesitan comunicarse mediante sockets en la misma máquina.\n"
            "  3. Seguridad: Un servidor vinculado a 127.0.0.1 solo acepta conexiones que provengan de la propia máquina,\n"
            "     haciéndolo invisible e inaccesible para atacantes o usuarios de la red externa (LAN o WAN).\n"
            "  4. Rendimiento: El tráfico hacia 127.0.0.1 nunca sale a la tarjeta de red física (NIC); el propio kernel del sistema\n"
            "     operativo lo enruta internamente en memoria de forma ultrarrápida."
        )
    },
    "pregunta_3": {
        "titulo": "3. ¿Qué constante de Python crea un socket TCP y cuál un socket UDP?",
        "respuesta_corta": "socket.SOCK_STREAM crea un socket TCP, y socket.SOCK_DGRAM crea un socket UDP.",
        "explicacion_detallada": (
            "En el módulo estándar 'socket' de Python:\n\n"
            "• Para crear un socket TCP (Orientado a conexión, fiable, flujo continuo de bytes):\n"
            "    socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
            "    -> 'SOCK_STREAM' indica un 'stream' o flujo continuo y ordenado de datos (TCP).\n\n"
            "• Para crear un socket UDP (Sin conexión, no garantizado, paquetes/datagramas individuales):\n"
            "    socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n"
            "    -> 'SOCK_DGRAM' indica 'datagram' o datagramas discretos independientes (UDP).\n\n"
            "• Nota sobre AF_INET:\n"
            "    'socket.AF_INET' indica la familia de direcciones (Address Family IPv4)."
        )
    }
}


def mostrar_verificacion_python():
    """Muestra los valores reales numéricos que tienen estas constantes en el kernel/Python."""
    print("=" * 70)
    print("🔍 INSPECCIÓN EN VIVO DEL MÓDULO 'socket' DE PYTHON:")
    print("=" * 70)
    print(f"  • socket.SOCK_STREAM = {socket.SOCK_STREAM}  -> (Tipo de Socket para TCP)")
    print(f"  • socket.SOCK_DGRAM  = {socket.SOCK_DGRAM}  -> (Tipo de Socket para UDP)")
    print(f"  • socket.AF_INET     = {socket.AF_INET}  -> (Familia de direcciones IPv4)")
    print(f"  • socket.AF_INET6    = {socket.AF_INET6} -> (Familia de direcciones IPv6)")
    print("=" * 70)


def mostrar_solucion_completa():
    """Imprime las respuestas redactadas completas del ejercicio."""
    print("=" * 70)
    print("       📝 EJERCICIO 4: RESPUESTAS TEÓRICAS - IP Y PUERTO")
    print("=" * 70)
    for clave, item in RESPUESTAS.items():
        print(f"\n{item['titulo']}")
        print("-" * 70)
        print(f"✅ RESPUESTA SINTÉTICA:\n   {item['respuesta_corta']}\n")
        print(f"📖 EXPLICACIÓN COMPLETA:\n{item['explicacion_detallada']}")
        print("=" * 70)

    mostrar_verificacion_python()


if __name__ == "__main__":
    mostrar_solucion_completa()

