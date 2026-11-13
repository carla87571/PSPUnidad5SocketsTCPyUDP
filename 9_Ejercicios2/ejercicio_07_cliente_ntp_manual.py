"""
=============================================================================
EJERCICIO 7: CLIENTE NTP MANUAL (UDP)
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 02 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"Crea un cliente UDP que obtenga la hora actual desde pool.ntp.org usando el
puerto 123. Envía un paquete de 48 bytes (el primero con valor \\x1b y el resto \\0).
Extrae el timestamp de los bytes 40 a 43 con struct.unpack('!I', ...) y ajústalo
restando 2208988800 para convertirlo a hora Unix.

💡 Pista: añade s.settimeout(5) antes del recvfrom(): si la respuesta se
pierde (UDP), lanza una excepción en lugar de bloquearse para siempre."

CONCEPTOS CLAVE:
1. Protocolo NTP (Network Time Protocol - RFC 5905):
   Protocolo de Capa de Aplicación sobre UDP (puerto 123) para sincronizar relojes.
2. Cabecera NTP (48 bytes):
   - Primer byte 0x1B (binario: 00 011 011):
     * LI = 00 (Leap Indicator: sin advertencia)
     * VN = 011 (Versión 3 de NTP)
     * Mode = 011 (Modo 3: Cliente)
   - Bytes 40-43: Timestamp de transmisión del servidor (segundos desde 1 de enero de 1900).
3. Diferencia época NTP vs Unix:
   NTP cuenta desde 1900; Unix cuenta desde 1970.
   La diferencia exacta son 70 años: 2.208.988.800 segundos.
4. struct.unpack('!I', data[40:44]):
   Desempaqueta un entero de 32 bits sin signo en orden Big-Endian (Network Byte Order '!').
=============================================================================
"""

import socket
import struct
import datetime
import sys
import time
import threading

SERVIDOR_NTP_DEFAULT = "pool.ntp.org"
PUERTO_NTP_DEFAULT = 123
OFFSET_NTP_UNIX = 2208988800  # Segundos entre 01/01/1900 y 01/01/1970


def consultar_hora_ntp(servidor: str = SERVIDOR_NTP_DEFAULT, puerto: int = PUERTO_NTP_DEFAULT):
    """
    Envía petición NTP mediante UDP y extrae la fecha y hora oficial.
    """
    print("=" * 70)
    print("        ⏰ EJERCICIO 7: CLIENTE NTP MANUAL (UDP)")
    print("=" * 70)
    print(f"[*] Conectando al servidor NTP: {servidor}:{puerto}")

    # 1. Crear el paquete de petición NTP de 48 bytes
    # El primer byte con valor 0x1B (\x1b) y el resto ceros (\0)
    paquete_ntp = bytearray(48)
    paquete_ntp[0] = 0x1B  # Mode = 3 (Client), Version = 3

    # 2. Crear socket UDP (SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 3. Pista: Añadir timeout de 5 segundos antes de recvfrom()
    s.settimeout(5.0)

    try:
        print("[>] Enviando datagrama de 48 bytes a pool.ntp.org...")
        s.sendto(paquete_ntp, (servidor, puerto))

        print("[*] Esperando respuesta del servidor NTP...")
        datos, addr = s.recvfrom(1024)
        print(f"[+] ¡Respuesta recibida desde {addr} ({len(datos)} bytes)!")

        # 4. Pista: Extraer el timestamp de los bytes 40 a 43 con struct.unpack('!I', ...)
        # En Python, el slice para los bytes 40, 41, 42 y 43 es datos[40:44]
        # '!I' indica: '!' = Network Byte Order (Big-Endian), 'I' = Unsigned Integer de 32 bits
        segundos_ntp = struct.unpack("!I", datos[40:44])[0]
        print(f"\n[+] Timestamp bruto NTP (desde 1900): {segundos_ntp} segundos")

        # 5. Pista: Ajustarlo restando 2208988800 para convertirlo a hora Unix
        segundos_unix = segundos_ntp - OFFSET_NTP_UNIX
        print(f"[+] Timestamp Unix (desde 1970):       {segundos_unix} segundos")

        # 6. Convertir a fecha y hora legible
        fecha_utc = datetime.datetime.fromtimestamp(segundos_unix, tz=datetime.timezone.utc)
        fecha_local = fecha_utc.astimezone()

        print("-" * 70)
        print(f"🌍 HORA OFICIAL SINCRONIZADA (UTC):   {fecha_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"🏠 HORA OFICIAL LOCAL:                 {fecha_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print("-" * 70)
        return True

    finally:
        s.close()
        print("[*] Socket UDP cerrado.")


def servidor_ntp_mock_local(puerto: int = 12300):
    """Servidor UDP mock para pruebas en entornos sin salida a internet externa."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(("127.0.0.1", puerto))
            datos, addr = s.recvfrom(1024)
            # Construir respuesta NTP de 48 bytes con el timestamp actual del sistema
            resp = bytearray(48)
            resp[0] = 0x1C  # Server response, VN=3
            ahora_ntp = int(time.time()) + OFFSET_NTP_UNIX
            struct.pack_into("!I", resp, 40, ahora_ntp)
            s.sendto(resp, addr)
    except Exception:
        pass


def ejecutar_con_respaldo():
    """
    Intenta consultar pool.ntp.org en internet. Si falla por falta de red,
    utiliza un servidor NTP mock local para demostrar el desempaquetado de struct.
    """
    try:
        consultar_hora_ntp(SERVIDOR_NTP_DEFAULT, PUERTO_NTP_DEFAULT)
    except (socket.gaierror, socket.timeout, OSError) as err:
        print(f"\n[ℹ️ Aviso]: No hay conexión a internet externa ({err}).")
        print("[*] Activando servidor NTP local de prueba para verificar struct.unpack...")

        puerto_local = 12300
        hilo = threading.Thread(target=servidor_ntp_mock_local, args=(puerto_local,), daemon=True)
        hilo.start()
        time.sleep(0.15)
        consultar_hora_ntp("127.0.0.1", puerto_local)
        hilo.join(timeout=1.0)


if __name__ == "__main__":
    ejecutar_con_respaldo()

