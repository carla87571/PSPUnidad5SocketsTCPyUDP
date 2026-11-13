"""
05_mini_chequeo.py
==================
Diapositiva de referencia: Diapositiva 7 ("Mini-chequeo: HTTP, bytes y NTP")

AUTOEVALUACIÓN DE CONCEPTOS:
----------------------------
Este script evalúa los 3 conceptos clave de la Diapositiva 7:
  1. La línea en blanco de HTTP y códigos de estado.
  2. Network byte order en struct.
  3. Por qué NTP utiliza UDP.

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
        "pregunta": "¿Qué significa la línea en blanco '\\r\\n\\r\\n' en una petición HTTP y qué indica el código 200?",
        "respuesta": "• '\\r\\n\\r\\n': Señala el final de las cabeceras HTTP ('ya estaba todo').\n• Código 200: Indica 'OK' (la petición fue recibida y procesada correctamente por el servidor)."
    },
    {
        "num": 2,
        "pregunta": "¿Qué código de 'struct' usa big-endian y por qué lo necesita el cliente NTP?",
        "respuesta": "• Se usa el prefijo '!' (ej: '!I' para entero sin signo de 4 bytes).\n• Lo necesita porque los servidores NTP escriben sus timestamps en Network Byte Order (Big-Endian),\ny para leer el número correcto debemos interpretarlo en el mismo orden."
    },
    {
        "num": 3,
        "pregunta": "¿Por qué NTP usa UDP si la hora debe ser exacta?",
        "respuesta": "• Porque NTP envía múltiples peticiones ligeras y calcula la hora estadísticamente promediando retardos.\n• Un datagrama perdido es irrelevante y no afecta al cálculo.\n• TCP añadiría latencia variable innecesaria debido al handshake y retransmisiones."
    }
]

def main():
    print("=" * 70)
    print("  05 - MINI-CHEQUEO: HTTP, BYTES Y NTP (Responde sin mirar)")
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
    print("  ¡Excelente trabajo! Has consolidado la unión entre sockets, HTTP y datos binarios.")
    print("=" * 70)

if __name__ == "__main__":
    main()

