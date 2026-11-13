"""
03_los_seis_retos_practicos.py
==============================
Diapositivas de referencia:
  • Diapositiva 8 ("Aprieta el lápiz: Seis retos sobre lo aprendido")
  • Diapositiva 9 ("Soluciones de los retos 1-3: Eco TCP, eco UDP y contador")
  • Diapositiva 10 ("Soluciones de los retos 4-6: Hora, timeout y comparativa")

LOS 6 RETOS DE PROGRAMACIÓN:
----------------------------
  Reto 1: Servidor Eco TCP.
  Reto 2: Servidor Eco UDP.
  Reto 3: Servidor Contador de letras (recibe una frase y responde la longitud).
  Reto 4: Servidor de Hora actual (devuelve HH:MM:SS al conectar).
  Reto 5: Cliente con timeout de 3 segundos ("Servidor no disponible").
  Reto 6: Comparativa de velocidad real: cronometrar 100 envíos en TCP vs UDP.
"""

import socket
import threading
import time

HOST = "127.0.0.1"
P_TCP_ECO = 9101
P_UDP_ECO = 9102
P_TCP_LETRAS = 9103
P_TCP_HORA = 9104
P_TCP_SPEED = 9105
P_UDP_SPEED = 9106

# --- RETO 3: CONTADOR DE LETRAS ---
def servidor_contador_letras():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, P_TCP_LETRAS))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            datos = conn.recv(1024).decode("utf-8")
            conteo = str(len(datos.strip()))
            conn.sendall(conteo.encode("utf-8"))

def cliente_contador_letras(frase):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((HOST, P_TCP_LETRAS))
        c.sendall(frase.encode("utf-8"))
        respuesta = c.recv(1024).decode("utf-8")
        return int(respuesta)

# --- RETO 4: SERVIDOR DE HORA ---
def servidor_hora():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, P_TCP_HORA))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            hora_actual = time.strftime("%H:%M:%S")
            conn.sendall(hora_actual.encode("utf-8"))

def cliente_hora():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((HOST, P_TCP_HORA))
        return c.recv(1024).decode("utf-8")

# --- RETO 5: CLIENTE CON TIMEOUT DE 3 SEGUNDOS ---
def cliente_con_timeout(puerto_inactivo=59990):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.settimeout(3.0)
        try:
            cli.connect((HOST, puerto_inactivo))
            cli.sendall(b"hola")
            return cli.recv(1024).decode("utf-8")
        except (socket.timeout, ConnectionRefusedError):
            return "Servidor no disponible"

# --- RETO 6: COMPARATIVA DE VELOCIDAD (100 MENSAJES TCP VS UDP) ---
def servidor_benchmark_tcp(mensajes=100):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, P_TCP_SPEED))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            for _ in range(mensajes):
                d = conn.recv(128)
                conn.sendall(b"ACK")

def servidor_benchmark_udp(mensajes=100):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, P_UDP_SPEED))
        for _ in range(mensajes):
            d, addr = s.recvfrom(128)
            s.sendto(b"ACK", addr)

def medir_velocidad_100_mensajes():
    N = 100
    # Medir TCP
    h_tcp = threading.Thread(target=servidor_benchmark_tcp, args=(N,), daemon=True)
    h_tcp.start()
    time.sleep(0.1)

    t0 = time.perf_counter()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c_tcp:
        c_tcp.connect((HOST, P_TCP_SPEED))
        for i in range(N):
            c_tcp.sendall(b"ping")
            c_tcp.recv(32)
    tiempo_tcp = (time.perf_counter() - t0) * 1000

    # Medir UDP
    h_udp = threading.Thread(target=servidor_benchmark_udp, args=(N,), daemon=True)
    h_udp.start()
    time.sleep(0.1)

    t0 = time.perf_counter()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c_udp:
        for i in range(N):
            c_udp.sendto(b"ping", (HOST, P_UDP_SPEED))
            c_udp.recvfrom(32)
    tiempo_udp = (time.perf_counter() - t0) * 1000

    return tiempo_tcp, tiempo_udp

def main():
    print("=" * 75)
    print("  03 - LOS SEIS RETOS PRÁCTICOS RESUELTOS (Diapositivas 8, 9 y 10)")
    print("=" * 75)

    # Retos 1 y 2 ya vistos en el archivo 02_practica_eco_cara_a_cara.py
    print("\n[Retos 1 y 2]: Servidores Eco TCP y UDP (Cubiertos en archivo 02).")

    # Reto 3: Contador de letras
    print("\n[Reto 3]: Contador de letras:")
    threading.Thread(target=servidor_contador_letras, daemon=True).start()
    time.sleep(0.1)
    frase = "Sockets en Python son geniales"
    total = cliente_contador_letras(frase)
    print(f"  • Frase enviada:    '{frase}'")
    print(f"  ✔ Longitud devuelta: {total} caracteres.")

    # Reto 4: Servidor hora
    print("\n[Reto 4]: Servidor de Hora:")
    threading.Thread(target=servidor_hora, daemon=True).start()
    time.sleep(0.1)
    hora = cliente_hora()
    print(f"  ✔ Hora actual devuelta por el servidor TCP: {hora}")

    # Reto 5: Cliente con timeout de 3s
    print("\n[Reto 5]: Cliente con Timeout hacia puerto cerrado:")
    resultado_timeout = cliente_con_timeout(59990)
    print(f"  ✔ Resultado del cliente: '{resultado_timeout}'")

    # Reto 6: Benchmark de velocidad (100 paquetes)
    print("\n[Reto 6]: Benchmark de velocidad (100 intercambios ida y vuelta):")
    t_tcp, t_udp = medir_velocidad_100_mensajes()
    print(f"  • Tiempo total TCP: {t_tcp:.2f} ms")
    print(f"  • Tiempo total UDP: {t_udp:.2f} ms")
    if t_udp < t_tcp:
        print(f"  ⚡ UDP fue {t_tcp / t_udp:.1f} veces más veloz debido a su menor sobrecarga.")

    print("\n" + "=" * 75)
    print("  ¡Los 6 retos completados con éxito!")
    print("=" * 75)

if __name__ == "__main__":
    main()

