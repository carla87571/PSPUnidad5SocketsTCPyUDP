"""
04_gestion_de_errores_y_reintentos.py
=====================================
Diapositivas de referencia:
  • Diapositiva 5 ("Las redes fallan: try/except y timeouts: tu red de seguridad")
  • Diapositiva 6 ("El mapa de excepciones: Cada error, su tratamiento")

LAS REDES NO SON PERFECTAS:
---------------------------
Cables cortados, servidores saturados, cortes de WiFi o caídas repentinas son normales en redes.
Un código profesional debe anticipar estos fallos con timeouts y gestión de excepciones.

EL MAPA DE EXCEPCIONES EN PYTHON (Diapositiva 6):
-------------------------------------------------
  1. socket.timeout:
     -> Ocurre cuando send(), recv() o connect() tardan más del settimeout() configurado.
  2. ConnectionRefusedError:
     -> Nadie está escuchando en ese puerto en la máquina destino (al conectar).
  3. ConnectionResetError:
     -> El servidor o cliente remoto se cerró o reinició de golpe mientras hablabas.
  4. BrokenPipeError:
     -> Intentas escribir con sendall() en un socket cuyo otro extremo ya colgó.
  5. OSError:
     -> Error genérico del sistema operativo (red desconectada, DNS que no resuelve).

REGLA PRÁCTICA DE PYTHON:
-------------------------
Captura siempre primero las excepciones específicas y deja 'OSError' al final
como última red de protección.
"""

import socket
import time

def conectar_seguro(host, port, reintentos=3, timeout=1.0):
    """
    Función robusta de la Diapositiva 5:
    Implementa política de reintentos con timeouts y manejo específico de errores.
    """
    print(f"\n[Iniciando conexión segura hacia {host}:{port} (Máx {reintentos} intentos)]")

    for intento in range(1, reintentos + 1):
        try:
            print(f"  -> Intento {intento}/{reintentos}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)          # 1. Timeout de seguridad
                s.connect((host, port))        # 2. Conexión
                s.sendall(b"test")             # 3. Envío
                respuesta = s.recv(1024)       # 4. Recepción
                print("     ✔ ¡Conexión y respuesta exitosa!")
                return respuesta

        except socket.timeout:
            print(f"     ⏱ socket.timeout: El servidor tardó más de {timeout}s.")
        except ConnectionRefusedError:
            print("     🔴 ConnectionRefusedError: ¿El servidor está encendido?")
            time.sleep(0.5)  # Breve pausa antes del siguiente reintento
        except ConnectionResetError:
            print("     💥 ConnectionResetError: El servidor cerró la conexión de golpe.")
        except BrokenPipeError:
            print("     💔 BrokenPipeError: Intentamos escribir en una tubería ya rota.")
        except OSError as e:
            print(f"     🔱 OSError (Error de red genérico): {e}")

    print("  ❌ Todos los reintentos fallaron. Retornando None al llamador.")
    return None

def main():
    print("=" * 70)
    print("  04 - GESTIÓN ROBUSTA DE ERRORES Y POLÍTICA DE REINTENTOS")
    print("=" * 70)

    # 1. Tabla resumen de excepciones (Diapositiva 6)
    print("\n[1] EL MAPA DE EXCEPCIONES DE RED:")
    print("  • socket.timeout          -> La operación superó el tiempo límite")
    print("  • ConnectionRefusedError  -> Nadie escucha en ese puerto (al llamar)")
    print("  • ConnectionResetError    -> El otro lado cortó abruptamente (al hablar)")
    print("  • BrokenPipeError         -> Escribir en un socket que ya colgó")
    print("  • OSError                 -> Red caída, interfaz apagada, genérico")

    # 2. Prueba práctica llamando a un puerto cerrado (59999)
    print("\n[2] DEMOSTRACIÓN DE REINTENTOS CON SERVIDOR APAGADO:")
    resultado = conectar_seguro("127.0.0.1", 59999, reintentos=3, timeout=0.5)
    print(f"\n    Resultado devuelto: {resultado}")

    print("\n" + "=" * 70)
    print("  LECCIÓN: Con timeouts y reintentos, tu aplicación nunca se congela")
    print("  y puede recuperarse de micro-cortes en la red.")
    print("=" * 70)

if __name__ == "__main__":
    main()

