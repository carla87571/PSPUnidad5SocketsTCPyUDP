"""
03_metodos_al_detalle.py
========================
Diapositiva de referencia: Diapositiva 4 ("Cada método, al detalle")

LOS MÉTODOS DEL CLIENTE BAJO LA LUPA:
-------------------------------------
1. socket(AF_INET, SOCK_STREAM):
   - Crea el socket TCP. Siempre se ejecuta primero.

2. connect((HOST, PORT)):
   - Dispara el 3-way handshake con el servidor.
   - ¡CUIDADO! Si nadie escucha en ese puerto, lanza ConnectionRefusedError.

3. sendall(datos) vs send(datos):
   - ¿Por qué sendall() y NO send()?
     * send(): Intenta enviar los bytes, pero si el buffer de red del SO se llena,
       puede enviar solo una parte y devolver cuántos bytes envió (ej. 500 de 1000).
       Te obligaría a programar un bucle manual para mandar el resto.
     * sendall(): Garantiza que se envían TODOS los bytes automáticamente. Si no puede,
       lanza un error. ¡Por eso SIEMPRE usamos sendall()!

4. recv(1024) y el buffer:
   - 1024 NO es el límite del mensaje: es el tamaño del BUFFER por lectura.
   - Si el servidor envía un mensaje de 3000 bytes, una sola llamada a recv(1024)
     recibirá los primeros 1024 bytes.
   - Para mensajes largos, se llama a recv() en un bucle y se van concatenando los fragmentos.
"""

import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5001

def servidor_mensaje_largo():
    """Servidor que envía un mensaje largo (2500 bytes) para demostrar cómo funciona el buffer."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            conn.recv(1024)  # Espera solicitud del cliente
            # Enviamos un mensaje de 2500 caracteres
            mensaje_largo = ("DATOS_IMPORTANTES_" * 150) + "FIN_DEL_MENSAJE"
            conn.sendall(mensaje_largo.encode("utf-8"))

def main():
    print("=" * 70)
    print("  03 - CADA MÉTODO AL DETALLE: sendall() Y EL BUFFER DE recv()")
    print("=" * 70)

    # 1. Tabla explicativa de la Diapositiva 4
    print("\n[1] RESUMEN DE MÉTODOS:")
    print("  • socket()       -> Crea el socket TCP (Siempre lo primero)")
    print("  • connect()      -> Establece conexión previa (Handshake)")
    print("  • sendall()      -> Envía TODOS los bytes (a diferencia de send)")
    print("  • recv(buffer)   -> Lee hasta N bytes del buffer del sistema")
    print("  • close() / with -> Libera recursos al terminar")

    # 2. Demostración práctica de recv() con buffer y concatenación
    print("\n[2] DEMOSTRACIÓN: Recibir un mensaje largo que supera el buffer de 1024 bytes")
    
    t = threading.Thread(target=servidor_mensaje_largo, daemon=True)
    t.start()
    time.sleep(0.2)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        cliente.sendall(b"DAME_DATOS")

        fragmentos = []
        numero_lectura = 1

        while True:
            # Leemos bloques de como máximo 1024 bytes
            bloque = cliente.recv(1024)
            if not bloque:
                # Cuando recv() devuelve b'' (bytes vacíos), significa que el servidor cerró la conexión
                print(f"    • Lectura {numero_lectura}: recv() devolvió b'' -> Fin de la transmisión.")
                break
            
            print(f"    • Lectura {numero_lectura}: recibidos {len(bloque)} bytes en este fragmento.")
            fragmentos.append(bloque)
            numero_lectura += 1

        # Concatenamos todos los fragmentos recibidos
        mensaje_completo = b"".join(fragmentos).decode("utf-8")
        print(f"\n    ✔ Tamaño total recibido: {len(mensaje_completo)} caracteres.")
        print(f"    ✔ El mensaje termina con: '{mensaje_completo[-14:]}'")

    print("\n" + "=" * 70)
    print("  CONCLUSIÓN PEDAGÓGICA:")
    print("  recv(1024) indica 'dame como máximo 1024 bytes ahora mismo'.")
    print("  Un mensaje mayor se reconstruye acumulando varios recv() hasta recibir b''.")
    print("=" * 70)

if __name__ == "__main__":
    main()

