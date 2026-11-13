"""
02_el_cliente_udp.py
====================
Diapositiva de referencia: Diapositiva 2 ("El cliente UDP: sendto() y recvfrom()")

EL CÓDIGO EXACTO DE LA DIAPOSITIVA 2:
-------------------------------------
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.sendto(b"Hola UDP!", (HOST, PORT))
        datos, _ = cliente.recvfrom(1024)
        print(f"Respuesta: {datos.decode()}")

PUNTOS CLAVE:
-------------
  1. socket.SOCK_DGRAM:
     -> Selecciona el protocolo UDP en lugar de TCP.
  2. cliente.sendto(datos_en_bytes, (HOST, PORT)):
     -> No existe connect(). En cada envío indicas a qué máquina y puerto va el paquete.
  3. datos, direccion = cliente.recvfrom(1024):
     -> Devuelve una tupla de dos elementos: los bytes recibidos y la tupla de dirección de quien te respondió.
     -> En la diapositiva, la dirección se descarta usando la variable '_' porque ya sabemos a quién le hablamos.
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5010

def mini_servidor_eco_udp():
    """Servidor de apoyo para que el cliente reciba respuesta inmediata."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        # Espera un datagrama y devuelve el eco
        datos, direccion_remota = s.recvfrom(1024)
        s.sendto(b"Recibido desde servidor UDP: " + datos, direccion_remota)

def main():
    print("=" * 70)
    print("  02 - EL CLIENTE UDP MÍNIMO (sendto() y recvfrom())")
    print("=" * 70)

    # Iniciamos el servidor de soporte en segundo plano
    threading.Thread(target=mini_servidor_eco_udp, daemon=True).start()
    time.sleep(0.2)

    print("\n[EJECUTANDO EL CÓDIGO DE LA DIAPOSITIVA 2]:\n")

    # --- INICIO DEL CÓDIGO DE LA DIAPOSITIVA 2 ---
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        # 1. Enviar datagrama con la tupla de destino integrada
        cliente.sendto(b"Hola UDP!", (HOST, PORT))
        print("  Paso 1: sendto(b'Hola UDP!', (HOST, PORT)) ejecutado.")

        # 2. Recibir datagrama (obtenemos datos y descartamos la dirección con _)
        datos, _ = cliente.recvfrom(1024)
        print("  Paso 2: recvfrom(1024) recibido.")

        # 3. Mostrar la respuesta decodificada
        print(f"\n  👉 Respuesta: {datos.decode()}")
    # --- FIN DEL CÓDIGO DE LA DIAPOSITIVA 2 ---

    print("\n" + "=" * 70)
    print("  OBSERVACIÓN:")
    print("  No hubo ningún saludo previo (SYN/ACK). ¡El datagrama salió disparado")
    print("  en la primera instrucción!")
    print("=" * 70)

if __name__ == "__main__":
    main()

