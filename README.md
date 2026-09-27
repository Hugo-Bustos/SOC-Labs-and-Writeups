# SOC-Labs-and-Writeups
Repositorio de investigaciones, análisis de logs, laboratorios prácticos de SOC (SIEM, PCAP, Threat Hunting) y metodologías de mitigación.

# 🛡️ SOC & Blue Team Labs Portfolio

Bienvenido a mi repositorio de laboratorios de Ciberseguridad Defensiva, análisis de incidentes y Threat Hunting. Este espacio documenta el análisis técnico, metodologías de investigación y medidas de mitigación para diversos escenarios de amenazas reales y simuladas.

---

##  Enfoque y Metodología
Cada laboratorio documentado incluye:
1. **Contexto de la Amenaza:** Escenario operativo y vectores de ataque.
2. **Análisis Técnico:** Evidencia en capturas de pantalla, análisis de paquetes (PCAP) y logs.
3. **Mapeo MITRE ATT&CK:** Identificación de TTPs (Tácticas, Técnicas y Procedimientos).
4. **Mitigación y Remediación:** Recomendaciones defensivas para la infraestructura.

---

## Índice de Laboratorios

###  01. Análisis de Tráfico de Red (PCAPs & NTA)
* 🔹 **[MITM / On-Path Attack Analysis](./01-Network-Traffic-Analysis/MITM-On-Path-Attack/):** Inspección de tráfico no cifrado en Wireshark y extracción de credenciales expuestas en peticiones POST.

###  02. Análisis de Logs & SIEM
* 🔹 **[Detección de Ataque Brute Force](./02-Log-Analysis-and-SIEM/SSH-Brute-Force-Detection/):** Identificación de patrones de intentos fallidos de autenticación en logs de servicios web/SSH usando Python.

###  03. Investigaciones de Laboratorios Destacados
* 🔹 **[TryHackMe - Grand Larceny Auto](./02-Log-Analysis-and-SIEM/Grand-Larceny-Auto/):** Investigación de escalación de privilegios y persistencia en sistemas Linux.

---

## 🛠️ Herramientas Utilizadas
* **Monitoreo y Análisis:** Wireshark, Tshark, Splunk, ELK Stack, Brim.
* **Sistemas Operativos:** Linux (Kali / Ubuntu), Windows Server.
* **Scripting y Automatización:** Python (Scripting defensivo y procesamiento de JSON/CSV), Bash.

---
📫 **Contacto:** [LinkedIn](https://linkedin.com/in/hugo-bustos-fuentes) | [Portfolio Web](https://hugo-bustos.github.io)
