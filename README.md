# Análisis de Red y Detección de Ataques MITM (Man-in-the-Middle)

![Badge Ciberseguridad](https://img.shields.io/badge/Ciberseguridad-Blue?style=for-the-badge)
![Badge Wireshark](https://img.shields.io/badge/Wireshark-Blue?style=for-the-badge)
![Badge TryHackMe](https://img.shields.io/badge/TryHackMe-Lab-Red?style=for-the-badge)

*Nota: Este análisis fue realizado en un entorno de laboratorio controlado. Las técnicas documentadas tienen fines estrictamente educativos y de investigación defensiva.*

## Resumen del Escenario
Como parte de la investigación de una alerta de monitoreo de red en "Acme Corp", asumí el rol de Analista SOC para investigar un posible ataque Man-in-the-Middle (MITM) dentro de la LAN corporativa. 

A través del análisis de capturas de paquetes (`.pcap`) utilizando **Wireshark**, logré identificar y documentar una cadena de ataque completa que involucró tres fases:
1. **ARP Spoofing:** Intercepción del tráfico de la red.
2. **DNS Spoofing:** Redirección de resoluciones de dominio.
3. **SSL Stripping:** Degradación de cifrado para el robo de credenciales.

---

## Herramientas y Habilidades Demostradas
* **Análisis de Tráfico de Red:** Inspección profunda de paquetes (DPI) y lectura de archivos `.pcap`.
* **Manejo de Wireshark:** Creación de filtros avanzados para aislar tráfico malicioso entre el ruido de la red.
* **Troubleshooting de Redes:** Comprensión práctica de los protocolos ARP, DNS, HTTP y TLS/SSL.
* **Respuesta a Incidentes:** Trazabilidad de un ataque basándose en la *Cyber Kill Chain*.

---

## Resolución Paso a Paso

### Fase 1: Detectando el Envenenamiento ARP (Intercepción)
El atacante aprovecha la falta de autenticación del protocolo ARP para suplantar a la puerta de enlace predeterminada (`192.168.10.1`). Para aislar al atacante y excluir la dirección MAC legítima del router (`02:aa:bb:cc:00:01`), utilicé el siguiente filtro:

```
arp.opcode == 2 && arp.src.proto_ipv4 == 192.168.10.1 && eth.src != 02:aa:bb:cc:00:01
```
**Hallazgos:**
El filtro expuso una inundación de respuestas ARP gratuitas provenientes de la dirección MAC 02:fe:fe:fe:55:55. Wireshark detectó explícitamente un conflicto de IP duplicada, confirmando el ARP Spoofing.

### Fase 2: Rastreando la Redirección DNS (DNS Spoofing)

Con el atacante posicionado en la red, procedí a auditar las consultas hacia el portal corporativo (corp-login.acme-corp.local). Apliqué un filtro para buscar resoluciones DNS que provinieran de una fuente no autorizada (distinta al servidor 8.8.8.8):

```
dns.flags.response == 1 && ip.src != 8.8.8.8 && dns.qry.name == "corp-login.acme-corp.local"
```
**Hallazgos:**
Se detectó una respuesta DNS falsificada enviada por la IP del atacante (192.168.10.55). La víctima, al intentar acceder al portal legítimo, fue redirigida al servidor del atacante.
### Fase 3: Evidencia de SSL Stripping y Robo de Credenciales

Para verificar la degradación del cifrado de la conexión, filtré el tráfico web buscando el envío del formulario de inicio de sesión (método POST) hacia el dominio corporativo:

```
http.request.method == "POST" && http.host == "corp-login.acme-corp.local"
```

**Hallazgos:**
La conexión carecía de handshakes TLS. Al inspeccionar el paquete HTTP POST interceptado por el atacante, los parámetros application/x-www-form-urlencoded mostraron el usuario y la contraseña de la víctima expuestos en texto plano, confirmando el compromiso total.

## Conclusiones y Medidas de Mitigación

Este incidente subraya el riesgo de la confianza implícita en las redes de área local. Para prevenir estas brechas, se recomiendan las siguientes configuraciones de endurecimiento:

    Contra ARP Spoofing: Habilitar Dynamic ARP Inspection (DAI) y Port Security en los switches corporativos para descartar mapeos IP-MAC inválidos.

    Contra DNS Spoofing: Implementar DNSSEC para requerir firmas criptográficas en los registros DNS.

    Contra SSL Stripping: Configurar HSTS (HTTP Strict Transport Security) en todos los servidores web, forzando a los navegadores a rechazar conexiones HTTP no cifradas.

```
 |\_/|    
 (. .)
  =w= (\  
 / ^ \//  Atte Hev.
(|| ||)
,""_""_ .
```

