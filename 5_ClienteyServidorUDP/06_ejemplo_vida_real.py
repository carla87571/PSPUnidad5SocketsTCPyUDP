"""
06_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Servidor de Sincronización en Tiempo Real para Videojuegos (Game Server UDP)

ESCENARIO REAL:
---------------
En videojuegos multijugador online (como Rocket League, Fortnite, Call of Duty o FIFA):
  • Cada jugador envía su posición (X, Y, Z) y velocidad entre 30 y 60 veces por segundo.
  • ¿Por qué UDP y NO TCP?
    Si un paquete con la posición de hace 16 milisegundos se pierde en la red WiFi,
    ¡no tiene ningún sentido retransmitirlo! Para cuando llegue, el jugador ya se habrá movido.
    TCP provocaría "lag spikes" (tirones) congelando la pantalla para esperar el paquete perdido.
  • En UDP, se descarta el paquete perdido y se procesa inmediatamente el siguiente más reciente.

CARACTERÍSTICAS DEL CÓDIGO:
---------------------------
  1. Servidor UDP que escucha en un solo puerto y recibe paquetes de múltiples jugadores
     sin necesidad de accept() ni de hilos por jugador.
  2. Clientes UDP que transmiten coordenadas continuamente con sendto().
  3. Formato compacto JSON serializado a bytes.
  4. Control de tiempo y timeouts para no congelarse si el servidor se apaga.

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático (simula servidor y 2 jugadores en vivo):
      python3 06_ejemplo_vida_real.py

2. Modo con consolas separadas:
      Terminal 1: python3 06_ejemplo_vida_real.py --servidor
      Terminal 2: python3 06_ejemplo_vida_real.py --cliente "Gamer_Alpha"
      Terminal 3: python3 06_ejemplo_vida_real.py --cliente "Gamer_Beta"
"""

import json
import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PUERTO = 7777

# --- SERVIDOR DE VIDEOJUEGO UDP ---
def ejecutar_servidor_juego(limite_paquetes=6):
    """
    Servidor UDP que recibe las posiciones de todos los jugadores
    en un único socket sin conexiones ni bloqueos.
    """
    print("\n" + "=" * 65)
    print(f"  [SERVIDOR GAME UDP] Iniciando motor del mundo en {HOST}:{PUERTO}")
    print("=" * 65)

    tabla_posiciones = {}

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        # bind() para recibir todos los datagramas dirigidos a este puerto
        servidor.bind((HOST, PUERTO))
        print("[SERVIDOR] Escuchando datagramas de jugadores en tiempo real...")

        paquetes_recibidos = 0
        while paquetes_recibidos < limite_paquetes:
            # 1. recvfrom() entrega datos y la tupla (IP, puerto) de quien mandó el datagrama
            datos_bytes, direccion_jugador = servidor.recvfrom(2048)
            paquetes_recibidos += 1

            paquete = json.loads(datos_bytes.decode("utf-8"))
            jugador_id = paquete["jugador"]
            pos = paquete["posicion"]

            # Actualizamos el estado del mundo
            tabla_posiciones[jugador_id] = pos

            print(f"[SERVIDOR] 🎮 Frame #{paquetes_recibidos} de {jugador_id} ({direccion_jugador[1]}): "
                  f"X={pos['x']}, Y={pos['y']}, Vel={pos['vel']} km/h")

            # 2. Devolvemos el estado actualizado del mundo ("World State Snapshot")
            snapshot = {
                "tipo": "WORLD_UPDATE",
                "jugadores_activos": len(tabla_posiciones),
                "confirmado_frame": paquete.get("frame_id"),
                "servidor_timestamp": time.time()
            }
            servidor.sendto(json.dumps(snapshot).encode("utf-8"), direccion_jugador)

    print("\n[SERVIDOR] Límite de la demo alcanzado. Servidor UDP detenido.")


# --- CLIENTE JUGADOR UDP ---
def ejecutar_cliente_jugador(nombre_jugador="Jugador_1", frames=3):
    """
    Cliente UDP que simula un videojuego enviando coordenadas a alta velocidad.
    """
    print(f"\n[CLIENTE {nombre_jugador}] Conectando al servidor UDP de la partida...")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        # Buena práctica: timeout para que el cliente no se cuelgue si el servidor se apaga
        cliente.settimeout(2.0)

        for frame in range(1, frames + 1):
            # Coordenadas simuladas en movimiento
            posicion = {
                "x": 100 + (frame * 5),
                "y": 200 + (frame * 2),
                "vel": 45.0 + frame
            }
            paquete = {
                "jugador": nombre_jugador,
                "frame_id": frame,
                "posicion": posicion,
                "client_time": time.time()
            }

            datos_a_enviar = json.dumps(paquete).encode("utf-8")
            
            # Envío del datagrama UDP: el destino viaja en cada llamada a sendto()
            cliente.sendto(datos_a_enviar, (HOST, PUERTO))

            try:
                # Recibimos el snapshot del servidor
                datos_recibidos, _ = cliente.recvfrom(2048)
                snapshot = json.loads(datos_recibidos.decode("utf-8"))
                print(f"  [{nombre_jugador}] ✔ Frame {frame} sincronizado con servidor. "
                      f"Jugadores en partida: {snapshot['jugadores_activos']}")
            except TimeoutError:
                print(f"  [{nombre_jugador}] ⏱ Paquete {frame} perdido en la red (UDP continuará sin frenar).")

            time.sleep(0.1)  # Simula 10 actualizaciones por segundo en la demo


def modo_demostracion():
    """Ejecuta demostración automática con el servidor y 2 jugadores en paralelo."""
    print("=" * 70)
    print("  06 - EJEMPLO DE LA VIDA REAL: SINCRONIZACIÓN DE VIDEOJUEGOS CON UDP")
    print("       (Demostración con 2 jugadores transmitiendo coordenadas)")
    print("=" * 70)

    # 1. Iniciar servidor UDP en segundo plano
    hilo_srv = threading.Thread(
        target=ejecutar_servidor_juego,
        kwargs={"limite_paquetes": 6},
        daemon=True
    )
    hilo_srv.start()
    time.sleep(0.2)

    # 2. Iniciar 2 jugadores simultáneos en hilos
    hilo_j1 = threading.Thread(target=ejecutar_cliente_jugador, args=("Faker_Mid", 3), daemon=True)
    hilo_j2 = threading.Thread(target=ejecutar_cliente_jugador, args=("Caps_Top", 3), daemon=True)

    hilo_j1.start()
    hilo_j2.start()

    hilo_j1.join()
    hilo_j2.join()
    hilo_srv.join(timeout=2.0)

    print("\n" + "=" * 70)
    print("  RESUMEN PEDAGÓGICO DE UDP EN TIEMPO REAL:")
    print("  1. No hubo handshake: el primer frame se envió instantáneamente.")
    print("  2. El servidor atendió a AMBOS jugadores por el MISMO socket y puerto.")
    print("  3. Si un paquete se retrasa o pierde, el juego no se congela: procesa el siguiente.")
    print("  4. recvfrom() aportó automáticamente la IP y puerto de cada jugador para responder.")
    print("=" * 70)

if __name__ == "__main__":
    if "--servidor" in sys.argv:
        ejecutar_servidor_juego(limite_paquetes=1000)
    elif "--cliente" in sys.argv:
        nick = sys.argv[2] if len(sys.argv) > 2 else "Jugador_Pro"
        ejecutar_cliente_jugador(nombre_jugador=nick, frames=20)
    else:
        modo_demostracion()

