"""
06_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Estación de Sensores IoT (Arquitectura Cliente-Servidor)

ESCENARIO REAL:
---------------
Imagina un invernadero o casa inteligente que tiene un microordenador (servidor)
conectado a sensores de temperatura y humedad.
Un panel de control o aplicación móvil (cliente) se conecta por TCP para solicitar
el estado actual del clima.

¿POR QUÉ TCP (CARTA CERTIFICADA)?
---------------------------------
Porque necesitamos confirmar que la petición llegó y que la lectura del sensor
llegue completa y sin datos corruptos antes de tomar decisiones (ej. regar o encender calefactor).

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático (todo en una sola terminal):
      python3 06_ejemplo_vida_real.py

2. Modo real con dos terminales (opcional):
      Terminal 1 (Servidor): python3 06_ejemplo_vida_real.py --servidor
      Terminal 2 (Cliente):  python3 06_ejemplo_vida_real.py --cliente
"""

import socket
import sys
import threading
import time

HOST = "127.0.0.1"  # localhost (nuestra propia máquina de pruebas)
PUERTO = 5000       # Puerto alto / de usuario (> 1024)

# Datos simulados de la estación meteorológica
DATOS_SENSOR = {
    "temperatura": "22.5 °C",
    "humedad": "58 %",
    "presion": "1013 hPa",
    "estado": "Condiciones óptimas en el invernadero"
}

def ejecutar_servidor(una_sola_consulta=False):
    """
    Representa la estación meteorológica (Servidor).
    Espera conexiones y responde con las lecturas de los sensores.
    """
    print("\n[SERVIDOR] Iniciando estación meteorológica...")

    # 1. Crear el socket TCP (IPv4, TCP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permite reutilizar el puerto inmediatamente si se reinicia el servidor
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Asociar el socket al endpoint (IP, PUERTO)
    servidor.bind((HOST, PUERTO))

    # 3. Poner el socket a la escucha de conexiones entrantes
    servidor.listen(1)
    print(f"[SERVIDOR] Escuchando en el endpoint ({HOST}:{PUERTO}). Esperando cliente...")

    try:
        while True:
            # 4. Aceptar la conexión (esto bloquea hasta que un cliente se conecta)
            socket_cliente, direccion_cliente = servidor.accept()
            print(f"\n[SERVIDOR] ¡Cliente conectado desde {direccion_cliente}!")

            # 5. Recibir la solicitud del cliente
            # NOTA DIDÁCTICA: Los sockets solo transmiten BYTES, por eso usamos .decode()
            peticion_bytes = socket_cliente.recv(1024)
            peticion_texto = peticion_bytes.decode("utf-8").strip()
            print(f"[SERVIDOR] Petición recibida del cliente: '{peticion_texto}'")

            # 6. Procesar y generar la respuesta
            if peticion_texto == "GET_CLIMA":
                respuesta = (
                    f"REPORTE_CLIMA | Temp: {DATOS_SENSOR['temperatura']} | "
                    f"Humedad: {DATOS_SENSOR['humedad']} | Estado: {DATOS_SENSOR['estado']}"
                )
            else:
                respuesta = "ERROR: Comando no reconocido. Usa 'GET_CLIMA'."

            # 7. Enviar la respuesta convertida a BYTES con .encode()
            print(f"[SERVIDOR] Enviando telemetría al cliente...")
            socket_cliente.sendall(respuesta.encode("utf-8"))

            # 8. Cerrar la conexión con este cliente específico
            socket_cliente.close()
            print("[SERVIDOR] Conexión con el cliente cerrada limpiamente.")

            if una_sola_consulta:
                break
    finally:
        servidor.close()
        print("[SERVIDOR] Servidor apagado.")

def ejecutar_cliente():
    """
    Representa la aplicación móvil o panel del usuario (Cliente).
    Se conecta al servidor, pide los datos y los muestra.
    """
    print("\n[CLIENTE] Iniciando aplicación de monitoreo...")

    # 1. Crear el socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 2. Conectar al servidor en su endpoint (IP, PUERTO)
        print(f"[CLIENTE] Conectando a la estación en ({HOST}:{PUERTO})...")
        cliente.connect((HOST, PUERTO))
        print("[CLIENTE] ¡Conexión TCP establecida exitosamente (Handshake completado)!")

        # 3. Enviar la petición codificada a bytes
        comando = "GET_CLIMA"
        print(f"[CLIENTE] Enviando comando: '{comando}'")
        cliente.sendall(comando.encode("utf-8"))

        # 4. Esperar y recibir la respuesta del servidor
        respuesta_bytes = cliente.recv(1024)
        respuesta_texto = respuesta_bytes.decode("utf-8")

        print("\n" + "=" * 50)
        print("  [CLIENTE] DATOS RECIBIDOS EN TIEMPO REAL:")
        print(f"  {respuesta_texto}")
        print("=" * 50 + "\n")

    except ConnectionRefusedError:
        print("[CLIENTE] Error: No se pudo conectar. ¿Está el servidor encendido?")
    finally:
        # 5. Cerrar el socket
        cliente.close()
        print("[CLIENTE] Socket del cliente cerrado.")

def modo_demostracion():
    """Ejecuta el servidor en un hilo de fondo y el cliente para demostración inmediata."""
    print("=" * 70)
    print("  06 - EJEMPLO DE LA VIDA REAL: ESTACIÓN DE MONITOREO CLIMÁTICO")
    print("       (Demostración automática Cliente/Servidor por Sockets TCP)")
    print("=" * 70)

    # Iniciar servidor en segundo plano
    hilo_servidor = threading.Thread(target=ejecutar_servidor, kwargs={"una_sola_consulta": True}, daemon=True)
    hilo_servidor.start()

    # Breve pausa para asegurar que el servidor esté escuchando
    time.sleep(0.5)

    # Ejecutar el cliente en el hilo principal
    ejecutar_cliente()

    # Esperar a que el servidor termine
    hilo_servidor.join(timeout=2.0)

    print("\n" + "=" * 70)
    print("  RESUMEN PEDAGÓGICO DE LO QUE OCURRIÓ:")
    print("  1. El SERVIDOR hizo bind en 127.0.0.1:5000 y se puso en listen().")
    print("  2. El CLIENTE hizo connect() estableciendo conexión fiable TCP.")
    print("  3. El CLIENTE codificó texto a bytes con .encode('utf-8') y usó sendall().")
    print("  4. El SERVIDOR leyó con .recv(), decodificó con .decode('utf-8') y respondió.")
    print("  5. Ambos sockets se cerraron ordenadamente con .close().")
    print("=" * 70)

if __name__ == "__main__":
    if "--servidor" in sys.argv:
        ejecutar_servidor(una_sola_consulta=False)
    elif "--cliente" in sys.argv:
        ejecutar_cliente()
    else:
        modo_demostracion()

