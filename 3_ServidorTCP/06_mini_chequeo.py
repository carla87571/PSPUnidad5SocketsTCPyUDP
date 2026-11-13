"""
06_mini_chequeo.py
==================
Diapositiva de referencia: Diapositiva 7 ("Mini-chequeo: servidor TCP")

AUTOEVALUACIÓN DE CONCEPTOS CLAVE DEL SERVIDOR TCP:
---------------------------------------------------
Este script evalúa las 3 preguntas clave de la Diapositiva 7.

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
        "pregunta": "¿Qué tres métodos preparan el servidor antes de atender a nadie?",
        "respuesta": "1. socket()               -> Crea el socket.\n2. bind((HOST, PORT))    -> Asigna la IP y el puerto.\n3. listen()              -> Habilita la cola de llamadas entrantes."
    },
    {
        "num": 2,
        "pregunta": "¿Qué devuelve accept() y por qué es bloqueante?",
        "respuesta": "• Devuelve: La tupla (conexion, direccion):\n   - 'conexion' es el socket privado para hablar con ese cliente.\n   - 'direccion' es la tupla (IP, puerto_remoto) del cliente.\n• Es bloqueante porque detiene el programa hasta que un cliente llame."
    },
    {
        "num": 3,
        "pregunta": "Tras accept(), ¿con qué objeto se recibe y envía: 'servidor' o 'conexion'?",
        "respuesta": "• Se usa CONEXION.\n• 'servidor' solo escucha en la puerta principal.\n• 'conexion' es el canal exclusivo de esa llamada concreta."
    }
]

def main():
    print("=" * 70)
    print("  06 - MINI-CHEQUEO: SERVIDOR TCP (Responde en 30 segundos)")
    print("  (Basado en la Diapositiva 7)")
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
    print("  ¡Enhorabuena! Has dominado los fundamentos del Servidor TCP.")
    print("=" * 70)

if __name__ == "__main__":
    main()

