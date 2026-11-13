"""
=============================================================================
EJERCICIO 7: TCP VS UDP - CLASIFICACIÓN DE APLICACIONES Y TABLA COMPARATIVA
Unidad 05 - Sockets TCP y UDP - Actividades no evaluables 01 (CEEDCV / DAM)
=============================================================================

ENUNCIADO:
"1. Clasifica cada aplicación como TCP o UDP y justifica brevemente:
    ● Web (HTTP)
    ● Videollamada (Zoom)
    ● Correo (SMTP)
    ● Juego online (Fortnite)
    ● Transferencia de archivos (FTP)
    ● DNS
 2. Completa la tabla:
    Característica       | TCP | UDP
    Conexión             | ... | ...
    Entrega garantizada  | ... | ...
    Orden                | ... | ...
    Velocidad            | ... | ..."
=============================================================================
"""

import sys

# Parte 1: Clasificación y justificación técnica
CLASIFICACION_APLICACIONES = [
    {
        "app": "Web (HTTP / HTTPS)",
        "protocolo": "TCP",
        "puerto": "80 (HTTP) / 443 (HTTPS)",
        "justificacion": (
            "Requiere que las páginas web, scripts JavaScript, estilos CSS y datos JSON\n"
            "lleguen íntegros y sin un solo byte corrupto. Si se perdiera código o texto,\n"
            "la página fallaría o se vería rota. TCP garantiza entrega y orden exactos."
        )
    },
    {
        "app": "Videollamada (Zoom / Teams / Meet)",
        "protocolo": "UDP",
        "puerto": "3478-3481 / Puertos dinámicos RTP",
        "justificacion": (
            "Prima el tiempo real y la baja latencia (interactividad). Si un fotograma de vídeo\n"
            "o paquete de audio se pierde, no sirve de nada retransmitirlo 300 ms después\n"
            "porque provocaría desfase o congelación. Es mejor descartar la pérdida y continuar."
        )
    },
    {
        "app": "Correo electrónico (SMTP / IMAP / POP3)",
        "protocolo": "TCP",
        "puerto": "25, 465, 587 (SMTP) / 993 (IMAP)",
        "justificacion": (
            "Un correo electrónico (texto o archivos adjuntos como PDF) debe llegar 100% completo.\n"
            "La pérdida de paquetes provocaría mensajes ilegibles o adjuntos dañados.\n"
            "TCP garantiza que no haya pérdida gracias a sus acuses de recibo (ACK)."
        )
    },
    {
        "app": "Juego online en tiempo real (Fortnite / CS:GO / Valorant)",
        "protocolo": "UDP",
        "puerto": "Puertos UDP variables del motor del juego",
        "justificacion": (
            "La posición de los jugadores y las acciones cambian decenas de veces por segundo.\n"
            "Retransmitir la posición de un jugador de hace 250 ms causaría 'rubberbanding' (tirones).\n"
            "UDP envía las coordenadas actuales sin demoras de retransmisión."
        )
    },
    {
        "app": "Transferencia de archivos (FTP / SFTP)",
        "protocolo": "TCP",
        "puerto": "20, 21 (FTP) / 22 (SFTP)",
        "justificacion": (
            "Los archivos binarios (ejecutables .exe, imágenes ISO, comprimidos .zip)\n"
            "se vuelven completamente inservibles con un solo bit corrupto o perdido.\n"
            "TCP ofrece control de flujo, orden y suma de comprobación estricta."
        )
    },
    {
        "app": "Resolución de nombres DNS",
        "protocolo": "UDP (por defecto) / TCP (casos especiales)",
        "puerto": "53",
        "justificacion": (
            "Normalmente una consulta DNS cabe en un único paquete de pregunta y respuesta.\n"
            "Usar UDP ahorra los 3 paquetes del handshake TCP, haciendo la resolución casi instantánea.\n"
            "*(Usa TCP como respaldo si la respuesta supera 512 bytes o para transferencias de zona AXFR)*."
        )
    }
]

# Parte 2: Tabla comparativa de características
TABLA_COMPARATIVA = [
    ("Conexión", "Orientado a conexión (Three-Way Handshake SYN, SYN-ACK, ACK)", "Sin conexión (No hay negociación previa)"),
    ("Entrega garantizada", "SÍ (Usa ACKs, temporizadores y retransmisión automática)", "NO (Best-effort: los paquetes pueden perderse sin aviso)"),
    ("Orden de entrega", "SÍ (Usa números de secuencia y reensamblado en orden)", "NO (Cada datagrama viaja independiente y puede desordenarse)"),
    ("Velocidad", "Más lento / Mayor latencia (Cabecera 20-60B, control de congestión)", "Muy rápido / Mínima latencia (Cabecera fija de 8B, sin esperas)")
]


def mostrar_clasificacion():
    """Muestra la clasificación detallada de cada una de las 6 aplicaciones."""
    print("=" * 75)
    print("  📋 PARTE 1: CLASIFICACIÓN DE APLICACIONES (TCP vs UDP)")
    print("=" * 75)
    for i, item in enumerate(CLASIFICACION_APLICACIONES, 1):
        icono = "🔒 [TCP]" if item["protocolo"] == "TCP" else "⚡ [UDP]"
        if "DNS" in item["app"]:
            icono = "⚡ [UDP / TCP]"
        print(f"\n{i}. Aplicación: {item['app']}")
        print(f"   Protocolo de Transporte: {icono} {item['protocolo']}")
        print(f"   Puerto estándar:         {item['puerto']}")
        print(f"   Justificación:")
        for linea in item["justificacion"].split("\n"):
            print(f"     {linea}")
    print("\n" + "=" * 75)


def mostrar_tabla_comparativa():
    """Muestra la tabla comparativa con formato ASCII estructurado."""
    print("\n" + "=" * 75)
    print("  📊 PARTE 2: TABLA COMPARATIVA DE CARACTERÍSTICAS (TCP vs UDP)")
    print("=" * 75)
    
    col_caract = 22
    col_tcp = 35
    col_udp = 35

    encabezado = f"| {'Característica'.ljust(col_caract)} | {'TCP'.ljust(col_tcp)} | {'UDP'.ljust(col_udp)} |"
    separador = f"+{'-' * (col_caract + 2)}+{'-' * (col_tcp + 2)}+{'-' * (col_udp + 2)}+"

    print(separador)
    print(encabezado)
    print(separador)

    for caract, tcp_val, udp_val in TABLA_COMPARATIVA:
        # Ajuste de texto para columnas
        print(f"| {caract.ljust(col_caract)} | {tcp_val[:col_tcp].ljust(col_tcp)} | {udp_val[:col_udp].ljust(col_udp)} |")
        # Si el texto es largo, mostramos la continuación
        if len(tcp_val) > col_tcp or len(udp_val) > col_udp:
            resto_tcp = tcp_val[col_tcp:].strip()
            resto_udp = udp_val[col_udp:].strip()
            print(f"| {''.ljust(col_caract)} | {resto_tcp[:col_tcp].ljust(col_tcp)} | {resto_udp[:col_udp].ljust(col_udp)} |")
        print(separador)


def resumen_regla_de_oro():
    """Regla mnemotécnica para recordar cuándo usar TCP o UDP."""
    print("\n💡 REGLA DE ORO DE DECISIÓN:")
    print("   • ¿Prefieres que los datos lleguen COMPLETOS y PERFECTOS antes de que lleguen rápido?")
    print("     👉 Usa TCP (Web, Correo, Archivos, BD, SSH).")
    print("   • ¿Prefieres que los datos lleguen YA MISMO aunque se pierda algún paquete?")
    print("     👉 Usa UDP (Streaming en vivo, VoIP, Juegos online, DNS).")
    print("=" * 75)


if __name__ == "__main__":
    mostrar_clasificacion()
    mostrar_tabla_comparativa()
    resumen_regla_de_oro()

