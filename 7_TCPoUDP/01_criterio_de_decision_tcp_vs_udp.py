"""
01_criterio_de_decision_tcp_vs_udp.py
=====================================
Diapositivas de referencia:
  • Diapositiva 1 ("¿TCP o UDP? La pregunta correcta")
  • Diapositiva 2 ("Casos reales: La tabla que se repite en las entrevistas")
  • Diapositiva 3 ("Mini-chequeo: criterio de decisión")

LA PREGUNTA CORRECTA (Diapositiva 1):
-------------------------------------
Cuando diseñas una aplicación conectada a la red, no te preguntes cuál es "mejor".
Pregúntate:
  • ¿El dato DEBE llegar intacto, completo y en orden? -> Usa TCP (Carta certificada).
  • ¿El dato DEBE llegar con la mínima latencia posible, tolerando pérdidas? -> Usa UDP (Avión de papel).

LA TABLA DE CASOS REALES QUE SE REPITE EN ENTREVISTAS (Diapositiva 2):
----------------------------------------------------------------------
  ┌───────────────────────────────┬───────────┬──────────────────────────────────────────────┐
  │ Aplicación                    │ Protocolo │ ¿Por qué?                                    │
  ├───────────────────────────────┼───────────┼──────────────────────────────────────────────┤
  │ Web (HTTP/1.1 y HTTP/2)       │ TCP       │ La página debe llegar completa y en orden    │
  │ Correo (SMTP, IMAP, POP3)     │ TCP       │ Un correo a medias o con bytes corruptos no sirve │
  │ Transferencia archivos (FTP)  │ TCP       │ Un solo byte perdido corrompe un ejecutable/zip │
  │ Pagos y compras online        │ TCP       │ El cobro y autorización deben ser exactos    │
  │ DNS (Resolución de nombres)   │ UDP       │ La consulta es diminuta; si se pierde, se repite │
  │ VoIP / Videollamadas          │ UDP       │ Debe ser fluida; un frame de audio perdido se tolera │
  │ Juegos online multijugador    │ UDP       │ Cientos de paquetes/seg; la latencia manda   │
  │ NTP (Sincronización horaria)  │ UDP       │ Manda muchas consultas ligeras y promedia    │
  └───────────────────────────────┴───────────┴──────────────────────────────────────────────┘

EL CASO ESPECIAL DEL STREAMING MODERNO (YouTube, Twitch, Netflix):
-----------------------------------------------------------------
Aunque el video parece tolerar pérdidas, las plataformas modernas usan HTTP sobre TCP
(mediante HLS y DASH). ¿Por qué?
Porque TCP atraviesa sin problemas firewalls, proxies y aprovecha toda la red de servidores
caché (CDN) de la web mundial, usando un buffer previo de 3-5 segundos.

¿Y SI QUIERES LO MEJOR DE AMBOS MUNDOS? (QUIC / HTTP/3):
--------------------------------------------------------
El nuevo protocolo QUIC (la base de HTTP/3 desarrollada por Google) corre ENCIMA de UDP
para eliminar el retardo del handshake TCP, pero implementa su propio control de congestión,
cifrado TLS 1.3 y retransmisión inteligente en espacio de usuario.
"""

CASOS_DE_USO = [
    {
        "app": "Descarga de una actualización de software (.zip)",
        "protocolo": "TCP",
        "motivo": "Si falta un solo byte, el archivo zip queda corrupto y no se puede instalar."
    },
    {
        "app": "Chat de voz en Discord durante una partida",
        "protocolo": "UDP",
        "motivo": "La voz debe oírse en tiempo real. Si se pierde una sílaba de hace 50ms, no sirve retransmitirla."
    },
    {
        "app": "Consulta de saldo bancario / Transacción financiera",
        "protocolo": "TCP",
        "motivo": "Garantía de entrega obligatoria y confirmación punto a punto."
    },
    {
        "app": "Telemetría de sensores de un dron (giroscopio a 100 Hz)",
        "protocolo": "UDP",
        "motivo": "Interesa únicamente la inclinación actual, no la de hace un segundo."
    },
    {
        "app": "Consulta DNS (¿Qué IP tiene 'google.com'?)",
        "protocolo": "UDP",
        "motivo": "Petición diminuta. Si no hay respuesta en 1s, el cliente simplemente vuelve a preguntar."
    }
]

def evaluar_decision(es_critico_cada_byte, tolera_perdidas_por_fluidez):
    """Aplica la regla de decisión de la Diapositiva 3."""
    if es_critico_cada_byte:
        return "TCP", "Prioridad: Fiabilidad absoluta y entrega en orden (Carta certificada)."
    elif tolera_perdidas_por_fluidez:
        return "UDP", "Prioridad: Mínima latencia y velocidad inmediata (Avión de papel)."
    else:
        return "QUIC (UDP con fiabilidad)", "Caso híbrido moderno (HTTP/3)."

def main():
    print("=" * 75)
    print("  01 - CRITERIO DE DECISIÓN ARQUITECTÓNICA: ¿TCP O UDP?")
    print("=" * 75)

    print("\n[1] REGLA FUNDAMENTAL DE DECISIÓN (Diapositiva 3):")
    print("    • ¿Puedes permitirte perder datos? -> Si NO: USA TCP.")
    print("    • ¿Prefieres fluidez y velocidad tolerando pérdidas? -> USA UDP.")

    print("\n[2] CASOS REALES ANALIZADOS:")
    for i, item in enumerate(CASOS_DE_USO, 1):
        print(f"\n  Caso {i}: {item['app']}")
        print(f"    👉 Protocolo recomendado: {item['protocolo']}")
        print(f"    💡 Justificación:          {item['motivo']}")

    print("\n[3] EL FUTURO: QUIC / HTTP/3:")
    print("    • Construye fiabilidad tipo TCP directamente encima de UDP.")
    print("    • Logra: Cero retardos de handshake, cifrado nativo y sin 'head-of-line blocking'.")

    print("\n" + "=" * 75)
    print("  LECCIÓN: No hay protocolo superior; hay requisitos de aplicación bien elegidos.")
    print("=" * 75)

if __name__ == "__main__":
    main()

