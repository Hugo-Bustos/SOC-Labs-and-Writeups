# Writeup: Detecting Web DDoS (TryHackMe)

![TryHackMe](https://img.shields.io/badge/Platform-TryHackMe-red?style=flat-square&logo=tryhackme)
![Blue Team](https://img.shields.io/badge/Category-Blue_Team-blue?style=flat-square&logo=shield)
![Security+](https://img.shields.io/badge/Certification-CompTIA_Security+-ff0000?style=flat-square&logo=comptia)
![Splunk](https://img.shields.io/badge/Tool-Splunk-black?style=flat-square&logo=splunk)
![SIEM](https://img.shields.io/badge/Skill-SIEM_Analysis-005571?style=flat-square)
![Linux](https://img.shields.io/badge/Tool-Bash_CLI-yellow?style=flat-square&logo=linux)
![Web Security](https://img.shields.io/badge/Topic-Web_DDoS_Defense-darkgreen?style=flat-square)

Este ejercicio de Blue Team se centra en la detección y análisis de un ataque DDoS (Distributed Denial-of-Service) de Capa 7 (Aplicación). 
![Modelo OSI](https://i.ibb.co/6803766a-b286-44c1-8451-b844caec1c33/image_3.png)

A diferencia de los ataques volumétricos tradicionales de red, los ataques de Capa 7 buscan agotar los recursos del servidor apuntando a endpoints que requieren un alto procesamiento de base de datos (como /login o /search).

El objetivo de este writeup es documentar el proceso de triaje, pasando desde el análisis manual de logs crudos en la terminal de Linux hasta la investigación avanzada utilizando Splunk (SIEM), culminando con estrategias de mitigación.
