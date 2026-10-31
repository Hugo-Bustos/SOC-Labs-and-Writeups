# Writeup: Linux Logging & Runtime Monitoring para SOC 

![Role](https://img.shields.io/badge/Role-Senior_SOC_Analyst-2a3d66?style=for-the-badge&logo=linux)
![Nivel](https://img.shields.io/badge/Nivel-Intermedio%2FAvanzado-bf360c?style=for-the-badge)
![TryHackMe](https://img.shields.io/badge/TryHackMe-Linux_Logging_for_SOC-111927?style=for-the-badge&logo=tryhackme&logoColor=white)
![OS](https://img.shields.io/badge/OS-Ubuntu_Linux-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Herramientas](https://img.shields.io/badge/Tools-Auditd%20%7C%20Grep%20%7C%20Ausearch-004d40?style=for-the-badge)

## Introducción

En el ecosistema corporativo moderno, Linux es la columna vertebral de la infraestructura crítica, alojando desde servidores web hasta bases de datos y clústeres en la nube. Contrario a la creencia popular, los entornos Linux son un objetivo prioritario para los actores de amenazas (APTs). En este laboratorio, asumimos el rol de analistas SOC para realizar un triage forense y cacería de amenazas (Threat Hunting), correlacionando eventos desde archivos de texto plano tradicionales hasta el monitoreo de llamadas al sistema (syscalls) en tiempo real mediante auditd.


## La Importancia del Monitoreo en Linux🐧

Para un Blue Team, la visibilidad es la diferencia entre contener un incidente en minutos o descubrir una brecha meses después de la exfiltración de datos. La recolección estructurada de logs en Linux permite:

✔️ Reconstruir Líneas de Tiempo (Timelining): Rastrear la actividad del atacante desde el compromiso inicial (fuerza bruta SSH) hasta el movimiento lateral o impacto.

✔️ Identificar TTPs: Mapear el comportamiento del atacante utilizando el framework MITRE ATT&CK (ej. T1110 para fuerza bruta, T1105 para transferencia de herramientas).

✔️ Auditoría de Integridad: Detectar la manipulación de configuraciones críticas o la creación de usuarios encubiertos (backdoors).

## Desafíos Operativos para el SOC

✔️ Monitorear sistemas Linux presenta barreras arquitectónicas que todo analista senior debe sortear:

✔️ Falta de Estandarización: A diferencia de los Event IDs estructurados de Windows, los logs de Linux suelen ser texto plano no estructurado que varía drásticamente entre distribuciones (Debian vs. RHEL).

✔️ Ruido Excesivo: Archivos como /var/log/syslog ingieren miles de eventos por minuto generados por procesos benignos y tareas cron, dificultando la extracción de la señal maliciosa.

✔️ Puntos Ciegos Nativos: Por defecto, Linux no registra la creación de procesos efímeros, conexiones de red o modificaciones a archivos a nivel de kernel. Los atacantes pueden evadir el historial (~/.bash_history) fácilmente. Esto hace obligatorio el despliegue de herramientas de Runtime Monitoring como auditd o motores eBPF.

## Metodología de Investigación y Ejecución de Comandos

A continuación, se detalla el flujo de investigación y los comandos ejecutados durante la respuesta a incidentes.

1. Triage Inicial y Correlación de Tiempo (/var/log/syslog)

Antes de analizar anomalías, es crucial verificar que el reloj del servidor esté sincronizado (NTP) para que los timestamps de los logs coincidan con la red global. También auditamos los mensajes del kernel (ej. el módulo de seguridad Yama).

```Bash

# Identificar el servidor de tiempo contactado por el sistema
grep -i "Contacted time server" /var/log/syslog

# Verificar mensajes de inicialización de módulos de seguridad del Kernel
grep -i "yama" /var/log/syslog
```
2. Auditoría de Autenticación y Persistencia (/var/log/auth.log)

El archivo de autenticación es la primera línea de defensa para detectar intrusiones por red y escalado de privilegios. Buscamos rastros de fuerza bruta por SSH y la creación no autorizada de cuentas administrativas.

```Bash

# Agrupar y contar intentos fallidos de inicio de sesión SSH (Fuerza Bruta)
grep "Failed password" /var/log/auth.log | awk '{print $11, $9}' | sort | uniq -c

# Detectar creación de cuentas persistentes y adición al grupo sudo (T1136.001)
grep -E 'useradd|usermod' /var/log/auth.log
```
3. Rastreo de Artefactos e Historial de Usuarios

Los atacantes suelen instalar utilidades (como unzip, nmap o netcat) para facilitar la manipulación de archivos y el reconocimiento. Auditamos el gestor de paquetes de Debian y forzamos la lectura del historial de todos los usuarios ignorando advertencias de permisos.
