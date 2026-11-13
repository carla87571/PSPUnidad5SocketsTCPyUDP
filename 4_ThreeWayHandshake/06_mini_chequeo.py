"""
06_mini_chequeo.py
==================
Diapositiva de referencia: Diapositiva 8 ("Mini-chequeo: ciclo de vida y errores - Las cuatro de la entrevista")

LAS 4 PREGUNTAS TÍPICAS DE ENTREVISTA TÉCNICA:
----------------------------------------------
Este script evalúa los 4 conceptos clave del ciclo de vida TCP y control de excepciones.

MODOS DE USO:
-------------
  • Modo normal (lectura y repaso con pausas didácticas):
      python3 06_mini_chequeo.py

  • Modo interactivo (espera a que presiones Enter en cada pregunta):
      python3 06_mini_chequeo.py --interactivo
"""

import sys
import time

PREGUNTAS = [
    {
        "num": 1,
        "pregunta": "¿Cuáles son los tres mensajes del handshake TCP y en qué orden?",
        "respuesta": "1. SYN     (Cliente ➔ Servidor)\n2. SYN+ACK (Servidor ➔ Cliente)\n3. ACK     (Cliente ➔ Servidor)\n(Tras este saludo de 3 vías, los datos ya pueden fluir en ambas direcciones)."
    },
    {
        "num": 2,
        "pregunta": "¿Qué error lanza el SO al relanzar un servidor sin SO_REUSEADDR y qué estado lo causa?",
        "respuesta": "• Error: OSError: [Errno 98] Address already in use\n• Causa: El estado TIME_WAIT del sistema operativo, que retiene el puerto durante 1-2 minutos."
    },
    {
        "num": 3,
        "pregunta": "¿Qué excepción lanza recv() si se pasa el timeout y cuál si escribes en un socket ya cerrado?",
        "respuesta": "• Al superar el tiempo límite de lectura: socket.timeout (o TimeoutError).\n• Al intentar escribir con sendall() en un socket cerrado por el otro lado: BrokenPipeError."
    },
    {
        "num": 4,
        "pregunta": "¿Cuál es la diferencia entre ConnectionRefusedError y ConnectionResetError?",
        "respuesta": "• ConnectionRefusedError: Ocurre AL CONECTAR (connect). Nadie está escuchando en ese puerto.\n• ConnectionResetError:   Ocurre AL HABLAR (recv/send). La conexión ya existía, pero el otro lado la cerró abruptamente de golpe."
    }
]

def main():
    print("=" * 70)
    print("  06 - MINI-CHEQUEO: CICLO DE VIDA Y ERRORES ('Las cuatro de la entrevista')")
    print("  (Basado en la Diapositiva 8)")
    print("=" * 70)

    modo_interactivo = "--interactivo" in sys.argv

    for item in PREGUNTAS:
        print(f"\n[Pregunta {item['num']}]")
        print(f"  {item['pregunta']}")

        if modo_interactivo:
            input("\n  👉 Presiona [ENTER] para revelar la respuesta...")
        else:
            time.sleep(0.4)
            print("\n  💡 Respuesta:")

        for linea in item['respuesta'].split("\n"):
            print(f"     {linea}")
        print("-" * 50)

    print("\n" + "=" * 70)
    print("  ¡Excelente! Estas 4 preguntas son fundamentales en redes y entrevistas de backend.")
    print("=" * 70)

if __name__ == "__main__":
    main()

