"""
03_solucion_so_reuseaddr.py
===========================
Diapositiva de referencia: Diapositiva 4 ("SO_REUSEADDR: Reinicia tu servidor sin esperar")

LA SOLUCIÓN A TIME_WAIT: SO_REUSEADDR
-------------------------------------
Para no tener que esperar 1-2 minutos cada vez que reinicias tu servidor en desarrollo,
Python permite configurar la opción de socket SO_REUSEADDR antes de llamar a bind():

    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

DESGLOSE DE PARÁMETROS (Diapositiva 4):
---------------------------------------
  • SOL_SOCKET:   Indica el nivel de protocolo (opciones a nivel del socket genérico).
  • SO_REUSEADDR: Nombre de la opción ("Socket Reuse Address").
  • 1:            Valor booleano: 1 para activar la opción (0 para desactivarla).

¿QUÉ LE DICE AL SISTEMA OPERATIVO?
----------------------------------
"Permite a este proceso asociarse a este puerto aunque todavía existan conexiones
anteriores en estado TIME_WAIT asociadas a él".
"""

import socket

HOST, PUERTO = "127.0.0.1", 5008

def main():
    print("=" * 70)
    print("  03 - SO_REUSEADDR: REINICIA TU SERVIDOR SIN ESPERAR")
    print("=" * 70)

    # 1. Tabla de la Diapositiva 4
    print("\n[1] ANATOMÍA DE setsockopt():")
    print("    ┌──────────────┬─────────────────────────────────────────────────┐")
    print("    │ Parámetro    │ Significado                                     │")
    print("    ├──────────────┼─────────────────────────────────────────────────┤")
    print("    │ SOL_SOCKET   │ Nivel de opciones del propio socket base        │")
    print("    │ SO_REUSEADDR │ Opción para reutilizar dirección en TIME_WAIT   │")
    print("    │ 1            │ Activa la opción (1 = True, 0 = False)          │")
    print("    └──────────────┴─────────────────────────────────────────────────┘")

    # 2. Demostración práctica
    print(f"\n[2] DEMOSTRACIÓN PRÁCTICA:")
    print("    1. Creando servidor con SO_REUSEADDR...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv1:
        # Activar la opción antes de bind()
        srv1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv1.bind((HOST, PUERTO))
        srv1.listen(1)
        print(f"       ✔ Servidor #1 enlazado a ({HOST}, {PUERTO}).")
    
    print("    2. Servidor #1 cerrado. El puerto entra en ciclo de cierre.")
    
    # Inmediatamente intentamos abrir un Servidor #2 en el mismo puerto
    print("    3. Abriendo inmediatamente Servidor #2 en el mismo puerto...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv2:
        srv2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv2.bind((HOST, PUERTO))
        srv2.listen(1)
        print(f"       ✔ Servidor #2 enlazado con éxito a ({HOST}, {PUERTO}) sin esperar.")

    print("\n" + "=" * 70)
    print("  CONSEJO DE ORO:")
    print("  Pon 'servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)'")
    print("  SIEMPRE en todos tus servidores antes de bind(). Te ahorrará muchos dolores de cabeza.")
    print("=" * 70)

if __name__ == "__main__":
    main()

