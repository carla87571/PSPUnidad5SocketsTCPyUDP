"""
=============================================================================
EJERCICIO 1: SERVIDOR QUE CUENTA CARACTERES (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor que reciba un texto y devuelva el número de caracteres
(ej: 'hola' -> '4').

💡 Pista: recibe con recv(1024).decode(), calcula len(texto) y envía
el resultado con str(...).encode()."

CONCEPTOS CLAVE:
1. socket.SOCK_STREAM: Protocolo TCP orientado a conexión.
2. recv(1024).decode(): Lee hasta 1024 bytes y los transforma en str de Python.
3. len(texto): Cuenta la cantidad de caracteres de la cadena (no bytes).
4. str(num).encode(): Serializa el número entero a bytes para enviarlo por red.
5. sendall(): Garantiza que todos los bytes del resultado sean entregados.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9000
BUFFER_SIZE = 1024


def ejecutar_servidor(host: str = HOST, puerto: int = PUERTO, un_solo_cliente: bool = True):
    """
    Inicia el servidor TCP contador de caracteres.
    
    :param host: Dirección IP de escucha (127.0.0.1).
    :param puerto: Puerto de escucha TCP (9000).
    :param un_solo_cliente: Si es True, atiende a un cliente y finaliza (modo ejercicio).
    """
    print("=" * 65)
    print("        🔤 EJERCICIO 1: SERVIDOR QUE CUENTA CARACTERES")
    print("=" * 65)
    print(f"[*] Creando socket TCP en {host}:{puerto}...")

    # 1. Crear socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # 2. Asociar el socket y escuchar conexiones
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(5)
        print(f"[+] Servidor escuchando en {host}:{puerto}...")
        print("-" * 65)
        print("💡 Para probar este servidor:")
        print(f"   Terminal B: nc {host} {puerto}")
        print(f"   O ejecuta:  python3 ejercicio_02_cliente_interactivo.py")
        print("-" * 65)

        contador = 0
        while True:
            print("[*] Esperando cliente entrante...")
            conn, addr = servidor_socket.accept()
            contador += 1
            print(f"\n[+] Conexión #{contador} aceptada desde {addr}")

            with conn:
                while True:
                    # 3. Recibir texto con recv() y decodificar a string
                    datos_bytes = conn.recv(BUFFER_SIZE)
                    if not datos_bytes:
                        print(f"[-] Cliente {addr} cerró la conexión.")
                        break

                    texto = datos_bytes.decode("utf-8", errors="replace").strip()
                    print(f"📥 Texto recibido: \"{texto}\"")

                    # Si el cliente solicita salir
                    if texto.lower() == "salir":
                        print("[i] Cliente envió 'salir'. Cerrando sesión.")
                        conn.sendall(b"Adios\n")
                        break

                    # 4. Calcular len(texto) y enviar el resultado con str(...).encode()
                    num_caracteres = len(texto)
                    respuesta = str(num_caracteres)
                    print(f"📤 Calculado: {num_caracteres} caracteres. Enviando \"{respuesta}\"")
                    conn.sendall(respuesta.encode("utf-8"))

            if un_solo_cliente:
                print("\n[i] Ejercicio 1 completado exitosamente tras atender al cliente.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario.")
    except Exception as err:
        print(f"\n[❌ ERROR en servidor]: {err}")
    finally:
        servidor_socket.close()
        print("[*] Socket del servidor cerrado.")


def cliente_demo_test(puerto: int = PUERTO):
    """Cliente de prueba que envía palabras y verifica el conteo devuelto."""
    time.sleep(0.25)
    print("\n   [Cliente Test] Conectando al servidor contador...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            palabras = ["hola", "CEEDCV", "Desarrollo Multiplataforma"]
            for p in palabras:
                c.sendall(p.encode("utf-8"))
                resp = c.recv(BUFFER_SIZE).decode("utf-8")
                print(f"   [Cliente Test] Enviado: '{p}' -> Respuesta recibida: '{resp}'")
                assert int(resp) == len(p), f"Error: esperados {len(p)}, recibidos {resp}"
            print("   [Cliente Test] ✅ ¡Verificación de conteo superada exitosamente!")
    except Exception as e:
        print(f"   [Cliente Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_demo_test, daemon=True)
        hilo.start()
        ejecutar_servidor(un_solo_cliente=True)
        hilo.join(timeout=1.0)
    else:
        ejecutar_servidor(un_solo_cliente=False)

