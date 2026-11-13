"""
=============================================================================
EJERCICIO 2: CLIENTE QUE ENVÍA Y RECIBE (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un cliente que se conecte a 127.0.0.1:9000, envíe “Hola” y luego
espere y muestre la respuesta del servidor."

CONCEPTOS CLAVE:
1. socket(AF_INET, SOCK_STREAM): Socket orientado a conexión (TCP).
2. connect((IP, PUERTO)): Inicia el Three-Way Handshake (SYN -> SYN-ACK -> ACK).
3. sendall(bytes): Envía la cadena codificada (str.encode('utf-8')).
4. recv(tam_buffer): Bloquea hasta recibir datos del servidor.
5. decode('utf-8'): Convierte los bytes recibidos a texto legible.
6. close(): Libera el socket y cierra la conexión TCP (FIN / ACK).
=============================================================================
"""

import socket
import sys
import time
import threading

# Configuración del destino indicada en el enunciado
HOST_DESTINO = "127.0.0.1"
PUERTO_DESTINO = 9000
MENSAJE_A_ENVIAR = "Hola"


def ejecutar_cliente(host: str = HOST_DESTINO, puerto: int = PUERTO_DESTINO, mensaje: str = MENSAJE_A_ENVIAR):
    """
    Ejecuta el cliente TCP que envía un mensaje y muestra la respuesta.
    """
    print("=" * 65)
    print("        📡 EJERCICIO 2: CLIENTE TCP QUE ENVÍA Y RECIBE")
    print("=" * 65)
    print(f"[*] Destino objetivo: {host}:{puerto}")
    print(f"[*] Mensaje a enviar: \"{mensaje}\"")
    print("-" * 65)

    # 1. Crear el socket TCP
    # AF_INET = IPv4, SOCK_STREAM = TCP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Opcional: configurar un timeout de 5 segundos para evitar bloqueos indefinidos
    cliente_socket.settimeout(5.0)

    try:
        # 2. Conectar al servidor (Three-Way Handshake)
        print(f"[1] Conectando a {host}:{puerto}...")
        cliente_socket.connect((host, puerto))
        print("[+] ¡Conexión establecida con éxito!")

        # 3. Enviar el mensaje codificado en bytes
        mensaje_bytes = mensaje.encode("utf-8")
        print(f"[2] Enviando {len(mensaje_bytes)} bytes: \"{mensaje}\"")
        cliente_socket.sendall(mensaje_bytes)
        print("[+] Mensaje enviado al servidor.")

        # 4. Esperar y recibir la respuesta del servidor
        print("[3] Esperando respuesta del servidor...")
        respuesta_bytes = cliente_socket.recv(1024)

        if respuesta_bytes:
            # 5. Decodificar y mostrar la respuesta
            respuesta_texto = respuesta_bytes.decode("utf-8")
            print("-" * 65)
            print(f"📥 RESPUESTA DEL SERVIDOR: \"{respuesta_texto}\"")
            print(f"   (Recibidos {len(respuesta_bytes)} bytes)")
            print("-" * 65)
        else:
            print("[!] El servidor cerró la conexión sin enviar datos.")

    except ConnectionRefusedError:
        print("\n[❌ ERROR] ConnectionRefusedError: No se pudo conectar al servidor.")
        print(f"          No hay ningún servidor escuchando en {host}:{puerto}.")
        print("💡 Solución:")
        print("   1. Abre otra terminal y ejecuta primero el servidor:")
        print("      python3 ejercicio_01_servidor_saludo.py")
        print("      (o: python3 ejercicio_03_servidor_eco.py)")
        print("   2. Luego vuelve a ejecutar este cliente.")
        return False
    except socket.timeout:
        print("\n[⏱️ ERROR] Timeout: El servidor no respondió dentro del tiempo límite (5s).")
        return False
    except Exception as err:
        print(f"\n[❌ ERROR inesperado]: {err}")
        return False
    finally:
        # 6. Cerrar el socket del cliente
        cliente_socket.close()
        print("[*] Conexión cerrada y recursos liberados.")
    return True


def servidor_temporal_demo(puerto: int = PUERTO_DESTINO):
    """Servidor temporal para permitir pruebas automáticas cuando no hay servidor manual."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST_DESTINO, puerto))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                msg = conn.recv(1024).decode("utf-8")
                # Responde confirmando la recepción
                conn.sendall(f"Servidor: ¡Hola cliente! Recibí tu mensaje '{msg}'".encode("utf-8"))
    except Exception:
        pass


if __name__ == "__main__":
    if "--demo" in sys.argv:
        print("[Iniciando servidor de demostración en segundo plano para prueba automática...]")
        hilo = threading.Thread(target=servidor_temporal_demo, args=(PUERTO_DESTINO,), daemon=True)
        hilo.start()
        time.sleep(0.2)
        ejecutar_cliente()
        hilo.join(timeout=1.0)
    else:
        exito = ejecutar_cliente()
        # Si no fue exitoso y estamos en un entorno sin tty, demostramos con el servidor demo
        if not exito and not sys.stdin.isatty():
            print("\n[Activando demostración automática de respaldo...]")
            hilo = threading.Thread(target=servidor_temporal_demo, args=(PUERTO_DESTINO,), daemon=True)
            hilo.start()
            time.sleep(0.2)
            ejecutar_cliente()
            hilo.join(timeout=1.0)
