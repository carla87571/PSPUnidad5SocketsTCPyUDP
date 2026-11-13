"""
=============================================================================
EJERCICIO 5: CLIENTE UDP CON ENTRADA DE USUARIO (INPUT)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un cliente UDP que pida un mensaje al usuario por teclado con input(),
lo envíe a 127.0.0.1:9001 y espere una respuesta.

💡 Pista: UDP no tiene connect(): la dirección va dentro del sendto(),
y la respuesta llega con recvfrom()."

CONCEPTOS CLAVE:
1. socket(AF_INET, SOCK_DGRAM): Socket sin conexión (UDP).
2. Sin connect(): En UDP no hay Three-Way Handshake previo.
3. sendto(bytes, (IP, PUERTO)): Cada datagrama debe especificar explícitamente
   la tupla de destino en cada envío.
4. recvfrom(tam_buffer): Recibe tanto los bytes de datos como la tupla (IP, puerto)
   del remitente que los envió.
5. Timeout esencial: Dado que UDP es 'best-effort' (no confiable) y no avisa si
   el servidor está apagado, se recomienda settimeout() para evitar bloqueos.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST_DESTINO = "127.0.0.1"
PUERTO_DESTINO = 9001
BUFFER_SIZE = 1024


def ejecutar_cliente_udp(mensaje_predeterminado: str = None):
    """
    Ejecuta el cliente UDP pidiendo la entrada al usuario.
    """
    print("=" * 65)
    print("        ✉️ EJERCICIO 5: CLIENTE UDP CON ENTRADA DE USUARIO")
    print("=" * 65)
    print(f"[*] Destino configurado: {HOST_DESTINO}:{PUERTO_DESTINO}")
    print("-" * 65)

    # 1. Obtener el mensaje del usuario con input()
    if mensaje_predeterminado is not None:
        mensaje = mensaje_predeterminado
        print(f"[input() simulado]: \"{mensaje}\"")
    elif sys.stdin.isatty():
        # Modo interactivo en terminal
        try:
            mensaje = input("✍️  Introduce un mensaje para enviar por UDP: ").strip()
            if not mensaje:
                mensaje = "Mensaje UDP por defecto"
                print(f"[!] Entrada vacía. Usando mensaje por defecto: \"{mensaje}\"")
        except EOFError:
            mensaje = "Prueba UDP automatizada"
    else:
        # Modo con entrada canalizada (pipe / script)
        linea = sys.stdin.readline().strip()
        if linea:
            mensaje = linea
            print(f"[Entrada leída desde stdin]: \"{mensaje}\"")
        else:
            mensaje = "¡Hola desde cliente UDP en DAM!"
            print(f"[Entrada automática]: \"{mensaje}\"")

    # 2. Crear el socket UDP (SOCK_DGRAM)
    # AF_INET = IPv4, SOCK_DGRAM = Datagramas UDP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Configurar timeout de 4 segundos para evitar bloqueo permanente si el servidor no responde
    cliente_socket.settimeout(4.0)

    try:
        # 3. Enviar el mensaje con sendto()
        # Observa que NO hacemos connect(): la dirección de destino va como 2º parámetro
        datos_a_enviar = mensaje.encode("utf-8")
        destino = (HOST_DESTINO, PUERTO_DESTINO)
        print(f"\n[>] Enviando datagrama ({len(datos_a_enviar)} bytes) a {destino}...")
        bytes_enviados = cliente_socket.sendto(datos_a_enviar, destino)
        print(f"[+] {bytes_enviados} bytes transmitidos exitosamente.")

        # 4. Esperar la respuesta con recvfrom()
        # recvfrom devuelve una tupla: (datos_recibidos, direccion_servidor)
        print("[*] Esperando respuesta del servidor con recvfrom()...")
        respuesta_bytes, remitente = cliente_socket.recvfrom(BUFFER_SIZE)

        # 5. Decodificar y mostrar el resultado
        respuesta_texto = respuesta_bytes.decode("utf-8", errors="replace")
        print("\n" + "=" * 65)
        print(f"📥 RESPUESTA RECIBIDA DESDE {remitente}:")
        print(f"   \"{respuesta_texto}\"")
        print("=" * 65)

    except socket.timeout:
        print("\n[⏱️ TIMEOUT] No se recibió respuesta en 4 segundos.")
        print("💡 ¿Por qué ocurre esto en UDP?")
        print("   A diferencia de TCP, en UDP no hay conexión previa.")
        print("   Si el servidor no está corriendo, UDP simplemente 'lanza el paquete'")
        print("   y no avisa de que no hay nadie escuchando.")
        print("   -> Asegúrate de iniciar primero: python3 ejercicio_06_servidor_udp_eco_personalizado.py")
    except Exception as err:
        print(f"\n[❌ ERROR inesperado]: {err}")
    finally:
        # 6. Cerrar el socket
        cliente_socket.close()
        print("\n[*] Socket UDP cerrado.")


def servidor_udp_demo(puerto: int = PUERTO_DESTINO):
    """Servidor UDP temporal para demostraciones automáticas."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST_DESTINO, puerto))
            datos, addr = s.recvfrom(BUFFER_SIZE)
            texto = datos.decode("utf-8", errors="replace")
            # Simula el comportamiento del ejercicio 6
            respuesta = f"Recibido: {texto}"
            s.sendto(respuesta.encode("utf-8"), addr)
    except Exception:
        pass


if __name__ == "__main__":
    if "--demo" in sys.argv:
        # Lanzar servidor temporal para demostrar el envío y recepción completos
        hilo_servidor = threading.Thread(target=servidor_udp_demo, daemon=True)
        hilo_servidor.start()
        time.sleep(0.15)
        ejecutar_cliente_udp(mensaje_predeterminado="Prueba de mensaje UDP interactivo")
        hilo_servidor.join(timeout=1.0)
    else:
        ejecutar_cliente_udp()
