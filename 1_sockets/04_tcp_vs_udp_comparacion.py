"""
04_tcp_vs_udp_comparacion.py
============================
Diapositivas de referencia:
  • Diapositiva 5 ("La analogía del bloque: Carta certificada contra avión de papel")
  • Diapositiva 6 ("TCP vs UDP cara a cara: La tabla que hay que saberse")

LAS DOS GRANDES FILOSOFÍAS DE TRANSPORTE:
-----------------------------------------
1. TCP (La carta certificada):
   - Filosofía: "La fiabilidad ante todo".
   - Hay un costo extra (handshake inicial, confirmaciones ACK, números de secuencia).
   - Si un paquete se pierde en el camino, se retransmite automáticamente.
   - Si llegan desordenados, el receptor los ordena antes de entregarlos al programa.

2. UDP (El avión de papel):
   - Filosofía: "La velocidad y la inmediatez ante todo".
   - No hay conexión previa: simplemente se envía el paquete a la dirección destino.
   - Si se pierde o llega desordenado, a UDP no le importa (no hay confirmación).
   - Paradójicamente, las tres respuestas negativas ("Sin conexión", "Sin garantía", "Sin orden")
     son la razón de que UDP sea tan veloz.
"""

import time

def simular_envio_tcp(mensaje):
    """Simula los pasos pedagógicos que ocurren en una conexión TCP."""
    print("\n--- SIMULACIÓN TCP (Carta Certificada) ---")
    print("1. [Handshake] Cliente y Servidor negocian la conexión (SYN -> SYN-ACK -> ACK)...")
    time.sleep(0.3)
    print("   ¡Conexión establecida con éxito!")
    
    print(f"2. [Envío] Enviando paquete con datos: '{mensaje}'")
    time.sleep(0.3)
    
    print("3. [Confirmación] El receptor responde con ACK (Acuse de recibo):")
    print("   ✓ 'Paquete recibido correctamente y en orden.'")
    print("4. [Cierre] Desconexión ordenada (FIN -> ACK).")

def simular_envio_udp(mensaje):
    """Simula el comportamiento de envío en UDP."""
    print("\n--- SIMULACIÓN UDP (Avión de Papel) ---")
    print("1. [Sin conexión previa] No hay handshake ni espera.")
    print(f"2. [Disparo] Se lanza el datagrama al destino: '{mensaje}'")
    time.sleep(0.2)
    print("3. [Olvidar] El emisor no espera acuse de recibo (ACK).")
    print("   ¿Llegó? ¿Se perdió en la red? ¿Llegó desordenado? Al emisor no le consta.")
    print("   ¡Pero se lanzó a máxima velocidad y con mínimo retardo!")

def main():
    print("=" * 70)
    print("  04 - TCP VS UDP CARA A CARA: FIABILIDAD VS VELOCIDAD")
    print("=" * 70)

    # 1. Tabla comparativa (Diapositiva 6)
    print("\n[1] LA TABLA QUE HAY QUE SABERSE:")
    print("┌─────────────────────┬──────────────────────────┬──────────────────────────┐")
    print("│ Característica      │ TCP                      │ UDP                      │")
    print("├─────────────────────┼──────────────────────────┼──────────────────────────┤")
    print("│ Conexión            │ Sí (handshake 3 vías)    │ No (sin estado previo)   │")
    print("│ Entrega garantizada │ Sí (retransmisiones)     │ No (best-effort)         │")
    print("│ Orden garantizado   │ Sí (números de secuencia)│ No                       │")
    print("│ Velocidad           │ Más lento (más control)  │ Más rápido (ligero)      │")
    print("│ Uso típico          │ Web (HTTP), Email, FTP   │ Streaming, Juegos, DNS   │")
    print("└─────────────────────┴──────────────────────────┴──────────────────────────┘")

    # 2. Las analogías de la diapositiva 5
    print("\n[2] LAS ANALOGÍAS:")
    print("    • TCP = CARTA CERTIFICADA:")
    print("      Pagas más, el cartero confirma la entrega y, si se pierde, se reenvía.")
    print("      Sabes que llegó... y en el orden correcto.")
    print("\n    • UDP = AVIÓN DE PAPEL:")
    print("      Lo lanzas desde el balcón y lo olvidas. Si aterriza, bien; si el viento")
    print("      se lo lleva, también. Pero lanzas CIEN en lo que tardas una carta.")

    # 3. Simulaciones paso a paso
    simular_envio_tcp("Transferencia de $500 dólares")
    simular_envio_udp("Coordenadas de posición en un videojuego multijugador")

    # 4. Conclusión pedagógica
    print("\n" + "=" * 70)
    print("[3] ¿CUÁL ELEGIR?")
    print("    • ¿Importa que falte un solo byte? (ej. archivo .zip, texto, banco) -> Usa TCP.")
    print("    • ¿Importa más la inmediatez que un paquete perdido? (ej. voz, video) -> Usa UDP.")
    print("=" * 70)

if __name__ == "__main__":
    main()

