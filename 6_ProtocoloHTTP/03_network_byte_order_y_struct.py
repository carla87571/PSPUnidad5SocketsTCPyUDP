"""
03_network_byte_order_y_struct.py
=================================
Diapositiva de referencia: Diapositiva 4 ("El orden de los bytes: network byte order")

¿QUÉ ES EL 'NETWORK BYTE ORDER'?
--------------------------------
Cuando transmites números enteros por la red (como puertos, contadores o timestamps):
  • Cada arquitectura de CPU puede guardar los bytes en diferente orden:
    - Little-Endian: El byte menos significativo va primero (Intel x86, AMD, ARM).
    - Big-Endian:    El byte más significativo va primero (como leemos de izquierda a derecha).
  • Para que dos computadoras distintas se entiendan sin importar su procesador,
    Internet acordó usar SIEMPRE BIG-ENDIAN, denominado estándar 'Network Byte Order'.

EL MÓDULO 'struct' EN PYTHON:
-----------------------------
Permite empaquetar números en bytes exactos y desempaquetarlos:
  • '!' -> Fuerza el Network Byte Order (Big-Endian).
  • 'I' -> Entero sin signo de 4 bytes (32 bits, rango 0 a 4.294.967.295).
  • 'H' -> Entero sin signo de 2 bytes (16 bits, rango 0 a 65.535, ideal para puertos).

EL CÓDIGO DE LA DIAPOSITIVA 4:
------------------------------
    import struct
    datos = struct.pack("!I", 5000)
    print(datos)                           # b'\\x00\\x00\\x13\\x88'
    puerto = struct.unpack("!I", datos)[0]
    print(puerto)                          # 5000
"""

import struct
import sys

def main():
    print("=" * 70)
    print("  03 - EL ORDEN DE LOS BYTES: NETWORK BYTE ORDER Y struct")
    print("=" * 70)

    # 1. Tu arquitectura local
    print(f"\n[1] TU COMPUTADORA LOCAL:")
    print(f"    • Orden de bytes nativo de tu CPU: {sys.byteorder.upper()}-ENDIAN")

    # 2. El código exacto de la Diapositiva 4
    print("\n[2] EMPAQUETANDO EL NÚMERO 5000:")
    numero = 5000

    # 5000 en hexadecimal es 0x00001388
    # En Big-Endian (!I): \x00 \x00 \x13 \x88
    datos_big_endian = struct.pack("!I", numero)
    print(f"    • Código: struct.pack('!I', {numero})")
    print(f"    • Resultado en bytes binarios: {datos_big_endian}")

    # Desempaquetar
    numero_recuperado = struct.unpack("!I", datos_big_endian)[0]
    print(f"    • Desempaquetado con '!I':    {numero_recuperado}")

    # 3. El peligro de olvidar el prefijo '!'
    print("\n[3] EL PELIGRO: ¿QUÉ PASA SI OLVIDAS EL PREFIJO '!'?")
    datos_little_endian = struct.pack("<I", numero)  # '<' es Little-Endian
    print(f"    • Bytes en Little-Endian (<I): {datos_little_endian} (bytes invertidos)")

    # Si la red lee Little-Endian creyendo que es Big-Endian:
    numero_corrupto = struct.unpack("!I", datos_little_endian)[0]
    print(f"    ❌ Si la red lo lee en Network Byte Order, el 5000 se convierte en:")
    print(f"       👉 {numero_corrupto:,} (¡Un desastre total!)")

    # 4. Tabla de formatos
    print("\n[4] TABLA QUE DEBES RECORDAR (Diapositiva 4):")
    print("    ┌──────────┬─────────────────────────────────────────────────┐")
    print("    │ Código   │ Significado                                     │")
    print("    ├──────────┼─────────────────────────────────────────────────┤")
    print("    │ !        │ Network Byte Order (Big-Endian obligatorio)     │")
    print("    │ I        │ Entero sin signo de 4 bytes (ej. timestamps)   │")
    print("    │ H        │ Entero sin signo de 2 bytes (ej. puertos)      │")
    print("    └──────────┴─────────────────────────────────────────────────┘")
    print("=" * 70)

if __name__ == "__main__":
    main()

