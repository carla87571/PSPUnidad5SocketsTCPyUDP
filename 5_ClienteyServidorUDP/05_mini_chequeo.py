"""
05_mini_chequeo.py
==================
Diapositiva de referencia: Diapositiva 8 ("Mini-chequeo: UDP")

AUTOEVALUACIÓN DE CONCEPTOS CLAVE DE UDP:
-----------------------------------------
Este script evalúa las 4 preguntas de la Diapositiva 8.

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
        "pregunta": "¿Qué dos métodos usa el cliente UDP y qué devuelve cada uno?",
        "respuesta": "• sendto(datos, dirección): Envía el datagrama (devuelve el número de bytes enviados).\n• recvfrom(1024): Espera un datagrama y devuelve la tupla (datos, dirección_del_emisor)."
    },
    {
        "num": 2,
        "pregunta": "¿Por qué el servidor UDP NO necesita accept()?",
        "respuesta": "• Porque UDP NO TIENE CONEXIONES ni estado previo.\n• Cada datagrama llega de forma independiente y recvfrom() ya te indica directamente la dirección de quién lo envió."
    },
    {
        "num": 3,
        "pregunta": "¿Qué tres cosas pueden pasarle a un datagrama en la red y qué pasa si se pierde?",
        "respuesta": "• Puede:\n   1. Perderse\n   2. Llegar desordenado\n   3. Duplicarse\n• Si se pierde: Se pierde para siempre (UDP no confirma ni reenvía)."
    },
    {
        "num": 4,
        "pregunta": "¿Cuál es el tamaño máximo de carga útil de un datagrama UDP?",
        "respuesta": "• Unos 65.507 bytes útiles.\n• Cálculo: 65.535 (límite IP de 16 bits) - 20 (cabecera IPv4) - 8 (cabecera UDP) = 65.507 bytes."
    }
]

def main():
    print("=" * 70)
    print("  05 - MINI-CHEQUEO: PROTOCOLO UDP (Responde en 30 segundos)")
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
    print("  ¡Excelente! Has asimilado los principios esenciales del protocolo UDP.")
    print("=" * 70)

if __name__ == "__main__":
    main()

