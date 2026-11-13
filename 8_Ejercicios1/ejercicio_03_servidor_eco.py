"""
=============================================================================
EJERCICIO 3: SERVIDOR ECO (TCP ECHO SERVER)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor TCP que acepte una conexión, reciba un mensaje y devuelva
exactamente lo mismo que recibe."

CONCEPTOS CLAVE:
1. Servidor Eco (Echo Server): Estándar histórico de red (RFC 862).
   Su única misión es rebotar/retransmitir exactamente los mismos bytes
   que recibe del cliente sin alterarlos.
2. Flujo de datos simétrico:
   Cliente -(envía bytes)-> Servidor -(recibe bytes)-> Servidor -(reenvía los mismos bytes)-> Cliente.
3. Tratamiento transparente de datos:
   Al trabajar con bytes puros (sin necesidad de alterar la codificación),
   el servidor eco funciona con cualquier tipo de dato (texto, binario, imágenes, etc.).
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9000
BUFFER_SIZE = 1024


def ejecutar_servidor_eco(host: str = HOST, puerto: int = PUERTO, una_sola_conexion: bool = True):
    """
    Ejecuta el servidor TCP de eco.
    
    :param host: Dirección IP de escucha.
    :param puerto: Puerto TCP de escucha.
    :param una_sola_conexion: Si es True, atiende a 1 cliente y termina (ideal para actividades).
    """
    print("=" * 65)
    print("        🔄 EJERCICIO 3: SERVIDOR TCP ECO (ECHO SERVER)")
    print("=" * 65)
    print(f"[*] Inicializando servidor en {host}:{puerto}...")

    # 1. Crear el socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # 2. Asociar el socket y poner a escuchar
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(1)
        print(f"[+] Servidor escuchando en {host}:{puerto}")
        print("-" * 65)
        print("💡 Para interactuar con este servidor:")
        print(f"   Terminal B: python3 ejercicio_02_cliente_envia_recibe.py")
        print(f"   O netcat:   nc 127.0.0.1 {puerto}")
        print("-" * 65)

        contador = 0
        while True:
            # 3. Aceptar la conexión entrante
            print("[*] Esperando que un cliente se conecte (accept bloqueante)...")
            cliente_socket, cliente_addr = servidor_socket.accept()
            contador += 1
            print(f"\n[+] ¡Conexión #{contador} establecida desde {cliente_addr}!")

            try:
                # 4. Recibir el mensaje del cliente
                datos_recibidos = cliente_socket.recv(BUFFER_SIZE)

                if datos_recibidos:
                    # Mostrar información didáctica de lo recibido
                    texto_recibido = datos_recibidos.decode("utf-8", errors="replace")
                    print(f"📥 Datos recibidos ({len(datos_recibidos)} bytes): \"{texto_recibido}\"")
                    print(f"   Representación en bytes crudos: {datos_recibidos}")

                    # 5. Devolver EXACTAMENTE lo mismo que recibe (Servidor Eco)
                    print(f"📤 Devolviendo eco al cliente...")
                    cliente_socket.sendall(datos_recibidos)
                    print("[+] Eco enviado con éxito.")
                else:
                    print("[!] El cliente se conectó pero no envió datos.")

            finally:
                # 6. Cerrar el socket de este cliente
                cliente_socket.close()
                print(f"[-] Conexión con {cliente_addr} cerrada.")

            if una_sola_conexion:
                print("\n[i] Ejercicio 3 completado exitosamente tras responder el eco.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario.")
    except OSError as e:
        print(f"\n[❌ Error en servidor]: {e}")
    finally:
        servidor_socket.close()
        print("[*] Servidor finalizado.")


def cliente_demo_para_eco(puerto: int = PUERTO):
    """Cliente de prueba que envía un mensaje para verificar el eco."""
    time.sleep(0.3)
    print("\n   [Cliente Eco Test] Conectando a 127.0.0.1:9000...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((HOST, puerto))
            mensaje_test = "¡Probando el servidor eco de DAM!"
            print(f"   [Cliente Eco Test] Enviando: \"{mensaje_test}\"")
            c.sendall(mensaje_test.encode("utf-8"))
            
            eco = c.recv(BUFFER_SIZE).decode("utf-8")
            print(f"   [Cliente Eco Test] Eco recibido: \"{eco}\"")
            assert eco == mensaje_test, "El eco no coincide con el mensaje original"
            print("   [Cliente Eco Test] ✅ ¡Verificación de eco 100% exitosa!")
    except Exception as e:
        print(f"   [Cliente Eco Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_demo_para_eco, args=(PUERTO,), daemon=True)
        hilo.start()
        ejecutar_servidor_eco(una_sola_conexion=True)
        hilo.join(timeout=1.0)
    else:
        ejecutar_servidor_eco(una_sola_conexion=True)

