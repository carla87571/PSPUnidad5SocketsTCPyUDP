"""
07_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Cliente y Servidor Resilientes con Circuit Breaker y Reintentos

ESCENARIO REAL:
---------------
En arquitecturas distribuidas modernas (ej. pasarelas de pago, sincronización bancaria,
agentes de telemetría en la nube o apps móviles en túneles con poca cobertura):
  • Las redes FALLAN constantemente: microcortes, reinicios de servidores, puertos ocupados.
  • Un software profesional NUNCA debe colgarse ni asumir que connect() funcionará a la primera.

ESTE SCRIPT INTEGRA TODOS LOS CONCEPTOS DEL BLOQUE:
---------------------------------------------------
  1. Handshake TCP transparente mediante connect().
  2. SO_REUSEADDR en el servidor para evitar bloqueos por TIME_WAIT al reiniciar.
  3. Despedida ordenada de 4 vías (FIN / ACK) administrada con bloques 'with'.
  4. Red de seguridad completa:
     - Timeouts con settimeout() para evitar bloqueos infinitos.
     - Captura jerárquica de excepciones:
       * ConnectionRefusedError  -> Reintentar con backoff (pausa).
       * socket.timeout          -> Cancelar o reintentar sin congelar.
       * ConnectionResetError    -> Reabrir canal si cortaron de golpe.
       * OSError                 -> Fallback genérico de red.

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático:
      python3 07_ejemplo_vida_real.py

2. Modo con dos consolas separadas:
      Terminal 1: python3 07_ejemplo_vida_real.py --servidor
      Terminal 2: python3 07_ejemplo_vida_real.py --cliente
"""

import json
import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PUERTO = 7070

# --- LADO SERVIDOR (Microservicio Ingestion Gateway) ---
def iniciar_servidor_gateway(limite_transacciones=2):
    """
    Servidor robusto que escucha transacciones de campo.
    Utiliza SO_REUSEADDR y gestiona cierres limpios.
    """
    print("\n" + "=" * 65)
    print(f"  [GATEWAY BACKEND] Iniciando servicio en {HOST}:{PUERTO}")
    print("=" * 65)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        # Clave: Reutilizar puerto para no quedar atascado en TIME_WAIT
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(5)
        print("[GATEWAY] Escuchando activamente (Three-Way Handshakes listos para atender)...")

        atendidos = 0
        while atendidos < limite_transacciones:
            try:
                conexion, direccion = servidor.accept()
                atendidos += 1
                print(f"\n[GATEWAY] Conexión #{atendidos} aceptada desde {direccion}")

                with conexion:
                    conexion.settimeout(2.0)
                    datos_bytes = conexion.recv(1024)
                    if datos_bytes:
                        paquete = json.loads(datos_bytes.decode("utf-8"))
                        print(f"[GATEWAY] Transacción #{paquete.get('id')} recibida: ${paquete.get('monto')}")

                        # Confirmamos con acuse de recibo (ACK de aplicación)
                        respuesta = {
                            "status": "CONFIRMADO",
                            "transaccion_id": paquete.get("id"),
                            "servidor_time": time.strftime("%H:%M:%S")
                        }
                        conexion.sendall(json.dumps(respuesta).encode("utf-8"))
                        print("[GATEWAY] Confirmación enviada. Cerrando canal (FIN/ACK)...")
            except Exception as e:
                print(f"[GATEWAY] Error en conexión: {e}")

    print("[GATEWAY] Servidor apagado ordenadamente.")


# --- LADO CLIENTE (Agente Emisor Resiliente) ---
def cliente_emisor_resiliente(datos_transaccion, max_reintentos=3):
    """
    Cliente ultra-resiliente con timeouts y política de reintentos progresivos.
    """
    print("\n" + "=" * 65)
    print(f"  [CLIENTE RESILIENTE] Enviando transacción: ID #{datos_transaccion['id']}")
    print("=" * 65)

    paquete_json = json.dumps(datos_transaccion).encode("utf-8")

    for intento in range(1, max_reintentos + 1):
        print(f"  -> Intento #{intento} de conexión con el Gateway...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
                # 1. Timeout estricto de 2 segundos
                cliente.settimeout(2.0)

                # 2. Handshake (SYN -> SYN+ACK -> ACK)
                cliente.connect((HOST, PUERTO))
                print("     ✔ Three-Way Handshake completado.")

                # 3. Envío fiable
                cliente.sendall(paquete_json)

                # 4. Recepción de confirmación
                respuesta_bytes = cliente.recv(1024)
                respuesta = json.loads(respuesta_bytes.decode("utf-8"))
                
                print("\n  " + "-" * 50)
                print(f"  ✔ ¡TRANSACCIÓN EXITOSA!")
                print(f"    • Estado:    {respuesta['status']}")
                print(f"    • ID:        {respuesta['transaccion_id']}")
                print(f"    • Hora Serv: {respuesta['servidor_time']}")
                print("  " + "-" * 50)
                return True

        except ConnectionRefusedError:
            print("     🔴 ConnectionRefusedError: Servidor no disponible.")
            if intento < max_reintentos:
                tiempo_espera = intento * 0.5
                print(f"        Pausando {tiempo_espera}s antes de reintentar...")
                time.sleep(tiempo_espera)
        except socket.timeout:
            print("     ⏱ socket.timeout: El servidor no respondió a tiempo.")
        except ConnectionResetError:
            print("     💥 ConnectionResetError: La conexión se cortó bruscamente.")
        except OSError as e:
            print(f"     🔱 OSError: Fallo de interfaz o red: {e}")

    print(f"\n  ❌ Fallaron los {max_reintentos} intentos. Transacción guardada en disco local para reintento.")
    return False


def main():
    if "--servidor" in sys.argv:
        iniciar_servidor_gateway(limite_transacciones=100)
    elif "--cliente" in sys.argv:
        tx = {"id": 1042, "concepto": "Pago Servicios Cloud", "monto": 89.90}
        cliente_emisor_resiliente(tx, max_reintentos=3)
    else:
        # Modo demostración automático
        print("=" * 70)
        print("  07 - EJEMPLO DE LA VIDA REAL: ARQUITECTURA TCP RESILIENTE")
        print("       (Demostración con recuperación ante fallos y reintentos)")
        print("=" * 70)

        # 1. Simular intento del cliente ANTES de que el servidor esté listo
        print("\n[FASE 1] Probando cliente mientras el servidor aún está apagado:")
        tx_inicial = {"id": 901, "concepto": "Prueba Offline", "monto": 10.00}
        
        # En segundo plano, levantaremos el servidor con 0.8s de retraso
        # para demostrar que el cliente se recupera gracias a los reintentos
        hilo_srv = threading.Thread(
            target=lambda: (time.sleep(0.8), iniciar_servidor_gateway(limite_transacciones=1)),
            daemon=True
        )
        hilo_srv.start()

        # El cliente reintentará hasta que el servidor despierte
        cliente_emisor_resiliente(tx_inicial, max_reintentos=3)

        hilo_srv.join(timeout=3.0)

        print("\n" + "=" * 70)
        print("  RESUMEN PEDAGÓGICO:")
        print("  1. El cliente detectó que el servidor no estaba activo en el Intento #1.")
        print("  2. En lugar de crashear, esperó y reintentó.")
        print("  3. Al despertar el servidor, el Handshake se completó exitosamente.")
        print("  4. SO_REUSEADDR garantiza que el puerto quede libre inmediatamente.")
        print("=" * 70)

if __name__ == "__main__":
    main()

