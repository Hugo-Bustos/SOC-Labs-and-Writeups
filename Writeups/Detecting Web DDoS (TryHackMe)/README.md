# 🤖 Writeup: Detecting Web DDoS (TryHackMe) 🤖

![TryHackMe](https://img.shields.io/badge/Platform-TryHackMe-red?style=flat-square&logo=tryhackme)
![Blue Team](https://img.shields.io/badge/Category-Blue_Team-blue?style=flat-square&logo=shield)
![Security+](https://img.shields.io/badge/Certification-CompTIA_Security+-ff0000?style=flat-square&logo=comptia)
![Splunk](https://img.shields.io/badge/Tool-Splunk-black?style=flat-square&logo=splunk)
![SIEM](https://img.shields.io/badge/Skill-SIEM_Analysis-005571?style=flat-square)
![Linux](https://img.shields.io/badge/Tool-Bash_CLI-yellow?style=flat-square&logo=linux)
![Web Security](https://img.shields.io/badge/Topic-Web_DDoS_Defense-darkgreen?style=flat-square)

<img width="2400" height="1792" alt="Gemini_Generated_Image_gxfii6gxfii6gxfi" src="https://github.com/user-attachments/assets/0cf73f83-6f2a-4f36-80ae-83395ac198c1" />

A diferencia de los ataques colosales tradicionales de red, los ataques de capa(layer) 7 buscan agotar los recursos del servidor apuntando a endpoints que requieren un alto procesamiento en la base de datos
como por ejemplo (/login search)

Este writeup tiene como objetivo documentar el proceso de triaje, pasando desde el análisis manual de logs crudos en la terminal de Linux hasta la investigación avanzada utilizando Splunk (SIEM), culminando con estrategias de mitigación. 

## Fase 1: Análisis Manual de Logs (CLI)

Durante las primeras etapas del incidente, el servidor comenzó a arrojar errores HTTP 503 Service Unavailable, indicando una denegación de servicio. Para identificar rápidamente al atacante en un entorno sin SIEM, procesamos el archivo access.log nativo del servidor web utilizando herramientas de la terminal de Linux.
Identificación de la IP del Atacante

```
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 5}
```
## Comando usado y su desglose
```
awk '{print $1}': Extrae la primera columna del log (Dirección IP).

sort: Ordena las IPs numéricamente (necesario para el siguiente paso).

uniq -c: Comprime los duplicados y cuenta cuántas veces aparece cada IP.

sort -nr: Ordena el resultado de mayor a menor (-r reverse, -n numeric).

head -n 5: Muestra solo el Top 5 de agresores.
```
## Resultado 
```
Se identificó la IP principal del atacante: 203.12.23.195.
```

Para encontrar la dirección IP que estaba generando la anomalía de tráfico, ejecutamos un pipeline de filtrado:




