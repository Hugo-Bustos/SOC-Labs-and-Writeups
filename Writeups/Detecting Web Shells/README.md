# TryHackMe Writeup: Detecting Web Shells

![TryHackMe](https://img.shields.io/badge/TryHackMe-Detecting_Web_Shells-red?style=for-the-badge&logo=tryhackme)
![Category](https://img.shields.io/badge/Categoría-Incident_Response-blue?style=for-the-badge)
![OS](https://img.shields.io/badge/OS-Linux-black?style=for-the-badge&logo=linux)
![Tools](https://img.shields.io/badge/Herramientas-Bash%20|%20CLI-blueviolet?style=for-the-badge&logo=gnu-bash)
![Status](https://img.shields.io/badge/Estado-Completado-success?style=for-the-badge)

Bienvenidos a mi repositorio. Este proyecto documenta la resolución práctica de la sala [Detecting Web Shells](https://tryhackme.com/room/detectingwebshells) de TryHackMe. 

El objetivo de este laboratorio es demostrar habilidades aplicadas en Respuesta a Incidentes (Incident Response) y Análisis Forense de Servidores, rastreando las huellas de un atacante desde el reconocimiento inicial hasta la recuperación del artefacto malicioso.

##  Objetivos de Aprendizaje y Habilidades Demostradas
*   **Análisis de Logs (Web Server):** Inspección y correlación de eventos en registros de acceso de Apache (`access.log`).
*   **Threat Hunting en CLI:** Uso avanzado de utilidades nativas de Linux (`grep`, `awk`, `sort`, `uniq`, `find`) para el filtrado rápido de datos.
*   **Identificación de IoCs:** Extracción de Indicadores de Compromiso (IPs hostiles, User-Agents anómalos, cargas útiles).
*   **Análisis de Código Estático:** Localización e inspección de scripts PHP ofuscados en sistemas de archivos locales.

##  Entorno y Herramientas
*   **Sistema Operativo:** Ubuntu Linux
*   **Servicio Analizado:** Servidor Web Apache (alojando un CMS WordPress)
*   **Directorio de Trabajo:** `/var/log/apache2/` y `/var/www/html/`

---

## Resolución Paso a Paso (Incident Timeline)

### Fase 1: Reconocimiento y Descubrimiento
El primer paso en la investigación fue analizar los registros del servidor web en busca de patrones anómalos. Los atacantes suelen utilizar herramientas automatizadas para escanear directorios, lo que genera una gran cantidad de errores `404 Not Found`. 
Filtrando el archivo `access.log` para aislar estos errores, pude identificar la dirección IP del atacante y las rutas que intentaba descubrir:

```bash
cat /var/log/apache2/access.log | grep "404"
```
IP del Atacante: 203.0.113.66

User-Agent Anómalo: El atacante utilizó una herramienta automatizada identificada como ashadyagent/1.1.
Vector de entrada: Tras múltiples intentos fallidos, el atacante logró identificar un directorio válido donde enfocar su ataque: /wordpress.

### Fase 2: Acceso Inicial y Entrega del Payload

Sabiendo que el atacante descubrió el directorio /wordpress, el siguiente paso fue determinar cómo logró vulnerar el sistema. Para subir una Web Shell, el atacante debe enviar datos al servidor utilizando una petición HTTP POST.
Filtré los registros buscando exclusivamente la IP del atacante y el método POST para encontrar el momento de la inyección:

```bash
grep "203.0.113.66" /var/log/apache2/access.log | grep "POST"
```
Archivo malicioso inyectado: Se confirmó la subida de un archivo llamado upload_form.php.

### Fase 3: Ejecución y Post-Explotación

Con la Web Shell ya plantada, el atacante comenzó a interactuar con el servidor enviando comandos del sistema a través de la URL (Query Strings) mediante peticiones GET.
Rastreando las peticiones hacia el archivo malicioso recién descubierto, pude observar los comandos exactos que ejecutó:

```bash
grep "203.0.113.66" /var/log/apache2/access.log | grep "cmd=" | head -n 5
```
Comando inicial: ?cmd=whoami (Un reconocimiento básico para verificar sus privilegios en el servidor).
Escalada de Privilegios: Posteriormente, el atacante usó su acceso para obligar al servidor a descargar un script externo de enumeración llamado linpeas.sh.

### Fase 4: Recuperación del Artefacto (Análisis Estático)

Para finalizar la investigación, pasé del análisis de red al sistema de archivos local. Navegando por el directorio web y utilizando el comando find, localicé la Web Shell inyectada.
Al leer su código fuente, confirmé la estructura del malware y recuperé el flag del laboratorio oculto en los comentarios del código PHP.

```bash
# Búsqueda del archivo
find /var/www/html/ -type f -name "upload_form.php"

# Inspección del código fuente
cat /var/www/html/wordpress/.../upload_form.php
```
```
Flag Capturada: THM{W3b_Sh3ll_Int3rnals}
```

#### Conclusiones y Mitigación

La investigación confirmó una vulneración crítica por subida de archivos inseguros. Para mitigar este vector de ataque en un entorno real, se aplicarían los siguientes controles:

* Validación Estricta de Entradas (Input Validation): Implementar controles rigurosos en los formularios de subida, verificando el tipo MIME real y el contenido para bloquear ejecutables encubiertos.

* Principio de Menor Privilegio: Configurar carpetas de subida (ej. wp-content/uploads/) sin permisos de ejecución para que el servidor web no procese scripts maliciosos.

* Monitoreo de IoCs: Implementar reglas en el SIEM para alertar sobre picos inusuales de errores 404 (fuerza bruta de directorios) y la presencia de variables sospechosas como ?cmd= o ?exec= en las URLs.

```
 |\_/|    
 (. .)
  =w= (\  
 / ^ \//  Atte Hev.
(|| ||)
,""_""_ .
```

