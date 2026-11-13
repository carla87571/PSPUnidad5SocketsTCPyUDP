"""
07_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Servidor Demonio de Diagnóstico y Métricas (DevOps Daemon)

ESCENARIO REAL:
---------------
En el mundo de la administración de sistemas y DevOps (como Prometheus, Nagios o Datadog),
los servidores ejecutan un "demonio" o agente TCP en segundo plano.
Este servidor escucha en un puerto privado y responde a las peticiones de monitoreo
para verificar que el servidor esté vivo y obtener sus métricas (CPU, RAM, disco).

CONCEPTOS DEL SERVIDOR APLICADOS:
---------------------------------
  1. Configuración de SO_REUSEADDR (para poder reiniciar el servidor sin esperas).
  2. bind() al endpoint local y listen() con cola de espera.
  3. Bucle de atención 'while True' para atender peticiones sucesivas.
  4. Uso correcto de los dos sockets:
     - 'servidor' escucha en la puerta principal.
     - 'conexion' atiende a cada cliente monitor.
  5. Manejo robusto de errores para que la caída de un cliente NO tire el servidor.

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático (todo en una sola terminal):
      python3 07_ejemplo_vida_real.py

2. Modo real con dos terminales:
      Terminal 1 (Servidor de métricas): python3 07_ejemplo_vida_real.py --servidor
      Terminal 2 (Cliente administrador): python3 07_ejemplo_vida_real.py --cliente
"""

import json
import os
import platform
import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PUERTO = 6000

def obtener_metricas_sistema():
    """Genera datos reales/simulados del estado del servidor."""
    return {
        "sistema": platform.system(),
        "nodo": platform.node(),
        "arquitectura": platform.machine(),
        "python_version": platform.python_version(),
        "cpu_nucleos": os.cpu_count(),
        "estado": "SALUDABLE (OK)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def ejecutar_servidor_metricas(limite_atenciones=None):
    """
    Representa el servidor de diagnóstico (Servidor TCP).
    Escucha en el puerto 6000 y atiende consultas de monitoreo.
    """
    print("\n" + "=" * 65)
    print(f"  [SERVIDOR DAEMON] Iniciando agente de diagnóstico en {HOST}:{PUERTO}")
    print("=" * 65)

    # 1. Crear el socket TCP maestro
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        # Permitir reutilización inmediata de la dirección
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. Reservar puerto con bind()
        servidor.bind((HOST, PUERTO))

        # 3. Anunciar modo escucha con listen()
        servidor.listen(5)
        print(f"[SERVIDOR] Escuchando activamente. Listo para recibir clientes...\n")

        atenciones = 0

        # 4. Bucle principal de atención
        while True:
            try:
                # 5. Esperar llamada entrante (bloqueante)
                conexion, direccion_cliente = servidor.accept()
                atenciones += 1
                print(f"[SERVIDOR] 📞 Conexión #{atenciones} aceptada desde {direccion_cliente}")

                # 6. Atender exclusivamente usando el socket 'conexion'
                with conexion:
                    # Timeout de lectura por si el cliente se conecta pero no envía nada
                    conexion.settimeout(3.0)

                    peticion_bytes = conexion.recv(1024)
                    if not peticion_bytes:
                        print("[SERVIDOR] El cliente se desconectó sin enviar comandos.")
                        continue

                    comando = peticion_bytes.decode("utf-8").strip().upper()
                    print(f"[SERVIDOR] Comando recibido: '{comando}'")

                    # Procesar comando
                    if comando == "PING":
                        respuesta = "PONG | Servidor activo y respondiendo."
                    elif comando == "METRICAS":
                        respuesta = json.dumps(obtener_metricas_sistema(), indent=2)
                    elif comando == "AYUDA":
                        respuesta = "Comandos disponibles: PING, METRICAS, AYUDA"
                    else:
                        respuesta = f"ERROR: Comando '{comando}' desconocido. Envía 'AYUDA'."

                    # Enviar respuesta con sendall()
                    conexion.sendall(respuesta.encode("utf-8"))
                    print(f"[SERVIDOR] Respuesta enviada al cliente. Cerrando canal privado.")

                if limite_atenciones and atenciones >= limite_atenciones:
                    print(f"\n[SERVIDOR] Límite de demostración alcanzado ({limite_atenciones} clientes).")
                    break

            except socket.timeout:
                print("[SERVIDOR] ⏱ Timeout: El cliente tardó demasiado en enviar datos.")
            except Exception as e:
                print(f"[SERVIDOR] ❌ Error atendiendo al cliente: {e}")
                # El bucle continúa: el servidor nunca se apaga por el fallo de un cliente

    print("[SERVIDOR] Socket maestro cerrado. Servidor apagado.")

def ejecutar_cliente_monitoreo(comando="METRICAS"):
    """Cliente que simula la herramienta de monitoreo del administrador."""
    print(f"\n[CLIENTE MONITOR] Conectando para enviar comando: '{comando}'...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PUERTO))
            cliente.sendall(comando.encode("utf-8"))
            respuesta = cliente.recv(2048)
            print("-" * 50)
            print(f"[CLIENTE MONITOR] Respuesta recibida:\n{respuesta.decode('utf-8')}")
            print("-" * 50)
        except ConnectionRefusedError:
            print("[CLIENTE MONITOR] Error: Servidor apagado o inaccesible.")

def modo_demostracion():
    """Ejecuta demostración automática con varios clientes secuenciales."""
    print("=" * 70)
    print("  07 - EJEMPLO DE LA VIDA REAL: SERVIDOR DE MÉTRICAS Y SALUD")
    print("       (Demostración automática de atención secuencial con TCP)")
    print("=" * 70)

    # Iniciar servidor en segundo plano limitado a 2 atenciones
    hilo_servidor = threading.Thread(
        target=ejecutar_servidor_metricas,
        kwargs={"limite_atenciones": 2},
        daemon=True
    )
    hilo_servidor.start()
    time.sleep(0.3)

    # Cliente 1 consulta PING
    ejecutar_cliente_monitoreo(comando="PING")
    time.sleep(0.3)

    # Cliente 2 consulta METRICAS
    ejecutar_cliente_monitoreo(comando="METRICAS")

    hilo_servidor.join(timeout=2.0)

    print("\n" + "=" * 70)
    print("  RESUMEN PEDAGÓGICO DEL SERVIDOR TCP:")
    print("  1. bind() + listen() dejaron el socket 'servidor' listo para recibir.")
    print("  2. accept() bloqueó el hilo hasta recibir cada llamada.")
    print("  3. Cada llamada generó un socket 'conexion' independiente.")
    print("  4. El bucle 'while True' permitió atender múltiples clientes sin caerse.")
    print("  5. Bloques 'try/except' garantizaron la resiliencia del servicio.")
    print("=" * 70)

if __name__ == "__main__":
    if "--servidor" in sys.argv:
        ejecutar_servidor_metricas()
    elif "--cliente" in sys.argv:
        cmd = sys.argv[2] if len(sys.argv) > 2 else "METRICAS"
        ejecutar_cliente_monitoreo(comando=cmd)
    else:
        modo_demostracion()

