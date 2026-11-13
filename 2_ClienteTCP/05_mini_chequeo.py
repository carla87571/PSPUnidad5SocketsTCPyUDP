"""
05_mini_chequeo.py
==================
Diapositiva de referencia: Diapositiva 6 ("Mini-chequeo: cliente TCP")

AUTOEVALUACIÓN DE CONCEPTOS CLAVE DEL CLIENTE TCP:
--------------------------------------------------
Este script evalúa las 3 preguntas clave del Mini-chequeo de la Diapositiva 6.

MODOS DE USO:
-------------
  • Modo normal (lectura y repaso con pausas didácticas):
      python3 05_mini_chequeo.py

  • Modo interactivo (espera a que presiones Enter en cada pregunta):
      python3 05_mini_chequeo.py --interactivo
"""

import sys
import time

PREGUNTAS = [
    {
        "num": 1,
        "pregunta": "¿Qué método establece la conexión y qué error lanza si no hay nadie escuchando?",
        "respuesta": "• Método: connect((HOST, PORT))\n• Excepción: ConnectionRefusedError (si no hay servidor activo en ese puerto)."
    },
    {
        "num": 2,
        "pregunta": "¿Por qué usar sendall() y no send()?",
        "respuesta": "• sendall() garantiza el envío de TODOS los bytes sin pérdidas.\n• send() puede mandar solo una parte de los datos si los buffers del sistema se saturan."
    },
    {
        "num": 3,
        "pregunta": "¿Qué hace recv(1024) y por qué NO es un límite absoluto?",
        "respuesta": "• Recibe HASTA 1024 bytes por cada llamada (es el tamaño del buffer de lectura).\n• No es un límite del mensaje: si el mensaje es más grande, basta con llamar a recv() varias veces y concatenar los fragmentos."
    }
]

def main():
    print("=" * 70)
    print("  05 - MINI-CHEQUEO: CLIENTE TCP (Responde sin mirar)")
    print("  (Basado en la Diapositiva 6)")
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
    print("  ¡Excelente repaso! Has completado las preguntas clave del Cliente TCP.")
    print("=" * 70)

if __name__ == "__main__":
    main()

