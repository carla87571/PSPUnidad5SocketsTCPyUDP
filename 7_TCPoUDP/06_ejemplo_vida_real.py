"""
06_ejemplo_vida_real.py
=======================
EJEMPLO DE LA VIDA REAL: Sistema de Comunicación Híbrido TCP + UDP (Estilo Discord / Zoom)

ESCENARIO REAL:
---------------
En plataformas como Discord, Zoom, Microsoft Teams o Slack:
  1. El CHAT DE TEXTO, autenticación y envío de archivos usan TCP:
     - Un mensaje de texto ("La reunión es a las 4:00 PM") NUNCA puede perderse ni llegar desordenado.
     - Requiere la carta certificada (TCP).
  2. El CANAL DE VOZ y AUDIO EN VIVO usan UDP:
     - Cada 20 milisegundos se envía un micro-paquete con ondas de sonido comprimidas.
     - Si la red WiFi pierde un micro-paquete de voz, es preferible un micro-silencio imperceptible
       antes que congelar la conversación esperando retransmisiones.
     - Requiere la velocidad del avión de papel (UDP).

ARQUITECTURA DEL SCRIPT:
------------------------
  • Servidor Híbrido:
      - Escucha en el puerto TCP 9200 (Chat de texto fiable).
      - Escucha en el puerto UDP 9201 (Streaming de voz en tiempo real).
  • Cliente Híbrido:
      - Abre un socket TCP para enviar mensajes de texto y recibir acuse.
      - Abre un socket UDP para transmitir ráfagas de audio a alta velocidad.

CÓMO EJECUTAR ESTE SCRIPT:
--------------------------
1. Modo demostración automático (todo en una sola terminal):
      python3 06_ejemplo_vida_real.py

2. Modo con dos consolas separadas:
      Terminal 1: python3 06_ejemplo_vida_real.py --servidor
      Terminal 2: python3 06_ejemplo_vida_real.py --cliente
"""

import json
import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PUERTO_TCP_CHAT = 9200
PUERTO_UDP_VOZ = 9201

# --- LADO SERVIDOR HÍBRIDO ---
def servidor_hibrido_tcp_chat(limite=2):
    """Atiende mensajes de chat fiables por TCP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv_tcp:
        srv_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv_tcp.bind((HOST, PUERTO_TCP_CHAT))
        srv_tcp.listen(5)

        for _ in range(limite):
            conn, addr = srv_tcp.accept()
            with conn:
                datos = conn.recv(1024)
                if datos:
                    msg = json.loads(datos.decode("utf-8"))
                    print(f"  [SRV-TCP / CHAT] Mensaje fiable de {msg['usuario']}: \"{msg['texto']}\"")
                    # Respondemos con confirmación garantizada
                    ack = json.dumps({"status": "ENTREGADO", "id": msg["id"]})
                    conn.sendall(ack.encode("utf-8"))

def servidor_hibrido_udp_voz(limite_paquetes=6):
    """Recibe paquetes de audio en tiempo real por UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv_udp:
        srv_udp.bind((HOST, PUERTO_UDP_VOZ))

        for _ in range(limite_paquetes):
            datos, direccion = srv_udp.recvfrom(512)
            paquete_audio = json.loads(datos.decode("utf-8"))
            print(f"  [SRV-UDP / VOZ]  Audio frame #{paquete_audio['seq']} de {paquete_audio['usuario']} ({len(datos)} B)")

def iniciar_servidor_completo():
    print("\n" + "=" * 65)
    print(f"  [SERVIDOR HÍBRIDO] Iniciado:")
    print(f"  • Canal TCP (Chat / Texto): {HOST}:{PUERTO_TCP_CHAT}")
    print(f"  • Canal UDP (Voz / Audio):  {HOST}:{PUERTO_UDP_VOZ}")
    print("=" * 65)

    h_tcp = threading.Thread(target=servidor_hibrido_tcp_chat, kwargs={"limite": 100}, daemon=True)
    h_udp = threading.Thread(target=servidor_hibrido_udp_voz, kwargs={"limite_paquetes": 1000}, daemon=True)
    h_tcp.start()
    h_udp.start()

    print("[SERVIDOR] Presiona Ctrl+C para salir.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando servicios...")


# --- LADO CLIENTE HÍBRIDO ---
def cliente_enviar_texto_tcp(usuario, texto):
    """Envía un mensaje de texto por el canal TCP garantizado."""
    print(f"\n[CLIENTE -> TCP] Enviando mensaje de texto garantizado...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.settimeout(3.0)
        c.connect((HOST, PUERTO_TCP_CHAT))
        
        paquete = {"id": 1, "usuario": usuario, "texto": texto}
        c.sendall(json.dumps(paquete).encode("utf-8"))
        
        confirmacion = c.recv(1024)
        resp = json.loads(confirmacion.decode("utf-8"))
        print(f"  ✔ [TCP ACK] Servidor confirmó entrega del mensaje: {resp['status']}")

def cliente_enviar_voz_udp(usuario, paquetes=4):
    """Transmite ráfagas de audio por el canal UDP ultra-rápido."""
    print(f"\n[CLIENTE -> UDP] Transmitiendo {paquetes} micro-paquetes de voz (20ms cada uno)...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        for seq in range(1, paquetes + 1):
            paquete = {
                "usuario": usuario,
                "seq": seq,
                "codec": "Opus-Audio",
                "duracion_ms": 20,
                "volumen_db": -12.4
            }
            c.sendto(json.dumps(paquete).encode("utf-8"), (HOST, PUERTO_UDP_VOZ))
            time.sleep(0.05)
    print("  ✔ [UDP VOZ] Ráfaga de audio enviada a máxima velocidad.")


def modo_demostracion():
    """Ejecuta demostración automática con ambos canales activos."""
    print("=" * 75)
    print("  06 - EJEMPLO DE LA VIDA REAL: ARQUITECTURA HÍBRIDA TCP + UDP")
    print("       (Demostración simultánea: Chat fiable + Audio VoIP)")
    print("=" * 75)

    # Iniciar servidores en segundo plano
    h_tcp = threading.Thread(target=servidor_hibrido_tcp_chat, kwargs={"limite": 1}, daemon=True)
    h_udp = threading.Thread(target=servidor_hibrido_udp_voz, kwargs={"limite_paquetes": 4}, daemon=True)
    h_tcp.start()
    h_udp.start()
    time.sleep(0.2)

    # 1. Cliente envía mensaje de chat por TCP
    cliente_enviar_texto_tcp("Carla_Dev", "Hola equipo, ¿me escuchan bien en la sala de voz?")
    time.sleep(0.2)

    # 2. Cliente envía audio de voz por UDP
    cliente_enviar_voz_udp("Carla_Dev", paquetes=4)

    h_tcp.join(timeout=2.0)
    h_udp.join(timeout=2.0)

    print("\n" + "=" * 75)
    print("  RESUMEN PEDAGÓGICO DE LA DECISIÓN ARQUITECTÓNICA:")
    print("  • TCP para Texto:  Garantizó que no se perdiera ni una sola palabra.")
    print("  • UDP para Voz:    Transmitió micro-paquetes instantáneos sin demoras.")
    print("  • ¡Las mejores aplicaciones combinan ambos protocolos inteligentemente!")
    print("=" * 75)

if __name__ == "__main__":
    if "--servidor" in sys.argv:
        iniciar_servidor_completo()
    elif "--cliente" in sys.argv:
        cliente_enviar_texto_tcp("Usuario_Consola", "Probando conexión de texto")
        cliente_enviar_voz_udp("Usuario_Consola", paquetes=5)
    else:
        modo_demostracion()

