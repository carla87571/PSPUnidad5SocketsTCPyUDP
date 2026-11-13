"""
=============================================================================
EJERCICIO 2: CLIENTE INTERACTIVO (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un cliente que pida texto por teclado con input(), lo envíe al
servidor y muestre la respuesta. El bucle termina cuando el usuario
escribe “salir”.

💡 Pista: envuelve el input() + sendall() + recv() en un while True y
rompe el bucle con break cuando el texto sea "salir"."

CONCEPTOS CLAVE:
1. Sesión persistente TCP: A diferencia de conexiones que se abren y cierran
   por cada mensaje, aquí mantenemos la conexión abierta durante múltiples
   intercambios (bucle while).
2. Protocolo de finalización: El comando especial "salir" pacta el fin de sesión.
3. break: Rompe el bucle while True cerrando ordenadamente el socket con close().
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9000
BUFFER_SIZE = 1024


def ejecutar_cliente_interactivo(host: str = HOST, puerto: int = PUERTO, lista_simulada: list = None):
    """
    Ejecuta el bucle interactivo del cliente TCP.
    
    :param host: Dirección IP del servidor.
    :param puerto: Puerto TCP del servidor.
    :param lista_simulada: Lista opcional de cadenas para pruebas no interactivas.
    """
    print("=" * 65)
    print("        💬 EJERCICIO 2: CLIENTE INTERACTIVO TCP")
    print("=" * 65)
    print(f"[*] Conectando a {host}:{puerto}...")

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.settimeout(6.0)

    try:
        cliente_socket.connect((host, puerto))
        print("[+] ¡Conectado al servidor con éxito!")
        print("-" * 65)
        print("💡 Escribe frases para enviarlas al servidor.")
        print("💡 Escribe 'salir' para finalizar la sesión.")
        print("-" * 65)

        indice_simulado = 0

        # Pista: Envuelve input() + sendall() + recv() en un while True
        while True:
            # 1. Obtener la entrada de usuario con input() o simulación
            if lista_simulada is not None:
                if indice_simulado < len(lista_simulada):
                    texto = lista_simulada[indice_simulado]
                    indice_simulado += 1
                    print(f"✍️  [Simulado]: {texto}")
                else:
                    texto = "salir"
            elif sys.stdin.isatty():
                try:
                    texto = input("✍️  Mensaje > ").strip()
                except (EOFError, KeyboardInterrupt):
                    texto = "salir"
                    print("\n[!] Entrada cancelada. Saliendo...")
            else:
                linea = sys.stdin.readline()
                if linea:
                    texto = linea.strip()
                    print(f"✍️  [stdin]: {texto}")
                else:
                    texto = "salir"

            # 2. Pista: Rompe el bucle con break cuando el texto sea "salir"
            if texto.lower() == "salir":
                print("\n[>] Enviando comando de cierre 'salir' al servidor...")
                cliente_socket.sendall(b"salir")
                try:
                    # Leemos posible mensaje de despedida del servidor
                    despedida = cliente_socket.recv(BUFFER_SIZE)
                    if despedida:
                        print(f"📥 Servidor respondió: \"{despedida.decode('utf-8', errors='replace').strip()}\"")
                except socket.timeout:
                    pass
                print("[!] Rompiendo el bucle con break.")
                break

            if not texto:
                continue

            # 3. Enviar el texto al servidor
            cliente_socket.sendall(texto.encode("utf-8"))

            # 4. Esperar y mostrar la respuesta
            respuesta_bytes = cliente_socket.recv(BUFFER_SIZE)
            if not respuesta_bytes:
                print("[!] El servidor cerró la conexión prematuramente.")
                break

            respuesta_texto = respuesta_bytes.decode("utf-8", errors="replace")
            print(f"📥 Respuesta del servidor: \"{respuesta_texto}\"")

    except ConnectionRefusedError:
        print(f"\n[❌ ERROR] ConnectionRefusedError: No hay servidor escuchando en {host}:{puerto}.")
        print("💡 Asegúrate de iniciar primero:")
        print("   python3 ejercicio_01_servidor_cuenta_caracteres.py")
        print("   (o: python3 ejercicio_03_servidor_mayusculas.py)")
        return False
    except socket.timeout:
        print("\n[⏱️ ERROR] Timeout: El servidor tardó demasiado en responder.")
        return False
    except Exception as err:
        print(f"\n[❌ ERROR inesperado]: {err}")
        return False
    finally:
        cliente_socket.close()
        print("[*] Socket cliente cerrado. Sesión finalizada.")
    return True


def servidor_temporal_eco(puerto: int = PUERTO):
    """Servidor temporal para pruebas automáticas del cliente."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, puerto))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    txt = data.decode("utf-8", errors="replace")
                    if txt.lower() == "salir":
                        conn.sendall(b"Adios!")
                        break
                    conn.sendall(f"Eco({txt})".encode("utf-8"))
    except Exception:
        pass


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        # Ejecución de prueba controlada
        hilo = threading.Thread(target=servidor_temporal_eco, daemon=True)
        hilo.start()
        time.sleep(0.2)
        ejecutar_cliente_interactivo(lista_simulada=["Hola mundo", "Probando bucle", "salir"])
        hilo.join(timeout=1.0)
    else:
        ejecutar_cliente_interactivo()

