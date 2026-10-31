from collections import defaultdict, deque
from datetime import datetime, timedelta

RUTA_ARCHIVO = "accesos.log"
UMBRAL = 5
VENTANA = timedelta(minutes=5)

# Formato esperado por línea:
# Fecha Hora IP Metodo Ruta Status Usuario
# Ejemplo:
# 2026-10-01 12:00:00 192.168.1.10 POST /login 401 admin

formato_timestamp = "%Y-%m-%d %H:%M:%S"

# Cada IP mantiene una ventana deslizante de timestamps de fallos.
eventos_por_ip = defaultdict(deque)


def procesar_evento(ip, timestamp):
    """Registra un fallo y devuelve True cuando alcanza el umbral dentro de la ventana."""
    eventos = eventos_por_ip[ip]
    limite = timestamp - VENTANA

    # Eliminamos eventos fuera de la ventana temporal.
    while eventos and eventos[0] < limite:
        eventos.popleft()

    eventos.append(timestamp)

    return len(eventos) >= UMBRAL


print("Iniciando análisis de logs...\n")

try:
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            partes = linea.split()

            if len(partes) < 6:
                print(f"Línea {numero_linea}: formato inválido, se omite.")
                continue

            fecha, hora, ip, metodo, ruta, status = partes[:6]

            # Se analiza únicamente POST /login con HTTP 401 exacto.
            if metodo != "POST" or ruta != "/login" or status != "401":
                continue

            try:
                timestamp = datetime.strptime(
                    f"{fecha} {hora}", formato_timestamp
                )
            except ValueError:
                print(f"Línea {numero_linea}: timestamp inválido, se omite.")
                continue

            if procesar_evento(ip, timestamp):
                cantidad = len(eventos_por_ip[ip])
                inicio = eventos_por_ip[ip][0]

                print("¡ALERTA DE SEGURIDAD!")
                print("Posible ataque de Password Guessing detectado.")
                print(f"Origen: {ip}")
                print(f"Intentos 401 dentro de la ventana: {cantidad}")
                print(f"Ventana: {inicio} → {timestamp}")
                print(f"Duración máxima evaluada: {VENTANA}")
                print("-" * 50)

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{RUTA_ARCHIVO}'.")
except OSError as error:
    print(f"Error al leer '{RUTA_ARCHIVO}': {error}")
