# 🛡️ Writeup: Análisis Forense y Threat Hunting con Windows Event Logs, Sysmon y PowerShell

![TryHackMe](https://img.shields.io/badge/TryHackMe-SOC_Level_1-red?style=for-the-badge&logo=tryhackme)
![Windows Logs](https://img.shields.io/badge/Windows-Event_Viewer-0078D6?style=for-the-badge&logo=windows)
![Sysmon](https://img.shields.io/badge/Sysinternals-Sysmon-blue?style=for-the-badge)
![PowerShell](https://img.shields.io/badge/DFIR-PowerShell-5391FE?style=for-the-badge&logo=powershell)

## Resumen Ejecutivo
Este reporte documenta la investigación forense de un endpoint Windows comprometido. Mediante el análisis de registros de seguridad nativos (Security.evtx), telemetría avanzada de procesos (Sysmon) y artefactos locales (PSReadline), se logró reconstruir la cadena de ataque (Kill Chain) completa. El adversario obtuvo acceso mediante fuerza bruta por RDP, estableció persistencia creando cuentas *backdoor*, ejecutó cargas útiles descargadas de un servidor de Comando y Control (C2), y utilizó técnicas de *Living off the Land* (LotL) con PowerShell para descubrimiento y evasión de defensas.

---

## Análisis Táctico de la Cadena de Ataque (Kill Chain)

### 1. Acceso Inicial (Initial Access)
El análisis del Visor de Eventos reveló un ataque de fuerza bruta exitoso contra el servicio RDP del equipo `THM-PC`.
* **Event IDs Involucrados:** `4625` (Fallo de autenticación) seguido de un `4624` (Autenticación exitosa Logon Type 10).
* **IP Atacante:** `10.10.53.248` | **Cuenta Comprometida:** `Administrator`
* **Logon ID Malicioso:** `0x183c36d`
* **Explicación Lógica:** Los atacantes automatizan intentos de login contra puertos RDP expuestos. Identificar el `Logon ID` del evento 4624 exitoso es el paso más crítico en esta fase, ya que actúa como una "huella digital" criptográfica que permite al SOC rastrear todas las acciones administrativas posteriores vinculadas a esa sesión específica.

### 2. Persistencia y Escalada de Privilegios (Persistence & Privilege Escalation)
Utilizando la sesión secuestrada, el atacante manipuló la gestión de usuarios locales para asegurar su acceso de forma sigilosa.
* **Event IDs:** `4720` (Creación de cuenta) y `4732` (Adición de miembro a un grupo local).
* **Cuenta Backdoor:** `svc_sysrestore` (Nombrada para camuflarse como un servicio legítimo).
* **Grupos Asignados:** `Backup Operators` y `Remote Desktop Users`.
* **Explicación Lógica:** En lugar de añadirse simplemente al grupo de Administradores (lo cual es muy ruidoso y monitoreado), el atacante utilizó `Backup Operators`. Este grupo permite eludir las Listas de Control de Acceso (ACLs) de Windows para realizar copias de seguridad, lo que se utiliza maliciosamente para extraer los archivos críticos `SAM` y `SYSTEM` del registro y volcar hashes de contraseñas offline.

### 3. Ejecución y Entrega (Execution & Delivery)
Apoyándonos en la telemetría de Sysmon, se detectó la descarga de un artefacto malicioso a través de un usuario estándar.
* **Sysmon Event ID 1 (Process Creation):** Confirmó que el usuario `sarah.miller` ejecutó `chrome.exe` como proceso padre.
* **Sysmon Event ID 15 (FileCreateStreamHash):** Extracción del flujo *Mark of the Web* (MotW).
* **Payload:** `ckjg.exe` | **URL de Origen:** `http://gettsveriff.com/bgj3/ckjg.exe`
* **Explicación Lógica:** Cuando un archivo se descarga de internet, Windows le adjunta un metadato (MotW) para marcarlo como no confiable. Sysmon captura esto magistralmente. Para el SOC, extraer la URL de origen desde la vista XML del log es vital para bloquear el dominio perimetralmente e identificar otras posibles víctimas en la red.

### 4. Comando y Control (Command & Control)
Una vez ejecutado, el malware inició comunicaciones de red anómalas.
* **Sysmon Event ID 3 (Network Connection) & ID 22 (DNS Query):** 
* **IP y Puerto C2:** `193.46.217.4:7777` | **Dominio C2:** `hkfasfsafg.click`
* **Explicación Lógica:** El malware utilizó un dominio generado por algoritmos (DGA) para resolver la IP del servidor atacante. La comunicación se estableció por el puerto 7777, un claro indicador de anomalía, ya que el tráfico web estándar opera en los puertos 80/443.

### 5. Persistencia del Malware
El ejecutable generó un mecanismo de auto-inicio.
* **Sysmon Event ID 11 (File Create):** Archivo `DeleteApp.url` en `C:\Users\sarah.miller\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`.
* **Explicación Lógica:** Colocar accesos directos o ejecutables en la carpeta `Startup` garantiza que el código malicioso vuelva a inyectarse en la memoria cada vez que la víctima encienda su computadora, asegurando el control continuo del botnet o C2.

### 6. Pos-Explotación (Post-Exploitation & Evasion)
El adversario utilizó comandos directos en PowerShell para reconocimiento, ocultando su actividad de los logs de procesos estándar.
* **Artefacto Forense:** `ConsoleHost_history.txt` (Ruta: `AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\`).
* **Actividad Detectada:**
  * Descubrimiento: `get-localuser > users.txt`, `get-smbshare > shares.txt`
  * Evasión de Defensas: `get-mppreference > defender.txt` (auditoría del AV nativo) y `clear-recyclebin`.
* **Explicación Lógica:** PowerShell permite ejecutar cientos de comandos dentro de un único proceso (`powershell.exe`). Por lo tanto, Sysmon Event ID 1 se vuelve ciego al contenido de la sesión. Auditar el archivo de historial de PSReadline permite al analista SOC ver exactamente qué tecleó el atacante en la terminal.

---

## Indicadores de Compromiso (IoCs)

| Categoría | Indicador | Descripción Forense |
| :--- | :--- | :--- |
| **Network (IP)** | `10.10.53.248` | IP Atacante (Origen del Brute Force RDP). |
| **Network (IP)** | `193.46.217.4:7777` | IP y Puerto del servidor C2. |
| **Network (Domain)** | `hkfasfsafg.click` | Dominio DGA C2 resuelto por el malware. |
| **Network (URL)** | `http://gettsveriff.com/bgj3/ckjg.exe` | Vector de entrega del payload malicioso. |
| **Host (File)** | `ckjg.exe` | Ejecutable malicioso droppeado inicial. |
| **Host (File)** | `DeleteApp.url` | Archivo de persistencia en carpeta Startup. |
| **Host (Account)** | `svc_sysrestore` | Cuenta backdoor local con privilegios elevados. |

---

## Conclusiones
El incidente demuestra una intrusión estructurada que aprovechó la exposición del puerto RDP para obtener acceso inicial. Una vez dentro, el adversario demostró un conocimiento intermedio-avanzado del ecosistema Windows, prefiriendo técnicas de *Living off the Land* (LotL) para evadir la detección y manipular grupos de usuarios no convencionales (`Backup Operators`) para la potencial extracción de credenciales. La contención requerirá no solo la eliminación de los binarios maliciosos y el bloqueo de IPs/Dominios, sino también una auditoría profunda de las cuentas locales y el cierre inmediato de la exposición RDP hacia internet.

## 🧠 Aprendizajes Clave como Analista SOC
1. **El Poder de la Correlación (Logon ID):** Identificar de forma aislada una alerta de creación de usuario (4720) no cuenta toda la historia. Vincular el `Logon ID` de ese evento con el `Logon ID` de un inicio de sesión de red (4624) es lo que permite atribuir la acción administrativa a un intruso remoto específico.
2. **Limitaciones de las Herramientas GUI:** El Visor de Eventos de Windows formatea los datos para hacerlos amigables, pero a menudo oculta o recorta campos vitales (como el `HostUrl` en el Evento 15 de Sysmon). Aprender a auditar los logs en su **Vista XML** es una habilidad obligatoria para extraer telemetría en crudo.
3. **Visibilidad de Sysmon vs. Windows Logs:** Mientras que los logs nativos (4688) ofrecen una visión limitada, Sysmon es imprescindible para la caza de amenazas moderna, permitiendo vincular procesos padre/hijo, resoluciones DNS y flujos de red en una sola línea de investigación.
4. **Resiliencia de la Telemetría (PSReadline):** Cuando los atacantes utilizan herramientas nativas
