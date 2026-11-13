"""
=============================================================================
EJERCICIO 4: CLIENTE CON RECONEXIÓN AUTOMÁTICA (TCP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Cliente que intenta conectar, y si falla, reintenta hasta 3 veces con 2s de espera.

💡 Pista: envuelve socket.connect() en un bucle for con try/except.
Captura ConnectionRefusedError y socket.timeout, espera 2s con time.sleep(2) y reintenta."

CONCEPTOS CLAVE:
1. Resiliencia de red: En entornos reales, los servidores pueden reiniciarse,
   sufrir sobrecargas temporales o experimentar microcortes de conectividad.
2. Regeneración del socket: Si un socket falla al invocar connect(), su estado
   interno queda invalidado. En cada reintento se debe instanciar un nuevo socket.
3. Retroceso / Espera (Backoff): time.sleep(2) evita saturar la CPU y la red
   con peticiones consecutivas inmediatas.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9005  # Puerto de prueba para reconexión
MAX_INTENTOS = 3
ESPERA_SEGUNDOS = 2.0


def ejecutar_cliente_con_reconexion(host: str = HOST, puerto: int = PUERTO, max_intentos: int = MAX_INTENTOS, espera: float = ESPERA_SEGUNDOS):
    """
    Intenta conectar a un servidor TCP reintentando hasta max_intentos veces.
    
    :param host: Dirección IP del servidor.
    :param puerto: Puerto TCP.
    :param max_intentos: Número máximo de intentos (3 por enunciado).
    :param espera: Segundos de espera entre intentos (2s por enunciado).
    """
    print("=" * 65)
    print("        🔄 EJERCICIO 4: CLIENTE CON RECONEXIÓN AUTOMÁTICA")
    print("=" * 65)
    print(f"[*] Objetivo: {host}:{puerto}")
    print(f"[*] Política: Hasta {max_intentos} intentos con {espera}s de espera.")
    print("-" * 65)

    conexion_exitosa = False

    # Pista: bucle for con try/except envolviendo connect()
    for intento in range(1, max_intentos + 1):
        print(f"\n[Intento {intento}/{max_intentos}] Intentando conectar a {host}:{puerto}...")

        # NOTA PEDAGÓGICA IMPORTANTE:
        # Se debe crear un NUEVO socket en cada intento porque un socket
        # que falla en connect() no puede reutilizarse en Linux/POSIX.
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.settimeout(3.0)

        try:
            inicio = time.time()
            cliente_socket.connect((host, puerto))
            tiempo_conexion = time.time() - inicio
            print(f"[+] ¡CONEXIÓN ESTABLECIDA con éxito en el intento {intento} ({tiempo_conexion:.3f}s)!")
            conexion_exitosa = True

            # Enviar mensaje de prueba para verificar la comunicación
            mensaje = "¡Hola desde cliente resiliente!"
            cliente_socket.sendall(mensaje.encode("utf-8"))
            respuesta = cliente_socket.recv(1024).decode("utf-8", errors="replace")
            print(f"📥 Respuesta del servidor: \"{respuesta}\"")

            cliente_socket.close()
            break  # Salir del bucle tras el éxito

        except (ConnectionRefusedError, socket.timeout) as err:
            # Captura de ConnectionRefusedError y socket.timeout según la pista del PDF
            print(f"[!] Falló el intento {intento}: {type(err).__name__} ({err})")
            cliente_socket.close()

            if intento < max_intentos:
                print(f"[⏱️] Esperando {espera} segundos antes del siguiente intento...")
                time.sleep(espera)
            else:
                print(f"\n[❌ ERROR FINAL] Se agotaron los {max_intentos} intentos sin éxito.")
                print(f"    El servidor en {host}:{puerto} no está disponible.")

    print("-" * 65)
    return conexion_exitosa


def servidor_tardio_demo(puerto: int = PUERTO, segundos_retraso: float = 2.5):
    """
    Servidor que arranca intencionadamente con retraso para demostrar
    cómo el cliente falla inicialmente y tiene éxito en el reintento.
    """
    print(f"   [Servidor Demo] Esperará {segundos_retraso}s antes de iniciar para simular caída...")
    time.sleep(segundos_retraso)
    print(f"   [Servidor Demo] ¡Iniciando ahora servidor en puerto {puerto}!")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, puerto))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                msg = conn.recv(1024).decode("utf-8")
                conn.sendall(f"Servidor recuperado: Recibido '{msg}'".encode("utf-8"))
        print("   [Servidor Demo] Petición atendida con éxito tras la recuperación.")
    except Exception as e:
        print(f"   [Servidor Demo] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN: Simulación de recuperación de red]")
        # El servidor tardará 2.5 segundos en levantarse.
        # Intento 1 (0s) -> Fallará (ConnectionRefusedError)
        # Espera de 2s
        # Intento 2 (~2.1s) -> El servidor ya estará escuchando y conectará!
        hilo_servidor = threading.Thread(target=servidor_tardio_demo, args=(PUERTO, 2.3), daemon=True)
        hilo_servidor.start()
        
        ejecutar_cliente_con_reconexion(max_intentos=3, espera=1.5)
        hilo_servidor.join(timeout=2.0)
    else:
        # Modo estándar: prueba contra el puerto indicado
        ejecutar_cliente_con_reconexion()

