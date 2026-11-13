"""
04_cliente_ntp_hora_internet.py
===============================
Diapositivas de referencia:
  • Diapositiva 5 ("NTP: sincronizar relojes con UDP - El reloj de Internet")
  • Diapositiva 6 ("Cómo funciona el cliente NTP: Tres detalles que importan")

¿QUÉ ES NTP (Network Time Protocol)?
-----------------------------------
Es el protocolo que usan todos los ordenadores y móviles del mundo para sincronizar
su reloj con servidores atómicos.
Usa el puerto 123 sobre UDP.

¿POR QUÉ NTP USA UDP Y NO TCP?
------------------------------
1. En TCP, el Three-Way Handshake introduce retardos variables (latencia asimétrica).
2. NTP envía datagramas UDP ligeros; mide el tiempo de ida y vuelta para restar el retardo de la red.
3. Si un paquete se pierde, ¡no pasa nada! Se mandan varios y se promedian estadísticamente.

LOS TRES DETALLES CLAVE DEL CÓDIGO (Diapositiva 6):
--------------------------------------------------
  1. b"\\x1b" + 47 * b"\\0":
     -> 48 bytes en total.
     -> \\x1b en binario es 00011011:
        * Versión NTP = 3 (bits centrales).
        * Modo = 3 (Cliente, bits inferiores).
     -> Los 47 bytes restantes son relleno en ceros.
  2. settimeout(5):
     -> Imprescindible en UDP para evitar bloqueo si el servidor no responde.
  3. struct.unpack("!I", datos[40:44])[0]:
     -> Lee el timestamp de 4 bytes en Network Byte Order (Big-Endian).
  4. Restar 2208988800:
     -> La época NTP comienza el 1 de enero de 1900.
     -> La época Unix (POSIX) comienza el 1 de enero de 1970.
     -> La diferencia entre 1900 y 1970 son exactamente 2.208.988.800 segundos.
"""

import socket
import struct
import threading
import time

HOST_LOCAL, PUERTO_LOCAL = "127.0.0.1", 5123

def servidor_ntp_local():
    """Servidor NTP/SNTP local que responde con la hora del sistema para pruebas autónomas."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST_LOCAL, PUERTO_LOCAL))
        paquete_cliente, direccion = s.recvfrom(1024)
        
        # Obtenemos la hora Unix actual y la convertimos a época NTP (+ 2208988800)
        hora_unix_actual = int(time.time())
        hora_ntp = hora_unix_actual + 2208988800

        # Respuesta de 48 bytes con el timestamp en las posiciones 40 a 44
        # Byte 0: 0x1c = Versión 3, Modo 4 (Servidor)
        respuesta = bytearray(48)
        respuesta[0] = 0x1c
        respuesta[40:44] = struct.pack("!I", hora_ntp)
        
        s.sendto(bytes(respuesta), direccion)

def consultar_hora_ntp(servidor, puerto):
    """Implementación exacta de la Diapositiva 5."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2.0)  # 2 segundos de timeout de seguridad

        # 1. Construir paquete de 48 bytes en modo cliente
        paquete = b"\x1b" + 47 * b"\0"
        
        # 2. Enviar por UDP
        s.sendto(paquete, (servidor, puerto))
        
        # 3. Recibir datagrama de respuesta
        datos, _ = s.recvfrom(1024)
        
        # 4. Desempaquetar timestamp en bytes 40-43 con Big-Endian (!I)
        tiempo_ntp = struct.unpack("!I", datos[40:44])[0]
        
        # 5. Convertir época NTP (1900) a época Unix (1970)
        DIFERENCIA_EPOCAS = 2208988800
        tiempo_unix = tiempo_ntp - DIFERENCIA_EPOCAS
        return tiempo_unix

def main():
    print("=" * 70)
    print("  04 - CLIENTE NTP: SINCRONIZANDO RELOJES CON UDP Y struct")
    print("=" * 70)

    # 1. Levantamos el servidor NTP local de apoyo
    threading.Thread(target=servidor_ntp_local, daemon=True).start()
    time.sleep(0.2)

    # 2. Ejecutamos la consulta NTP
    print(f"\n[1] ENVIANDO DATAGRAMA UDP A SERVIDOR NTP ({HOST_LOCAL}:{PUERTO_LOCAL})...")
    segundos_unix = consultar_hora_ntp(HOST_LOCAL, PUERTO_LOCAL)

    # 3. Formateamos la hora en texto legible
    hora_legible = time.ctime(segundos_unix)

    print("\n[2] RESULTADO DE LA SINCRONIZACIÓN:")
    print(f"    • Timestamp Unix recuperado: {segundos_unix}")
    print(f"    • Fecha y Hora sincronizada: {hora_legible}")

    print("\n" + "=" * 70)
    print("  RESUMEN PEDAGÓGICO (Diapositivas 5 y 6):")
    print("  • Primer byte '\\x1b' activa el modo cliente.")
    print("  • '!I' lee el entero de 4 bytes respetando el Network Byte Order.")
    print("  • Se restan 2.208.988.800 segundos para ajustar la época 1900 -> 1970.")
    print("=" * 70)

if __name__ == "__main__":
    main()

