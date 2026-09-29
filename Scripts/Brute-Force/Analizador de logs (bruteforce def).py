# Analizador de logs para detección de Brute Force con Timestamps
ruta_archivo = "accesos.log"
UMBRAL = 5
INDICADOR_FALLO = "401"

# Ahora el diccionario guardará un sub-diccionario con fallos, inicio y fin.
conteo_ips = {}

print("Iniciando análisis de logs...\n")

try:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if INDICADOR_FALLO in linea and "POST /login" in linea:
                partes = linea.split()
                
                # Formato esperado: Fecha Hora IP Metodo Ruta Status Usuario
                if len(partes) > 3:
                    fecha = partes[0]
                    hora = partes[1]
                    ip = partes[2]
                    
                    timestamp = f"{fecha} {hora}"
                    
                    # Si es la primera vez que vemos esta IP fallar, la registramos
                    if ip not in conteo_ips:
                        conteo_ips[ip] = {
                            "fallos": 1,
                            "primer_intento": timestamp,
                            "ultimo_intento": timestamp
                        }
                    # Si la IP ya existe, sumamos el fallo y actualizamos la hora del último intento
                    else:
                        conteo_ips[ip]["fallos"] += 1
                        conteo_ips[ip]["ultimo_intento"] = timestamp

    # Evaluación e impresión de alertas
    for ip_atacante, datos in conteo_ips.items():
        if datos["fallos"] >= UMBRAL:
            print(f" ¡ALERTA DE SEGURIDAD! ")
            print(f"Posible ataque de Brute Force detectado.")
            print(f"Origen: {ip_atacante}")
            print(f"Intentos fallidos: {datos['fallos']}")
            print(f"Inicio del ataque: {datos['primer_intento']}")
            print(f"Último intento: {datos['ultimo_intento']}\n")
            print("-" * 40)

except FileNotFoundError:
    print(f" Error: No se encontró el archivo '{ruta_archivo}'.")
