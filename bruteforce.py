logs = """
2026-08-12 01:14:03 192.168.10.45 POST /login 401 usuario=admin
2026-08-12 01:14:09 192.168.10.45 POST /login 401 usuario=admin
2026-08-12 01:14:16 192.168.10.45 POST /login 401 usuario=admin
2026-08-12 01:14:24 192.168.10.45 POST /login 401 usuario=admin
2026-08-12 01:14:31 192.168.10.45 POST /login 401 usuario=admin
2026-08-12 01:14:39 192.168.10.45 POST /login 401 usuario=admin
2026-08-12 01:15:02 192.168.10.45 POST /login 200 usuario=admin
"""

ip_objetivo = "192.168.10.45"
UMBRAL = 5

fallos = logs.count(f"{ip_objetivo} POST /login 401")

print(f"IP analizada: {ip_objetivo}")
print(f"Total de intentos fallidos: {fallos}")

if fallos > UMBRAL:
    print(f"¡ALERTA! Se superó el umbral de {UMBRAL} fallos. Posible Ataque de Brute Force.")
