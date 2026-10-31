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

## Sobre mí
Soy estudiante de Ciberseguridad en transición hacia el área de Seguridad Defensiva, con especial interés en SOC, análisis de logs, detección de amenazas e investigación de incidentes.
Antes de iniciar mi formación en Ciberseguridad trabajé durante casi una década en educación, experiencia que me permitió desarrollar habilidades de análisis, investigación, organización y comunicación técnica.
Actualmente utilizo este repositorio para documentar mi evolución práctica mediante laboratorios de SOC, análisis de logs, tráfico de red, Threat Hunting, Detection Engineering y scripting defensivo.

## ¿Qué esperar aquí?
Este repositorio reúne laboratorios e investigaciones prácticas orientadas a SOC y Blue Team, incluyendo análisis de logs, tráfico de red, Threat Hunting, Detection Engineering, respuesta a incidentes y scripting defensivo.

El objetivo no es únicamente documentar herramientas o reproducir comandos, sino mostrar cómo se analiza una situación de seguridad a partir de evidencia, cómo se formulan y validan hipótesis y cómo se llega a una conclusión defensiva.

En los distintos proyectos intento seguir un proceso similar al utilizado en una investigación de seguridad:

Detectar → Triage → Investigar → Correlacionar → Evaluar → Decidir → Responder

Cada laboratorio representa además una etapa de mi aprendizaje, por lo que procuro documentar tanto los resultados obtenidos como las limitaciones y aspectos que podrían mejorarse.

---

##  Enfoque y Metodología
Intento abordar cada investigación desde una perspectiva orientada al trabajo de un analista SOC, priorizando la evidencia y el contexto por sobre las conclusiones apresuradas.

El proceso que utilizo como referencia es:

    Contexto: Comprender el escenario, los activos involucrados y el comportamiento esperado.

    Triage: Determinar rápidamente si la actividad merece investigación y establecer una prioridad inicial.

    Análisis: Examinar logs, tráfico de red, procesos, artefactos y otros indicadores disponibles.

    Correlación: Relacionar eventos temporalmente y entre distintas fuentes para construir una visión más completa.

    Validación: Buscar evidencia que confirme o contradiga la hipótesis inicial, considerando también posibles falsos positivos.

    Mapeo MITRE ATT&CK: Relacionar las técnicas observadas con el comportamiento del adversario cuando existe evidencia suficiente.

    Evaluación: Determinar impacto, severidad, nivel de confianza e indicadores relevantes.

    Respuesta: Proponer acciones de contención, erradicación, recuperación o prevención según el escenario.

    Documentación: Registrar evidencia, razonamiento, limitaciones y conclusiones de forma reproducible.

No todos los laboratorios permiten completar todas estas etapas. Cuando la evidencia disponible no permite confirmar una hipótesis, intento indicarlo explícitamente en lugar de presentar una conclusión como un hecho.
---

## 📂 Índice de Laboratorios

### 01. Análisis de Tráfico de Red (PCAPs & NTA)
* 🔹 **[Análisis de Red y Detección de Ataques MITM](<./Writeups/Análisis de Red y Detección de Ataques MITM (Man-in-the-Middle)>):** Inspección de tráfico no cifrado en Wireshark y extracción de credenciales expuestas en peticiones POST.

### 02. Análisis de Logs & SIEM
* 🔹 **[Análisis de logs en error 401](<./Scripts/Analizador 401.py>)**: Detection Engineering básico para logs enfocado en el error 401.
* 🔹 **[Detección de Web Shells (Incident Response)](<./Writeups/Detecting Web Shells>):** Análisis de logs de Apache utilizando herramientas CLI (grep, awk) para reconstruir la inyección y ejecución de una Web Shell maliciosa
* 🔹 **[Detección de ataque web DDoS](<./Writeups/Detecting Web DDoS (TryHackMe)>):** Análisis defensivo de un HTTP Flood distribuido contra recursos web.
* 🔹 **[Investigación de un Endpoint Windows mediante Event Logs, Sysmon y PowerShell](<./Writeups/Windows Logging for SOC>):** Este reporte documenta la investigación de un endpoint Windows comprometido mediante el análisis correlacionado de registros de seguridad nativos (Security.evtx), telemetría de Sysmon y artefactos locales de PowerShell.
* 🔹 **[Investigación de un Endpoint Linux mediante Logs Nativos y Auditd](<./Writeups/Linux Logging & Runtime Monitoring para SOC>):** Este reporte documenta la cacería de amenazas en un servidor comprometido mediante el análisis de registros tradicionales (syslog, auth.log) y el monitoreo en tiempo real de system calls usando ausearch para rastrear la ingesta y ejecución de herramientas maliciosas.

### 03. Criptografía 
* 🔹 **[Criptografía Simétrica](<./cryptography/Example with Fernet>):** Ejercicio de código que permite cifrar y descifrar mensajes usando Fernet (simétrico)
  
### 04. Investigaciones de Laboratorios
* 🔹 **[Grand Larceny Auto, LAB TRYHACKME: Reverse Engineering](<./Writeups/Grand-Larceny-Auto-Tryhackme-soluci-n-linux-espa-ol>) :** Análisis de una vulnerabilidad de lógica y explotación de una aplicación .NET mediante manipulación de estado y análisis de su implementación.

---

## Herramientas y tecnologías:

* **SIEM y análisis de seguridad:** Splunk, ELK Stack, Brim.
* **Análisis de red:** Wireshark, Tshark.
* **Windows / DFIR:** Event Viewer, Sysmon, PowerShell.
* **Linux / monitoreo:** syslog, auth.log, auditd, ausearch.
* **Scripting y automatización:** Python, Bash.
* **Frameworks y metodologías:** MITRE ATT&CK, análisis basado en evidencia e investigación orientada a incidentes.

## Principios que estoy aplicando

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
