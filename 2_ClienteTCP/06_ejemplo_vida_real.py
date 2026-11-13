"""
06_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Terminal Punto de Venta (POS) / Cliente de Pasarela de Pagos

ESCENARIO REAL:
---------------
En un restaurante, tienda o supermercado, el datáfono o terminal de cobro (POS)
es un CLIENTE TCP. Cada vez que pagas:
  1. El cliente inicia la conexión con el servidor bancario de autorizaciones.
  2. Establece un timeout estricto (ej. 3 segundos): si la red falla, no puede dejar al cajero colgado.
  3. Envía los datos de la transacción en bytes garantizados con sendall().
  4. Espera la respuesta de autorización bancaria con recv().
  5. Cierra la conexión de forma segura y emite el recibo.

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático (todo en una sola terminal):
      python3 06_ejemplo_vida_real.py

2. Modo con dos terminales separadas:
      Terminal 1 (Servidor bancario): python3 06_ejemplo_vida_real.py --servidor
      Terminal 2 (Terminal POS):      python3 06_ejemplo_vida_real.py --cliente
"""

import json
import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PUERTO = 5050

# --- CÓDIGO DEL CLIENTE TCP (Terminal Punto de Venta) ---
def ejecutar_cliente_pos(transaccion):
    """
    Representa el terminal de cobro con tarjeta (Cliente TCP).
    Aplica todos los conceptos del bloque:
      - Creación del socket TCP
      - Salida de emergencia con timeout
      - Manejo de ConnectionRefusedError
      - Envío fiable con sendall()
      - Recepción con recv()
      - Cierre seguro con with
    """
    print("\n" + "=" * 60)
    print("  [TERMINAL POS] INICIANDO PROCESO DE COBRO CON TARJETA")
    print("=" * 60)
    print(f"  • Comercio:     {transaccion['comercio']}")
    print(f"  • Tarjeta:      {transaccion['tarjeta']}")
    print(f"  • Importe:      ${transaccion['monto']:.2f}")

    # 1. Crear el socket TCP (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        
        # 2. Configurar timeout para evitar bloqueos eternos si el banco no responde
        TIMEOUT_SEGUNDOS = 3.0
        cliente.settimeout(TIMEOUT_SEGUNDOS)
        print(f"\n  [Paso 1] Timeout de seguridad configurado a {TIMEOUT_SEGUNDOS}s.")

        try:
            # 3. Conectar al servidor bancario (dispara el Three-Way Handshake)
            print(f"  [Paso 2] Conectando a pasarela bancaria en ({HOST}:{PUERTO})...")
            cliente.connect((HOST, PUERTO))
            print("  [Paso 2] ✔ ¡Handshake completado! Conexión segura establecida.")

            # 4. Serializar datos a JSON y codificar a BYTES con .encode()
            mensaje_json = json.dumps(transaccion)
            mensaje_bytes = mensaje_json.encode("utf-8")

            # 5. Enviar con sendall() para garantizar el envío íntegro de todos los bytes
            print(f"  [Paso 3] Enviando paquete de cobro ({len(mensaje_bytes)} bytes) con sendall()...")
            cliente.sendall(mensaje_bytes)

            # 6. Esperar la respuesta del banco con recv(1024)
            print("  [Paso 4] Esperando confirmación de la pasarela bancaria...")
            respuesta_bytes = cliente.recv(1024)

            # Si recv devuelve b'', el servidor cerró inesperadamente
            if not respuesta_bytes:
                print("  ❌ La pasarela bancaria cerró la conexión sin responder.")
                return

            # 7. Decodificar bytes a texto y convertir de JSON
            respuesta_texto = respuesta_bytes.decode("utf-8")
            respuesta_datos = json.loads(respuesta_texto)

            print("\n" + "-" * 60)
            print("  [RECIBO DE TRANSACCIÓN]")
            print(f"  • Estado:            {respuesta_datos['estado']}")
            print(f"  • Código Aprobación: {respuesta_datos['codigo_autorizacion']}")
            print(f"  • Mensaje:           {respuesta_datos['mensaje']}")
            print(f"  • Marca de tiempo:   {respuesta_datos['timestamp']}")
            print("-" * 60)

        except ConnectionRefusedError:
            print("\n  ❌ ERROR: No se puede contactar con la pasarela de pagos.")
            print("     (El servidor bancario está apagado o no responde en el puerto).")
        except TimeoutError:
            print(f"\n  ⏱ ERROR: Tiempo de espera agotado ({TIMEOUT_SEGUNDOS}s).")
            print("     La transacción fue cancelada por seguridad para no duplicar cargos.")
        except Exception as e:
            print(f"\n  ❌ Error imprevisto: {e}")
        finally:
            print("\n  [Paso 5] Conexión cerrada y recursos liberados con el 'with'.")


# --- CÓDIGO DEL SERVIDOR DE SOPORTE (Pasarela Bancaria) ---
def ejecutar_servidor_bancario(una_sola_transaccion=False):
    """Simula la pasarela bancaria de autorizaciones."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(1)

    try:
        while True:
            socket_pos, dir_pos = servidor.accept()
            with socket_pos:
                datos = socket_pos.recv(1024)
                if datos:
                    tx = json.loads(datos.decode("utf-8"))
                    
                    # Generamos autorización si el monto es positivo
                    aprobada = tx.get("monto", 0) > 0
                    respuesta = {
                        "estado": "APROBADA" if aprobada else "RECHAZADA",
                        "codigo_autorizacion": "AUTH-983421" if aprobada else "REJ-0001",
                        "mensaje": "Cobro efectuado correctamente" if aprobada else "Monto inválido",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    socket_pos.sendall(json.dumps(respuesta).encode("utf-8"))

            if una_sola_transaccion:
                break
    finally:
        servidor.close()


def main():
    if "--servidor" in sys.argv:
        print(f"[BANCO] Servidor de pagos escuchando en {HOST}:{PUERTO}...")
        ejecutar_servidor_bancario(una_sola_transaccion=False)
    elif "--cliente" in sys.argv:
        datos_prueba = {
            "comercio": "Cafetería La Central",
            "tarjeta": "**** **** **** 5821",
            "monto": 14.50
        }
        ejecutar_cliente_pos(datos_prueba)
    else:
        # Modo demostración automático
        print("=" * 70)
        print("  06 - EJEMPLO DE LA VIDA REAL: PASARELA DE PAGOS (POS)")
        print("       (Demostración automática del Cliente TCP)")
        print("=" * 70)

        # Iniciar pasarela bancaria en segundo plano
        hilo_banco = threading.Thread(
            target=ejecutar_servidor_bancario,
            kwargs={"una_sola_transaccion": True},
            daemon=True
        )
        hilo_banco.start()
        time.sleep(0.3)

        # Ejecutar la transacción desde el cliente
        datos_prueba = {
            "comercio": "Restaurante Gran Gourmet",
            "tarjeta": "**** **** **** 9142",
            "monto": 48.75
        }
        ejecutar_cliente_pos(datos_prueba)
        hilo_banco.join(timeout=2.0)

        print("\n" + "=" * 70)
        print("  RESUMEN PEDAGÓGICO DEL CLIENTE TCP:")
        print("  1. El cliente inicia la llamada activa (connect).")
        print("  2. Maneja ConnectionRefusedError por si el servidor no está disponible.")
        print("  3. Protege la operación con settimeout() para evitar bloqueos en recv().")
        print("  4. Envía la estructura codificada con sendall() garantizando entrega.")
        print("  5. Decodifica la respuesta de bytes a string y cierra ordenadamente.")
        print("=" * 70)

if __name__ == "__main__":
    main()

