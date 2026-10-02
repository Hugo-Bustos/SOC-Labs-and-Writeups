# 🛡️ SOC & Blue Team Labs Portfolio
![Blue Team](https://img.shields.io/badge/Blue_Team-Defensive_Security-blue?style=for-the-badge)
![SOC Analyst](https://img.shields.io/badge/SOC-Analyst-darkred?style=for-the-badge)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT&CK-critical?style=for-the-badge)

![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-000000?style=for-the-badge&logo=splunk&logoColor=white)
![ElasticSearch](https://img.shields.io/badge/ELK_Stack-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

# SOC-Labs-and-Writeups
Repositorio de investigaciones, análisis de logs, laboratorios prácticos de SOC (SIEM, PCAP, Threat Hunting) y metodologías de mitigación.

Bienvenido a mi repositorio de laboratorios de Ciberseguridad Defensiva, análisis de incidentes y Threat Hunting. Este espacio documenta el análisis técnico, metodologías de investigación y medidas de mitigación para diversos escenarios de amenazas reales y simuladas.

---

##  Enfoque y Metodología
Cada laboratorio documentado incluye:
1. **Contexto de la Amenaza:** Escenario operativo y vectores de ataque.
2. **Análisis Técnico:** Evidencia en capturas de pantalla, análisis de paquetes (PCAP) y logs.
3. **Mapeo MITRE ATT&CK:** Identificación de TTPs (Tácticas, Técnicas y Procedimientos).
4. **Mitigación y Remediación:** Recomendaciones defensivas para la infraestructura.

---

## 📂 Índice de Laboratorios

### 📡 01. Análisis de Tráfico de Red (PCAPs & NTA)
* 🔹 **[Análisis de Red y Detección de Ataques MITM](<./Writeups/Análisis de Red y Detección de Ataques MITM (Man-in-the-Middle)>):** Inspección de tráfico no cifrado en Wireshark y extracción de credenciales expuestas en peticiones POST.

### 📊 02. Análisis de Logs & SIEM
* 🔹 **[Detección de Ataque Brute Force en LOGS](<./Scripts/Brute-Force/Analizador de logs (bruteforce def).py>):** Un script simple que ayuda a revisar logs e informar de potenciales peligros, como por ejemplo intentos de bruteforce.
* 🔹 **[Detección de Web Shells]

### 🔐 03. Criptografía 
* 🔹 **[Criptografía Simétrica](<./cryptography/Example with Fernet>):** Ejercicio de código que permite cifrar y descifrar mensajes usando Fernet (simétrico)
  
### 🧪 04. Investigaciones de Laboratorios
* 🔹 **[Grand Larceny Auto, LAB TRYHACKME: Reverse Engineering / .NET Logic Flaw](<./Writeups/Grand-Larceny-Auto-Tryhackme-soluci-n-linux-espa-ol>) :** Investigación de escalación de privilegios y persistencia en sistemas Linux.

---

## 🛠️ Herramientas Utilizadas
* **Monitoreo y Análisis:** Wireshark, Tshark, Splunk, ELK Stack, Brim.
* **Sistemas Operativos:** Linux (Kali / Ubuntu), Windows Server.
* **Scripting y Automatización:** Python (Scripting defensivo y procesamiento de JSON/CSV), Bash.

---
📫 **Contacto:** [LinkedIn](https://linkedin.com/in/hugo-bustos-fuentes) | [Portfolio Web](https://hugo-bustos.github.io)
