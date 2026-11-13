"""
04_los_males_de_udp_y_limite_tamano.py
======================================
Diapositiva de referencia: Diapositiva 7 ("Datagramas: cada envío es un mundo aparte")

LOS 4 "MALES" DE UDP:
---------------------
Al no tener estado ni control de flujo, UDP sufre de 4 características:

  1. PÉRDIDA:
     -> No hay confirmación (ACK). Si un router o antena WiFi descarta un paquete,
        se pierde para siempre.

  2. DESORDEN:
     -> No hay números de secuencia. Si envías A, B y C, pueden llegar en orden C, A y B
        porque cada paquete viaja por rutas distintas en la red.

  3. DUPLICADOS:
     -> En redes inalámbricas, un mismo datagrama puede retransmitirse por rebote y llegar dos veces.

  4. TAMAÑO MÁXIMO DE CARGA ÚTIL (Payload):
     -> El campo de longitud de IPv4 tiene 16 bits (máximo 65.535 bytes).
     -> Restamos:
          65.535 bytes (Total paquete IP)
        -     20 bytes (Cabecera estándar IPv4)
        -      8 bytes (Cabecera UDP)
        --------------------------------------
        = 65.507 bytes de datos útiles máximos.
     -> Si intentas enviar más de 65.507 bytes en un solo datagrama, el SO lanza:
        OSError: [Errno 90] Message too long

¿POR QUÉ ELEGIR UDP ENTONCES?
-----------------------------
Porque esos "males" son el precio de la VELOCIDAD: sin handshake de 3 vías ni esperas
de confirmación, cada paquete cuesta el mínimo absoluto de latencia.
"""

import socket
import threading
import time

HOST, PUERTO = "127.0.0.1", 5012

def receptor_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PUERTO))
        while True:
            datos, _ = s.recvfrom(65535)
            if datos == b"FIN":
                break
            print(f"    [Servidor] Recibido: {datos.decode() if len(datos) < 50 else f'{len(datos)} bytes'}")

def main():
    print("=" * 70)
    print("  04 - LOS MALES DE UDP Y EL LÍMITE DE TAMAÑO (Diapositiva 7)")
    print("=" * 70)

    # Iniciar receptor de apoyo
    threading.Thread(target=receptor_udp, daemon=True).start()
    time.sleep(0.2)

    # 1. Código de 'cinco_aviones.py' (Envío de datagramas independientes)
    print("\n[1] ENVIANDO 5 DATAGRAMAS INDEPENDIENTES ('cinco_aviones.py'):")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        for i in range(1, 6):
            mensaje = f"Mensaje #{i}".encode("utf-8")
            cliente.sendto(mensaje, (HOST, PUERTO))
            time.sleep(0.1)

    # 2. Experimento con el tamaño máximo de un datagrama UDP
    print("\n[2] EL LÍMITE DE TAMAÑO: 65.507 BYTES:")
    print("    Cálculo: 65.535 - 20 (cabecera IP) - 8 (cabecera UDP) = 65.507 bytes útiles.")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        # Prueba A: Enviar un paquete dentro del límite (ej. 30.000 bytes)
        datos_validos = b"X" * 30000
        cliente.sendto(datos_validos, (HOST, PUERTO))
        print("    ✔ Datagrama de 30.000 bytes enviado con éxito.")

        # Prueba B: Intentar enviar más de 65.507 bytes (ej. 70.000 bytes)
        datos_excesivos = b"Y" * 70000
        print("\n    • Intentando enviar datagrama de 70.000 bytes (supera el límite)...")
        try:
            cliente.sendto(datos_excesivos, (HOST, PUERTO))
            print("    Enviado (inesperado).")
        except OSError as e:
            print(f"\n    ❌ ¡OSError capturado tal como enseña la Diapositiva 7!")
            print(f"    Tipo de error: {type(e).__name__}")
            print(f"    Detalle:       {e}")
            print("    💡 Ningún datagrama UDP puede superar los 65.507 bytes de carga.")

        # Señal de fin
        cliente.sendto(b"FIN", (HOST, PUERTO))

    print("\n" + "=" * 70)
    print("  LECCIÓN: Para enviar archivos grandes (fotos, zip), usa TCP.")
    print("  Para ráfagas cortas y rápidas (coordenadas, métricas), usa UDP.")
    print("=" * 70)

if __name__ == "__main__":
    main()

