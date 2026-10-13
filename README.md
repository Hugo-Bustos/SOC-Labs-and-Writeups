# 🛡️ Hugo Bustos — SOC & Blue Team Portfolio

<img src="SOC HB.png" width="1080">

![Blue Team](https://img.shields.io/badge/Blue_Team-Defensive_Security-blue?style=for-the-badge)
![SOC Analyst](https://img.shields.io/badge/SOC-Analyst-darkred?style=for-the-badge)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT&CK-critical?style=for-the-badge)

![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-000000?style=for-the-badge&logo=splunk&logoColor=white)
![ElasticSearch](https://img.shields.io/badge/ELK_Stack-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

Bienvenido (a) a mi repositorio de investigaciones, análisis de logs, laboratorios prácticos de SOC (SIEM, PCAP, Threat Hunting) y metodologías de mitigación.

En este repositorio he ido documentando distintos laboratorios de Ciberseguridad Defensiva, análisis de incidentes y Threat Hunting. Con un enfoque en el análisis técnico, metodologías de investigación y medidas de mitigación para diversos escenarios para potenciales amenazas.

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
* 🔹 **[Análisis de logs en error 401](<./Scripts/Analizador 401.py>): Detection Engineering básico para logs enfocado en el error 401.
* 🔹 **[Detección de Web Shells (Incident Response)](<./Writeups/Detecting Web Shells>):** Análisis forense de logs de Apache utilizando herramientas CLI (grep, awk) para reconstruir la inyección y ejecución de una Web Shell maliciosa
* 🔹 **[Detección de ataque web DDoS](<./Writeups/Detecting Web DDoS (TryHackMe)>):** Análisis defensivo frente a una botnet atacando recursos web. Incluye procesamiento de logs en terminal, correlación avanzada de eventos con Splunk y estrategias de prevención.  

### 🔐 03. Criptografía 
* 🔹 **[Criptografía Simétrica](<./cryptography/Example with Fernet>):** Ejercicio de código que permite cifrar y descifrar mensajes usando Fernet (simétrico)
  
### 🧪 04. Investigaciones de Laboratorios
* 🔹 **[Grand Larceny Auto, LAB TRYHACKME: Reverse Engineering](<./Writeups/Grand-Larceny-Auto-Tryhackme-soluci-n-linux-espa-ol>) :** Investigación de escalación de privilegios y persistencia en sistemas Linux.

---

## 🛠️ Herramientas Utilizadas
* **Monitoreo y Análisis:** Wireshark, Tshark, Splunk, ELK Stack, Brim.
* **Sistemas Operativos:** Linux (Kali / Ubuntu), Windows Server.
* **Scripting y Automatización:** Python (Scripting defensivo y procesamiento de JSON/CSV), Bash.

## 🧠 Principios que estoy aplicando

Durante el desarrollo de este portafolio estoy intentando aplicar los siguientes principios de análisis:

- **La evidencia debe respaldar la conclusión.** No considero un evento sospechoso como un incidente confirmado sin analizar su contexto y buscar evidencia adicional.

- **El contexto importa.** La misma actividad puede ser legítima o maliciosa dependiendo del sistema afectado, el usuario, el momento, la frecuencia y el comportamiento esperado.

- **Las detecciones deben ser medibles.** Un umbral o una regla de detección debe poder explicarse, probarse y evaluarse mediante escenarios positivos y negativos.

- **Los falsos positivos forman parte del problema.** Una detección útil no solamente debe encontrar amenazas; también debe evitar generar una cantidad innecesaria de alertas irrelevantes.

- **La correlación temporal es fundamental.** La relación entre eventos y el intervalo de tiempo en que ocurren puede ser determinante para distinguir actividad normal de comportamiento automatizado o malicioso.

- **Las herramientas no reemplazan el razonamiento.** Wireshark, Splunk, Linux, Python u otras herramientas permiten obtener y procesar información, pero la interpretación de esa información sigue dependiendo del analista.

- **Una investigación debe ser reproducible.** Intento documentar los comandos, filtros, consultas, evidencias y conclusiones de manera que otra persona pueda comprender y repetir el análisis.

- **Las limitaciones también deben documentarse.** Si una evidencia no permite confirmar una hipótesis, prefiero señalar esa limitación antes que presentar una conclusión que los datos disponibles no permiten demostrar.

- **La documentación es parte del trabajo defensivo.** Una buena investigación debe permitir que otro analista comprenda rápidamente qué ocurrió, qué evidencia existe, cuál es el nivel de riesgo y qué acciones podrían realizarse a continuación.

Este repositorio representa mi proceso de aprendizaje y evolución técnica. Por ello, algunos proyectos son ejercicios iniciales y otros representan investigaciones más elaboradas. Mi intención es continuar revisándolos, mejorándolos y reemplazando progresivamente aproximaciones simples por detecciones y metodologías más robustas.


---
📫 **Contacto:** [LinkedIn](https://linkedin.com/in/hugo-bustos-fuentes) 
