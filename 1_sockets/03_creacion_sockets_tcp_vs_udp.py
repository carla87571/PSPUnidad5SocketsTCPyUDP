"""
03_creacion_sockets_tcp_vs_udp.py
=================================
Diapositiva de referencia: Diapositiva 4 ("Crear un socket en Python: Una línea que decide el protocolo")

UNA SOLA LÍNEA QUE DECIDE TODO:
-------------------------------
Para crear un socket en Python usamos:
    s = socket.socket(familia, tipo)

PARÁMETROS EXPLICADOS:
----------------------
1. Familia de direcciones (¿Qué tipo de IP usaremos?):
   - socket.AF_INET  -> IPv4 (ej: "192.168.1.1", formato más común).
   - socket.AF_INET6 -> IPv6 (ej: "2001:0db8:...", formato de 128 bits).

2. Tipo de socket (¿Qué protocolo de transporte usaremos?):
   - socket.SOCK_STREAM -> TCP: Orientado a conexión, fiable, entrega garantizada.
   - socket.SOCK_DGRAM  -> UDP: Sin conexión, rápido, datagramas sueltos.

TRUCO MNEMOTÉCNICO PARA NO LIARTE:
----------------------------------
   • DGRAM  = Datagramas sueltos  --> UDP (avión de papel)
   • STREAM = Flujo/Chorro continuo --> TCP (carta certificada)
"""

import socket

def main():
    print("=" * 65)
    print("  03 - CREACIÓN DE SOCKETS EN PYTHON: TCP VS UDP")
    print("=" * 65)

    # 1. Creación de un socket TCP
    print("\n[1] CREANDO UN SOCKET TCP (Orientado a conexión):")
    print("    Código: s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)")
    
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"    • Familia: {s_tcp.family.name} ({s_tcp.family}) -> IPv4")
    print(f"    • Tipo:    {s_tcp.type.name} ({s_tcp.type}) -> TCP (Flujo continuo)")
    s_tcp.close()
    print("    • Socket TCP cerrado.")

    # 2. Creación de un socket UDP
    print("\n[2] CREANDO UN SOCKET UDP (Sin conexión, datagramas):")
    print("    Código: s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)")
    
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"    • Familia: {s_udp.family.name} ({s_udp.family}) -> IPv4")
    print(f"    • Tipo:    {s_udp.type.name} ({s_udp.type}) -> UDP (Datagramas)")
    s_udp.close()
    print("    • Socket UDP cerrado.")

    # 3. Uso elegante con 'with' (Context Manager en Python)
    print("\n[3] BUENA PRÁCTICA EN PYTHON: Sentencia 'with'")
    print("    Al usar 'with', el socket se cierra automáticamente al terminar:")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_auto:
        print(f"    • Socket dentro del bloque 'with': fileno={s_auto.fileno()} (Activo)")
    
    print("    • Fuera del bloque 'with': Socket cerrado automáticamente.")

    # 4. Tabla resumen mnemotécnica
    print("\n[4] REGLA MNEMOTÉCNICA:")
    print("    ┌─────────────┬─────────────────────┬──────────────────────────┐")
    print("    │ Constante   │ Significado         │ Analogía                 │")
    print("    ├─────────────┼─────────────────────┼──────────────────────────┤")
    print("    │ SOCK_STREAM │ TCP (Flujo de datos)│ Carta certificada        │")
    print("    │ SOCK_DGRAM  │ UDP (Datagramas)    │ Avión de papel           │")
    print("    └─────────────┴─────────────────────┴──────────────────────────┘")
    print("=" * 65)

if __name__ == "__main__":
    main()

