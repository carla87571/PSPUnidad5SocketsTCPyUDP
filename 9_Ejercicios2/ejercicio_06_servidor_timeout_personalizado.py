"""
=============================================================================
EJERCICIO 6: SERVIDOR CON TIMEOUT PERSONALIZADO (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor que cierre la conexión si el cliente no envía datos
en 10 segundos.

💡 Pista: después de accept(), llama a conn.settimeout(10).
Captura socket.timeout y envía un mensaje de despedida antes de cerrar."

CONCEPTOS CLAVE:
1. Prevención de ataques DoS y Slowloris:
   Si un cliente se conecta y nunca envía datos, consumiría un socket del sistema
   indefinidamente.
2. conn.settimeout(10):
   Configura un temporizador para las operaciones de lectura (recv) en ese socket específico.
3. socket.timeout:
   Excepción levantada por el kernel si transcurren los 10 segundos sin que
   llegue un solo byte.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9015
TIMEOUT_DEFAULT = 10.0  # 10 segundos requeridos por el enunciado


def ejecutar_servidor_timeout(host: str = HOST, puerto: int = PUERTO, segundos_timeout: float = TIMEOUT_DEFAULT):
    """
    Ejecuta el servidor que cierra conexiones inactivas por timeout.
    
    :param host: IP de escucha.
    :param puerto: Puerto TCP.
    :param segundos_timeout: Tiempo límite de inactividad (10s por enunciado).
    """
    print("=" * 70)
    print("        ⏱️ EJERCICIO 6: SERVIDOR CON TIMEOUT PERSONALIZADO")
    print("=" * 70)
    print(f"[*] Escuchando en {host}:{puerto}")
    print(f"[*] Límite de inactividad configurado: {segundos_timeout} segundos.")
    print("-" * 70)

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(1)
        print("[+] Servidor esperando conexión...")

        conn, addr = servidor_socket.accept()
        print(f"\n[+] ¡Cliente conectado desde {addr}!")

        # Pista: Después de accept(), llama a conn.settimeout(10)
        conn.settimeout(segundos_timeout)
        print(f"[+] conn.settimeout({segundos_timeout}) aplicado.")
        print(f"[*] Esperando datos del cliente (máximo {segundos_timeout} segundos)...")

        try:
            inicio = time.time()
            datos = conn.recv(1024)

            if datos:
                texto = datos.decode("utf-8", errors="replace")
                print(f"[+] Datos recibidos a tiempo: \"{texto.strip()}\"")
                conn.sendall(b"Datos recibidos a tiempo. Gracias.\n")
            else:
                print("[-] El cliente cerró la conexión sin enviar datos.")

        # Pista: Captura socket.timeout y envía un mensaje de despedida antes de cerrar
        except socket.timeout:
            tiempo_transcurrido = time.time() - inicio
            print(f"\n[⚠️ ALERTA] socket.timeout activado tras {tiempo_transcurrido:.2f}s sin actividad.")
            mensaje_despedida = (
                f"Servidor: Tiempo de inactividad agotado ({segundos_timeout}s). "
                "Cerrando conexion por inactividad.\n"
            )
            try:
                print("[>] Enviando mensaje de despedida al cliente...")
                conn.sendall(mensaje_despedida.encode("utf-8"))
            except Exception:
                pass
            print("[+] Mensaje de despedida enviado.")

        finally:
            conn.close()
            print(f"[-] Conexión con {addr} cerrada.")

    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario.")
    finally:
        servidor_socket.close()
        print("[*] Socket del servidor cerrado.")


def cliente_inactivo_demo(puerto: int = PUERTO, segundos_espera: float = 3.0):
    """Cliente que se conecta y se queda en silencio a propósito para forzar el timeout."""
    time.sleep(0.2)
    print("\n   [Cliente Silencioso Test] Conectando al servidor con timeout...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            print("   [Cliente Silencioso Test] Conectado. Permaneciendo en silencio intencionadamente...")
            # Lee la respuesta de despedida cuando el servidor corte
            despedida = c.recv(1024).decode("utf-8", errors="replace")
            print(f"   [Cliente Silencioso Test] Servidor envió despedida:\n   \"{despedida.strip()}\"")
            print("   [Cliente Silencioso Test] ✅ ¡Verificación de timeout superada!")
    except Exception as e:
        print(f"   [Cliente Silencioso Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN: Probando con timeout de 2.0s para agilizar]")
        hilo = threading.Thread(target=cliente_inactivo_demo, args=(PUERTO, 2.0), daemon=True)
        hilo.start()
        ejecutar_servidor_timeout(segundos_timeout=2.0)
        hilo.join(timeout=3.0)
    else:
        # Modo estándar con los 10 segundos estrictos del enunciado
        ejecutar_servidor_timeout(segundos_timeout=10.0)

