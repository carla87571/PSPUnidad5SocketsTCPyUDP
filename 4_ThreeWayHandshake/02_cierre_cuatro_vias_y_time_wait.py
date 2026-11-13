"""
02_cierre_cuatro_vias_y_time_wait.py
====================================
Diapositivas de referencia:
  • Diapositiva 2 ("El cierre de la conexión: La despedida: FIN y ACK")
  • Diapositiva 3 ("TIME_WAIT y «Address already in use»: El puerto que queda retenido")

LA DESPEDIDA DE TCP (Four-Way Teardown):
----------------------------------------
Así como TCP requiere 3 pasos para abrirse, requiere 4 pasos para despedirse
porque es una conexión full-duplex (ambos lados pueden hablar independientemente):

  1. Lado A envía FIN:  "Ya no tengo más datos que enviar".
  2. Lado B responde ACK: "Entendido que terminaste".
  3. Lado B envía su FIN: "Yo tampoco tengo más datos".
  4. Lado A responde ACK: "Recibido. Fin total".

EL MISTERIOSO ESTADO 'TIME_WAIT':
---------------------------------
Tras enviar el último ACK, el lado que inició el cierre NO libera el puerto inmediatamente.
Entra en un estado llamado TIME_WAIT (que suele durar entre 30 segundos y 2 minutos).

¿POR QUÉ EXISTE TIME_WAIT?
--------------------------
Es protección del protocolo TCP:
  1. Si el último ACK se pierde por la red, el otro lado reenviará su FIN. El puerto debe
     estar ahí para reenviar el ACK.
  2. Garantiza que ningún paquete "rezagado" de la conexión vieja se mezcle con una
     conexión nueva que abra en el mismo puerto.

EL PROBLEMA EN EL DESARROLLO («Address already in use»):
--------------------------------------------------------
Si cierras tu servidor y lo vuelves a ejecutar de inmediato, el sistema operativo
rechazará el bind con:
    OSError: [Errno 98] Address already in use
"""

import socket

def main():
    print("=" * 70)
    print("  02 - CIERRE DE CONEXIÓN, TIME_WAIT Y 'Address already in use'")
    print("=" * 70)

    # 1. Esquema del Four-Way Teardown (Diapositiva 2)
    print("\n[1] LOS 4 PASOS DEL CIERRE (FIN / ACK):")
    print("    1. Lado A -> FIN  : «No tengo más que enviar»")
    print("    2. Lado B -> ACK  : «Recibido que no enviarás más»")
    print("    3. Lado B -> FIN  : «Yo tampoco tengo nada más»")
    print("    4. Lado A -> ACK  : «Confirmado. Conexión liberada»")

    # 2. Explicación de TIME_WAIT (Diapositiva 3)
    print("\n[2] ¿QUÉ ES TIME_WAIT?")
    print("    • Es un estado donde el kernel retiene la tupla (IP, puerto)")
    print("      durante 60-120 segundos tras el cierre.")
    print("    • Motivo: Evitar que paquetes huérfanos se confundan con una nueva conexión.")

    # 3. Demostración práctica de Address already in use
    HOST, PUERTO = "127.0.0.1", 5007
    print(f"\n[3] DEMOSTRACIÓN DE 'Address already in use':")

    # Creamos un socket que ocupa el puerto
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((HOST, PUERTO))
    s1.listen(1)
    print(f"    • Socket #1 activo escuchando en ({HOST}, {PUERTO}).")

    # Intentamos crear otro socket en el MISMO puerto sin cerrar el primero
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"    • Intentando enlazar Socket #2 al mismo puerto {PUERTO}...")
        s2.bind((HOST, PUERTO))
    except OSError as e:
        print(f"\n    ❌ ¡ERROR CAPTURADO!")
        print(f"    Tipo:   {type(e).__name__}")
        print(f"    Detalle: {e}")
        print("    💡 Como el puerto está ocupado (o en TIME_WAIT), el SO rechaza el bind.")

    s1.close()
    s2.close()

    print("\n" + "=" * 70)
    print("  ¿Cómo evitamos esperar 2 minutos cada vez que reiniciamos el servidor?")
    print("  -> ¡Con la opción SO_REUSEADDR! (Ver archivo 03).")
    print("=" * 70)

if __name__ == "__main__":
    main()

