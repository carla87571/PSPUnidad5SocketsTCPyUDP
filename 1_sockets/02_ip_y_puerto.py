"""
02_ip_y_puerto.py
=================
Diapositiva de referencia: Diapositiva 3 ("IP y puerto: El «quién» y el «dónde»")

EL «QUIÉN» Y EL «DÓNDE» EN REDES:
---------------------------------
Para que dos programas se comuniquen a través de la red, necesitan dos datos:

1. DIRECCIÓN IP («¿A qué máquina voy?»):
   - Identifica la máquina (computadora, servidor, celular) en la red.
   - Ejemplo: 192.168.1.10 (en tu red local) o 142.250.190.46 (un servidor web).
   - CASO ESPECIAL: 127.0.0.1 es "localhost" (tu propia máquina).
     ¡Es ideal para hacer pruebas de desarrollo sin necesitar conexión a internet!

2. PUERTO («¿Con qué programa dentro de esa máquina quiero hablar?»):
   - Una computadora ejecuta muchos programas a la vez (navegador, base de datos, chat).
   - El puerto es un número del 0 al 65535 que identifica el programa específico:
     * 0 a 1023: Puertos "bien conocidos" o reservados por el SO (ej: 80 = HTTP, 443 = HTTPS, 22 = SSH).
     * 1024 a 65535: Puertos de usuario / altos (ej: 5000, 8000, 9000). ¡Estos son los que usamos para nuestros programas!

3. ENDPOINT / DIRECCIÓN DE SOCKET:
   - La combinación (IP, Puerto) se denomina "endpoint".
   - En Python se representa siempre como una TUPLA de dos elementos:
     direccion = ("127.0.0.1", 5000)
"""

import socket

def main():
    print("=" * 65)
    print("  02 - IP Y PUERTO: EL «QUIÉN» Y EL «DÓNDE»")
    print("=" * 65)

    # 1. Definición de un Endpoint en Python
    ip_localhost = "127.0.0.1"
    puerto_app = 5000
    
    # En Python, el endpoint es una tupla: (IP, Puerto)
    endpoint = (ip_localhost, puerto_app)

    print("\n[1] REPRESENTACIÓN EN PYTHON:")
    print(f"    • IP (La máquina):               {ip_localhost} -> 'localhost'")
    print(f"    • Puerto (El programa):          {puerto_app} -> (Puerto alto / libre)")
    print(f"    • Tupla Endpoint de Python:      {endpoint}")
    print(f"    • Tipo de dato:                  {type(endpoint)}")

    # 2. Rango de puertos explicados
    print("\n[2] EL RANGO DE PUERTOS (0 a 65535):")
    print("    • 0 a 1023    -> Reservados por el Sistema Operativo (requieren admin/root)")
    print("                     Ejemplos: 80 (HTTP), 443 (HTTPS), 22 (SSH), 53 (DNS)")
    print("    • 1024 a 65535 -> Puertos altos / de usuario")
    print("                     Ideales para nuestros scripts: 5000, 8080, 9000")

    # 3. Comprobación práctica con la librería socket
    print("\n[3] UTILIDAD DE 'socket.gethostbyname':")
    try:
        ip_resuelta = socket.gethostbyname("localhost")
        print(f"    -> Al resolver el nombre 'localhost', obtenemos la IP: {ip_resuelta}")
    except socket.error as e:
        print(f"    -> Error al resolver nombre: {e}")

    # 4. Resumen clave
    print("\n[4] REGLA DE ORO:")
    print("    ¡Recuerda pasar siempre una TUPLA a las funciones de sockets de Python!")
    print("    Correcto:   s.bind(('127.0.0.1', 5000))")
    print("    Incorrecto: s.bind('127.0.0.1', 5000)  <-- Provocaría TypeError")
    print("=" * 65)

if __name__ == "__main__":
    main()

