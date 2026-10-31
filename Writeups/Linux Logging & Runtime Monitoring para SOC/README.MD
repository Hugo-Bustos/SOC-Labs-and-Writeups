# Writeup: Linux Logging & Runtime Monitoring para SOC 

![Role](https://img.shields.io/badge/Role-Senior_SOC_Analyst-2a3d66?style=for-the-badge&logo=linux)
![Nivel](https://img.shields.io/badge/Nivel-Intermedio%2FAvanzado-bf360c?style=for-the-badge)
![TryHackMe](https://img.shields.io/badge/TryHackMe-Linux_Logging_for_SOC-111927?style=for-the-badge&logo=tryhackme&logoColor=white)
![OS](https://img.shields.io/badge/OS-Ubuntu_Linux-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Herramientas](https://img.shields.io/badge/Tools-Auditd%20%7C%20Grep%20%7C%20Ausearch-004d40?style=for-the-badge)

<img src="Assets/Portada Linux.jpg" width="1080">

## Introducción

En el ecosistema corporativo moderno, Linux es la columna vertebral de la infraestructura crítica, alojando desde servidores web hasta bases de datos y clústeres en la nube. Contrario a la creencia popular, los entornos Linux son un objetivo prioritario para los actores de amenazas (APTs). En este laboratorio, asumimos el rol de analistas SOC para realizar un triage forense y cacería de amenazas (Threat Hunting), correlacionando eventos desde archivos de texto plano tradicionales hasta el monitoreo de llamadas al sistema (syscalls) en tiempo real mediante auditd.


## Resumen 

Se investigó un servidor Ubuntu Linux comprometido tras alertas de actividad anómala. El análisis forense reveló que un adversario logró acceso mediante un ataque de fuerza bruta SSH. Una vez dentro, el atacante estableció persistencia (creación de cuentas en grupo `sudo`), ejecutó técnicas de evasión de defensas (deshabilitando el EDR local) y utilizó la herramienta `wget` para descargar el escáner de red **Naabu**. El incidente culminó con un escaneo interno hacia el segmento `192.168.50.0/24` y la búsqueda sistemática de archivos confidenciales.

## La Importancia del Monitoreo en Linux🐧

- Para un Blue Team, la visibilidad es la diferencia entre contener un incidente en minutos o descubrir una brecha meses después de la exfiltración de datos. La recolección estructurada de logs en Linux permite:

- Reconstruir Líneas de Tiempo (Timelining): Rastrear la actividad del atacante desde el compromiso inicial (fuerza bruta SSH) hasta el movimiento lateral o impacto.

- Identificar TTPs: Mapear el comportamiento del atacante utilizando el framework MITRE ATT&CK (ej. T1110 para fuerza bruta, T1105 para transferencia de herramientas).

- Auditoría de Integridad: Detectar la manipulación de configuraciones críticas o la creación de usuarios encubiertos (backdoors).

## Desafíos Operativos para el SOC

- Monitorear sistemas Linux presenta barreras arquitectónicas que todo analista senior debe sortear:

- Falta de Estandarización: A diferencia de los Event IDs estructurados de Windows, los logs de Linux suelen ser texto plano no estructurado que varía drásticamente entre distribuciones (Debian vs. RHEL).

- Ruido Excesivo: Archivos como /var/log/syslog ingieren miles de eventos por minuto generados por procesos benignos y tareas cron, dificultando la extracción de la señal maliciosa.

- Puntos Ciegos Nativos: Por defecto, Linux no registra la creación de procesos efímeros, conexiones de red o modificaciones a archivos a nivel de kernel. Los atacantes pueden evadir el historial (~/.bash_history) fácilmente. Esto hace obligatorio el despliegue de herramientas de Runtime Monitoring como auditd o motores eBPF.


## Matriz MITRE ATT&CK 

| Táctica | ID Técnica | Nombre de la Técnica | Evidencia en el Incidente |
| :--- | :--- | :--- | :--- |
| **Credential Access** | T1110.001 | Brute Force: Password Guessing | Logs SSH con masivos `Failed password`. |
| **Persistence** | T1136.001 | Create Account: Local Account | Uso de `useradd` y `usermod` para cuenta `backdoor`. |
| **Defense Evasion** | T1562.001 | Disable or Modify Tools | Ejecución vía sudo para detener el EDR. |
| **Command and Control**| T1105 | Ingress Tool Transfer | Uso de `wget` para descargar el binario Naabu. |
| **Discovery** | T1083 | File and Directory Discovery | Uso de `find` buscando la cadena `*secret*`. |


## Indicadores de Compromiso (IoCs)

| Tipo de IoC | Valor / Artefacto | Descripción |
| :--- | :--- | :--- |
| **Cuenta** | `backdoor` (UID=1002) | Cuenta persistente agregada al grupo `sudo`. |
| **Comando** | `systemctl stop edr` | Desactivación del agente de seguridad local. |
| **Herramienta** | `naabu_2.3.5_linux_amd64.zip` | Escáner de puertos descargado vía GitHub en `/tmp`. |
| **Ruta de red** | `192.168.50.0/24` | Segmento de red interna comprometido/escaneado. |

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
<img src="Assets/Screenshot_11.png" width="1080">
<img src="Assets/Screenshot_12.png" width="1080">

2. Auditoría de Autenticación y Persistencia (/var/log/auth.log)

El archivo de autenticación es la primera línea de defensa para detectar intrusiones por red y escalado de privilegios. Buscamos rastros de fuerza bruta por SSH y la creación no autorizada de cuentas administrativas.

```Bash

# Agrupar y contar intentos fallidos de inicio de sesión SSH (Fuerza Bruta)
grep "Failed password" /var/log/auth.log | awk '{print $11, $9}' | sort | uniq -c

# Detectar creación de cuentas persistentes y adición al grupo sudo (T1136.001)
grep -E 'useradd|usermod' /var/log/auth.log
```
<img src="Assets/Screenshot_13.png" width="1080">
<img src="Assets/Screenshot_14.png" width="1080">

3. Rastreo de Artefactos e Historial de Usuarios

Los atacantes suelen instalar utilidades (como unzip, nmap o netcat) para facilitar la manipulación de archivos y el reconocimiento. Auditamos el gestor de paquetes de Debian y forzamos la lectura del historial de todos los usuarios ignorando advertencias de permisos.

```Bash

# Identificar la versión exacta de las herramientas instaladas recientemente
grep "unzip" /var/log/dpkg.log

# Leer de forma recursiva y con privilegios el historial de bash de todos los usuarios
sudo cat /home/*/.bash_history /root/.bash_history 2>/dev/null

# Buscar la flag del desafío para este caso
sudo grep -i "THM" /home/*/.bash_history /root/.bash_history 2>/dev/null
```
<img src="Assets/Screenshot_15.png" width="1080">
<img src="Assets/Screenshot_16.png" width="1080">

4. Runtime Monitoring y Reconstrucción del Ataque (auditd)

Para suplir las deficiencias de los logs nativos, utilizamos ausearch para interactuar con los registros de auditd (ubicados en /var/log/audit/audit.log). Esto nos permitió ver las llamadas al sistema exactas que realizó el atacante.

```Bash

# Investigar el acceso no autorizado a archivos sensibles (FIM)
sudo ausearch -i -k file_thmsecret

# Descubrir la ingesta de herramientas (Transferencia de archivos vía wget)
sudo ausearch -i -k proc_wget
```
<img src="Assets/Screenshot_17.png" width="1080">

## Hallazgo Crítico (Reconstrucción Final):
Gracias al monitoreo de procesos de auditd (EXECVE), logramos aislar la cadena de ejecución final. El atacante descargó la herramienta de escaneo rápido Naabu (mediante la clave proc_wget). Posteriormente, listó el directorio temporal con ls /tmp, le asignó permisos de ejecución mediante chmod +x naabu, y ejecutó un escaneo de puertos agresivo contra la red interna apuntando al segmento 192.168.50.0/24. Finalizó su actividad realizando una búsqueda generalizada de archivos confidenciales con el comando find / -name *secret* -type f.   


<img src="Assets/Screenshot_18.png" width="1080">
<img src="Assets/Screenshot_19.png" width="1080">

## Recomendaciones y Plan de Remediación

1. **Hardening de SSH:** Deshabilitar inmediatamente la autenticación por contraseñas (`PasswordAuthentication no` en `/etc/ssh/sshd_config`) y forzar autenticación exclusiva por llaves PKI (Ed25519 o RSA).
2. **Mitigación de Fuerza Bruta:** Desplegar herramientas de bloqueo automático como **Fail2Ban** o **CrowdSec** para bloquear IPs que superen un umbral de intentos fallidos.
3. **Restricción de Directorios (Prevención de Ejecución):** Montar las particiones temporales (`/tmp` y `/var/tmp`) con la bandera `noexec` en el archivo `/etc/fstab` para evitar que scripts o binarios descargados por atacantes puedan ejecutarse directamente desde allí.
4. **Centralización de Logs (SIEM):** Configurar `rsyslog` o `syslog-ng` para enviar los registros de `/var/log` y `audit.log` a un SIEM centralizado. Esto previene que un atacante destruya la evidencia borrando los logs locales.

## Conclusión

Este incidente subraya de manera irrefutable que los registros de texto plano (syslog, auth.log) son insuficientes para detectar operaciones adversarias avanzadas si no se complementan con telemetría a nivel de Kernel. La integración de auditd en la estrategia de monitorización del SOC no es opcional; es el mecanismo definitivo que nos permitió pasar de simplemente saber "que alguien entró", a comprender con exactitud criptográfica qué herramientas descargaron, qué comandos exactos ejecutaron, qué infraestructura interna fue escaneada y qué archivos críticos se vieron comprometidos.
