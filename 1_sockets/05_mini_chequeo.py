"""
05_mini_chequeo.py
==================
Diapositiva de referencia: Diapositiva 7 ("Mini-chequeo: el socket")

AUTOEVALUACIÓN DE CONCEPTOS CLAVE:
----------------------------------
Este script te permite poner a prueba lo aprendido en las diapositivas
mediante las 4 preguntas del Mini-chequeo.

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
        "pregunta": "¿Qué identifica la IP y qué identifica el puerto?",
        "respuesta": "• La IP identifica la MÁQUINA en la red.\n• El PUERTO identifica el PROGRAMA dentro de ella."
    },
    {
        "num": 2,
        "pregunta": "¿Qué representa 127.0.0.1 y para qué sirve?",
        "respuesta": "• Es 'localhost' (tu propia máquina).\n• Sirve para pruebas de desarrollo seguras sin requerir red real ni internet."
    },
    {
        "num": 3,
        "pregunta": "¿Qué constante de Python crea un socket TCP y cuál uno UDP?",
        "respuesta": "• TCP: socket.SOCK_STREAM\n• UDP: socket.SOCK_DGRAM\n• (Ambos usando socket.AF_INET para IPv4)"
    },
    {
        "num": 4,
        "pregunta": "¿Qué garantiza TCP que UDP NO garantiza? (Menciona tres cosas)",
        "respuesta": "1. Conexión previa (handshake)\n2. Entrega garantizada (retransmisión si se pierde)\n3. Orden de los paquetes"
    }
]

def main():
    print("=" * 70)
    print("  05 - MINI-CHEQUEO: PON A PRUEBA TUS CONOCIMIENTOS")
    print("  (Basado en la Diapositiva 7: Responde en 30 segundos)")
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
    print("  ¡Excelente! Si respondiste las 4 correctamente, dominas la base de sockets.")
    print("=" * 70)

if __name__ == "__main__":
    main()
