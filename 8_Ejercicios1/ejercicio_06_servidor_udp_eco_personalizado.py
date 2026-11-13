"""
=============================================================================
EJERCICIO 6: SERVIDOR UDP CON ECO PERSONALIZADO
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un servidor UDP que escuche en 127.0.0.1:9001. Al recibir un mensaje,
responda con "Recibido: " seguido del mensaje original."

CONCEPTOS CLAVE:
1. socket(AF_INET, SOCK_DGRAM): Socket para datagramas UDP.
2. bind((IP, PUERTO)): Asocia el socket a la IP y puerto local donde esperará datos.
3. ¡SIN listen() NI accept()!:
   En UDP no hay conexión ni handshake. No existe un socket hijo por cliente.
   Un único socket recibe datagramas de cualquier cliente del mundo mediante recvfrom().
4. recvfrom(tam_buffer): Devuelve (datos_bytes, (ip_origen, puerto_origen)).
5. sendto(datos_respuesta, direccion_cliente): Envía la respuesta al remitente original.
=============================================================================
"""

import socket
import sys
import time
import threading

HOST = "127.0.0.1"
PUERTO = 9001
BUFFER_SIZE = 1024


def ejecutar_servidor_udp(host: str = HOST, puerto: int = PUERTO, un_solo_paquete: bool = True):
    """
    Ejecuta el servidor UDP con eco personalizado.
    
    :param host: Dirección IP de escucha (127.0.0.1).
    :param puerto: Puerto UDP de escucha (9001).
    :param un_solo_paquete: Si es True, atiende un datagrama y finaliza (ideal para ejercicios).
    """
    print("=" * 65)
    print("        📬 EJERCICIO 6: SERVIDOR UDP CON ECO PERSONALIZADO")
    print("=" * 65)
    print(f"[*] Creando socket UDP (SOCK_DGRAM)...")

    # 1. Crear el socket UDP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 2. Asociar el socket a la dirección y puerto
        servidor_socket.bind((host, puerto))
        print(f"[+] bind() exitoso en {host}:{puerto}")
        print("-" * 65)
        print("💡 Observa la gran diferencia con TCP:")
        print("   - NO hay servidor_socket.listen()")
        print("   - NO hay servidor_socket.accept()")
        print("   - Pasamos directamente a recvfrom() para esperar datagramas.")
        print("-" * 65)
        print("💡 Para probarlo:")
        print("   - Terminal B: python3 ejercicio_05_cliente_udp_input.py")
        print(f"   - O con netcat: nc -u {host} {puerto}")
        print("-" * 65)

        contador = 0
        while True:
            print(f"[*] Esperando datagrama en {host}:{puerto} (recvfrom bloqueante)...")

            # 3. Recibir datagrama de cualquier cliente
            datos_bytes, direccion_cliente = servidor_socket.recvfrom(BUFFER_SIZE)
            contador += 1

            # 4. Decodificar el mensaje original
            mensaje_original = datos_bytes.decode("utf-8", errors="replace")
            print(f"\n[+] Datagrama #{contador} recibido desde {direccion_cliente}:")
            print(f"    Texto: \"{mensaje_original}\" ({len(datos_bytes)} bytes)")

            # 5. Construir la respuesta con el prefijo "Recibido: " solicitado
            respuesta_texto = f"Recibido: {mensaje_original}"
            respuesta_bytes = respuesta_texto.encode("utf-8")

            # 6. Responder al cliente usando sendto()
            print(f"[>] Enviando eco personalizado: \"{respuesta_texto}\" a {direccion_cliente}...")
            servidor_socket.sendto(respuesta_bytes, direccion_cliente)
            print("[+] Datagrama de respuesta enviado con éxito.")

            if un_solo_paquete:
                print("\n[i] Ejercicio 6 completado exitosamente tras responder al cliente.")
                break

    except KeyboardInterrupt:
        print("\n[!] Servidor UDP detenido por el usuario.")
    except Exception as err:
        print(f"\n[❌ ERROR en servidor UDP]: {err}")
    finally:
        # 7. Cerrar socket
        servidor_socket.close()
        print("[*] Socket UDP cerrado.")


def cliente_demo_udp(puerto: int = PUERTO):
    """Cliente de prueba que envía un datagrama UDP para verificar el servidor."""
    time.sleep(0.25)
    print("\n   [Cliente UDP Test] Enviando datagrama de prueba al servidor...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
            c.settimeout(3.0)
            msg = "Mi saludo para el ejercicio 6"
            c.sendto(msg.encode("utf-8"), (HOST, puerto))
            
            resp, _ = c.recvfrom(BUFFER_SIZE)
            texto_resp = resp.decode("utf-8")
            print(f"   [Cliente UDP Test] Respuesta del servidor: \"{texto_resp}\"")
            assert texto_resp == f"Recibido: {msg}", "La respuesta no cumple el formato esperado"
            print("   [Cliente UDP Test] ✅ Verificación exitosa: formato 'Recibido: ...' correcto.")
    except Exception as e:
        print(f"   [Cliente UDP Test] Error: {e}")


if __name__ == "__main__":
    if "--demo" in sys.argv or not sys.stdin.isatty():
        print("[MODO DEMOSTRACIÓN AUTOMÁTICA]")
        hilo = threading.Thread(target=cliente_demo_udp, daemon=True)
        hilo.start()
        ejecutar_servidor_udp(un_solo_paquete=True)
        hilo.join(timeout=1.0)
    else:
        ejecutar_servidor_udp(un_solo_paquete=True)

