"""
=============================================================================
EJERCICIO 3: SERVIDOR DE MAYÚSCULAS (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"El cliente envía texto, el servidor lo devuelve en MAYÚSCULAS.

💡 Pista: recibe los datos con recv(1024).decode(), aplica .upper() y
envía el resultado con sendall(...)."

CONCEPTOS CLAVE:
1. Procesamiento en la Capa de Aplicación: El socket TCP actúa como canal de
   transporte de bytes; la lógica del servidor (transformar a mayúsculas con
   .upper()) reside enteramente en el código de aplicación.
2. Codificación / Decodificación:
   Bytes recibidos -> decode("utf-8") -> texto.upper() -> encode("utf-8") -> Bytes enviados.
3. sendall(): Asegura el envío atómico de todo el texto transformado.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9000
BUFFER_SIZE = 1024


def ejecutar_servidor_mayusculas(host: str = HOST, puerto: int = PUERTO, un_solo_cliente: bool = True):
    """
    Ejecuta el servidor TCP de transformación a mayúsculas.
    
    :param host: Dirección IP de escucha.
    :param puerto: Puerto TCP de escucha.
    :param un_solo_cliente: Si es True, atiende a un cliente completo y finaliza.
    """
    print("=" * 65)
    print("        🔠 EJERCICIO 3: SERVIDOR DE MAYÚSCULAS")
    print("=" * 65)
    print(f"[*] Iniciando servidor en {host}:{puerto}...")

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(5)
        print(f"[+] Servidor escuchando en {host}:{puerto}")
        print("-" * 65)
        print("💡 Para probarlo:")
        print(f"   Terminal B: python3 ejercicio_02_cliente_interactivo.py")
        print(f"   O netcat:   nc {host} {puerto}")
        print("-" * 65)

        contador = 0
        while True:
            print("[*] Esperando conexión de cliente...")
            conn, addr = servidor_socket.accept()
            contador += 1
            print(f"\n[+] ¡Conexión #{contador} establecida desde {addr}!")

            with conn:
                while True:
                    # 1. Recibir datos con recv(1024).decode()
                    datos_bytes = conn.recv(BUFFER_SIZE)
                    if not datos_bytes:
                        print(f"[-] Conexión cerrada por el cliente {addr}.")
                        break

                    texto_original = datos_bytes.decode("utf-8", errors="replace").strip()
                    print(f"📥 Recibido: \"{texto_original}\"")

                    # Si el cliente indica salida
                    if texto_original.lower() == "salir":
                        print("[i] Comando 'salir' recibido. Despidiendo al cliente.")
                        conn.sendall(b"HASTA PRONTO (SESION FINALIZADA)\n")
                        break

                    # 2. Pista: Aplica .upper()
                    texto_mayusculas = texto_original.upper()

                    # 3. Pista: Envía el resultado con sendall(...)
                    print(f"📤 Transformado a: \"{texto_mayusculas}\". Enviando...")
                    conn.sendall(texto_mayusculas.encode("utf-8"))

            if un_solo_cliente:
                print("\n[i] Ejercicio 3 completado exitosamente tras atender al cliente.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario.")
    except Exception as err:
        print(f"\n[❌ ERROR en servidor]: {err}")
    finally:
        servidor_socket.close()
        print("[*] Socket del servidor cerrado.")


def cliente_demo_mayusculas(puerto: int = PUERTO):
    """Cliente de prueba que envía frases y comprueba que se reciben en mayúsculas."""
    time.sleep(0.25)
    print("\n   [Cliente Mayúsculas Test] Conectando al servidor...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            frases = ["hola mundo", "python sockets", "desarrollo dam"]
            for f in frases:
                c.sendall(f.encode("utf-8"))
                resp = c.recv(BUFFER_SIZE).decode("utf-8")
                print(f"   [Cliente Mayúsculas Test] Enviado: '{f}' -> Recibido: '{resp}'")
                assert resp == f.upper(), f"Error: esperada '{f.upper()}', recibida '{resp}'"
            print("   [Cliente Mayúsculas Test] ✅ ¡Verificación de mayúsculas 100% correcta!")
    except Exception as e:
        print(f"   [Cliente Mayúsculas Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_demo_mayusculas, daemon=True)
        hilo.start()
        ejecutar_servidor_mayusculas(un_solo_cliente=True)
        hilo.join(timeout=1.0)
    else:
        ejecutar_servidor_mayusculas(un_solo_cliente=False)

