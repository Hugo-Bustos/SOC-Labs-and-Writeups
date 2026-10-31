# TryHackMe Writeup: Investigación y Detección de una Web Shell

![TryHackMe](https://img.shields.io/badge/TryHackMe-Detecting_Web_Shells-red?style=for-the-badge&logo=tryhackme)
![Category](https://img.shields.io/badge/Categoría-Incident_Response-blue?style=for-the-badge)
![OS](https://img.shields.io/badge/OS-Linux-black?style=for-the-badge&logo=linux)
![Tools](https://img.shields.io/badge/Herramientas-Bash%20%7C%20CLI-blueviolet?style=for-the-badge&logo=gnu-bash)
![Status](https://img.shields.io/badge/Estado-Completado-success?style=for-the-badge)

Este proyecto documenta la resolución práctica de la sala [Detecting Web Shells](https://tryhackme.com/room/detectingwebshells) de TryHackMe.

El objetivo es investigar un servidor web Linux a partir de registros de Apache y artefactos del sistema, reconstruyendo la actividad del atacante desde el reconocimiento inicial hasta la identificación y recuperación del archivo utilizado como Web Shell.

## Objetivos de la investigación

- Analizar logs de Apache y detectar patrones anómalos.
- Reconstruir una secuencia temporal de actividad.
- Identificar indicadores de compromiso (IP, User-Agent, rutas y artefactos).
- Determinar el vector de entrega de la Web Shell.
- Confirmar la presencia del artefacto mediante análisis del sistema de archivos.
- Diferenciar entre acceso, ejecución y escalada de privilegios según la evidencia disponible.
- Proponer controles defensivos y oportunidades de detección.

## Entorno y herramientas

- **Sistema Operativo:** Ubuntu Linux
- **Servicio Analizado:** Apache / WordPress
- **Logs:** `/var/log/apache2/access.log`
- **Directorio web:** `/var/www/html/`
- **Herramientas:** Bash, grep, awk, sort, uniq, find

---

# Resumen del incidente

El análisis permitió identificar actividad procedente de la IP `203.0.113.66`, asociada a un User-Agent inusual (`ashadyagent/1.1`). La actividad comenzó con solicitudes que generaron múltiples respuestas `404`, compatibles con reconocimiento automatizado de rutas.

Posteriormente se observó actividad sobre `/wordpress` y una petición `POST` asociada a la subida de `upload_form.php`. Las solicitudes posteriores hacia este archivo incluyeron el parámetro `cmd`, proporcionando evidencia de interacción con una Web Shell.

Finalmente, la inspección del sistema de archivos permitió localizar el artefacto y analizar su código PHP.

> **Conclusión principal:** la evidencia del laboratorio permite confirmar la presencia y utilización de una Web Shell. La descarga de herramientas posteriores, como `linpeas.sh`, demuestra actividad de post-explotación/enumeración, pero **no constituye por sí sola evidencia de una escalada de privilegios exitosa**.

---

# Timeline de la actividad

| Etapa | Evidencia | Interpretación |
|---|---|---|
| Reconocimiento | Múltiples `404` | Enumeración de rutas/directorios |
| Identificación del objetivo | `/wordpress` | El atacante encontró una ruta válida de interés |
| Entrega | `POST` asociado a `upload_form.php` | Actividad compatible con subida del artefacto |
| Ejecución/interacción | `GET` con `cmd=` | Uso de la Web Shell para enviar comandos |
| Post-explotación | Descarga de `linpeas.sh` | Enumeración del sistema |
| Recuperación | `upload_form.php` en `/var/www/html/` | Identificación del artefacto malicioso |

---

# Fase 1 — Reconocimiento y descubrimiento

El primer objetivo fue identificar patrones de reconocimiento en el `access.log`. Una gran cantidad de respuestas `404` puede aparecer cuando una herramienta automatizada intenta descubrir rutas que no existen.

```bash
grep "404" /var/log/apache2/access.log
```

**Indicadores observados:**

- **IP:** `203.0.113.66`
- **User-Agent:** `ashadyagent/1.1`
- **Ruta de interés:** `/wordpress`

La presencia de múltiples solicitudes fallidas y un User-Agent poco habitual constituye una señal útil para el triage, aunque ninguno de estos indicadores debería considerarse malicioso de forma aislada.

### Consideración SOC

En un entorno real convendría correlacionar:

- cantidad de `404` por IP;
- ventana temporal;
- rutas solicitadas;
- User-Agent;
- distribución de métodos HTTP;
- comportamiento posterior de la misma IP.

---

# Fase 2 — Entrega del artefacto

Una vez identificada la ruta `/wordpress`, se investigó si la IP había realizado peticiones `POST` relacionadas con la entrega de contenido.

```bash
grep "203.0.113.66" /var/log/apache2/access.log | grep "POST"
```

El análisis permitió identificar actividad asociada a:

```text
upload_form.php
```

La petición `POST` constituye evidencia relevante de una posible operación de subida. La confirmación del artefacto se realizó posteriormente mediante la inspección del sistema de archivos.

> **Importante:** una petición `POST` no demuestra por sí sola que un archivo haya sido almacenado o ejecutado. En este laboratorio, la evidencia del log se correlaciona posteriormente con la presencia de `upload_form.php` en el servidor.

---

# Fase 3 — Interacción con la Web Shell

Con el artefacto identificado, se analizaron las peticiones posteriores de la misma IP buscando parámetros asociados a ejecución de comandos.

```bash
grep "203.0.113.66" /var/log/apache2/access.log | grep "cmd=" | head -n 5
```

Se observó la siguiente actividad:

```text
?cmd=whoami
```

El comando `whoami` permite determinar el contexto de usuario bajo el cual se ejecuta la operación. En este escenario constituye una señal clara de interacción con una interfaz que permite ejecutar comandos del sistema.

Posteriormente se observó la utilización de `linpeas.sh` para realizar enumeración del sistema.

### Distinción entre post-explotación y escalada de privilegios

La descarga o ejecución de una herramienta de enumeración como `linpeas.sh` **no demuestra por sí misma una escalada de privilegios exitosa**.

Para afirmar una escalada sería necesario observar evidencia adicional, por ejemplo:

- cambio efectivo de usuario;
- ejecución de comandos con privilegios superiores;
- abuso de `sudo`, SUID u otro mecanismo de elevación;
- creación/modificación de cuentas privilegiadas;
- evidencia de acceso a recursos que anteriormente no estaban disponibles.

Por ello, en este laboratorio se clasifica esta fase como **post-explotación y enumeración**.

---

# Fase 4 — Recuperación y análisis del artefacto

La investigación pasó posteriormente del análisis de logs a la inspección del sistema de archivos.

```bash
find /var/www/html/ -type f -name "upload_form.php"
```

Una vez localizado el archivo, se inspeccionó su contenido:

```bash
cat /var/www/html/wordpress/.../upload_form.php
```

El análisis del código PHP permitió confirmar la funcionalidad asociada a la Web Shell y recuperar el indicador del laboratorio:

```text
THM{W3b_Sh3ll_Int3rnals}
```

### Valor forense del artefacto

El archivo encontrado constituye un artefacto especialmente relevante porque permite relacionar:

1. la actividad observada en `access.log`;
2. la petición `POST` asociada a su entrega;
3. las solicitudes posteriores con `cmd=`;
4. el contenido almacenado en el servidor.

Esta correlación aumenta significativamente la confianza de la conclusión frente a analizar únicamente una señal aislada.

---

# Indicadores y artefactos

| Tipo | Valor | Relevancia |
|---|---|---|
| IP | `203.0.113.66` | Fuente de la actividad observada |
| User-Agent | `ashadyagent/1.1` | Indicador de automatización potencial |
| Ruta | `/wordpress` | Recurso identificado durante reconocimiento |
| Archivo | `upload_form.php` | Web Shell identificada |
| Parámetro | `cmd=` | Indicador de interacción con comandos |
| Herramienta | `linpeas.sh` | Enumeración post-explotación |

> Los indicadores anteriores deben considerarse dentro del contexto del laboratorio. Una IP, User-Agent o parámetro aislado no constituye necesariamente evidencia de compromiso.

---

# Evaluación SOC

| Campo | Evaluación |
|---|---|
| **Tipo de incidente** | Compromiso de aplicación web / Web Shell |
| **Vector observado** | Subida de archivo mediante aplicación web |
| **Ejecución** | Interacción posterior mediante `cmd=` |
| **Post-explotación** | Enumeración mediante `linpeas.sh` |
| **Persistencia** | No demostrada con la evidencia presentada |
| **Escalada de privilegios** | No confirmada |
| **Impacto** | Ejecución remota de comandos en el servidor web |
| **Severidad** | Alta |
| **Confianza** | Alta para la presencia y utilización de la Web Shell |

---

# Respuesta y remediación

### 1. Contención

- Aislar el servidor afectado si el contexto operacional lo permite.
- Preservar logs y artefactos antes de realizar cambios destructivos.
- Bloquear temporalmente indicadores asociados mientras se determina el alcance.

### 2. Erradicación

- Eliminar la Web Shell y cualquier artefacto asociado después de preservar la evidencia necesaria.
- Revisar otros archivos modificados recientemente dentro del directorio web.
- Investigar cuentas, procesos y conexiones creados durante el periodo del incidente.
- Revisar plugins, temas y componentes de WordPress relacionados con el vector de entrada.

### 3. Prevención

- Validar estrictamente archivos subidos por usuarios.
- Verificar tipo MIME y contenido real del archivo, no solamente su extensión.
- Impedir la ejecución de scripts en directorios destinados exclusivamente a uploads.
- Aplicar el principio de menor privilegio al usuario del servidor web.
- Mantener WordPress, plugins y componentes actualizados.

### 4. Detección

El incidente también permite derivar posibles casos de uso para un SIEM o sistema de detección:

- múltiples `404` desde una misma IP dentro de una ventana temporal;
- `POST` hacia endpoints de subida de archivos;
- creación de archivos `.php` en directorios donde normalmente no deberían existir;
- solicitudes hacia archivos recién creados;
- parámetros como `cmd=`, `exec=` u otros patrones asociados a interfaces de ejecución;
- ejecución de intérpretes o herramientas de sistema por parte del proceso del servidor web;
- descarga de herramientas de enumeración desde un proceso asociado a Apache/PHP.

> Los umbrales deben calibrarse con el comportamiento normal de la aplicación para reducir falsos positivos.

---

# Conclusiones y aprendizajes

Este laboratorio demuestra un flujo de investigación aplicable a un SOC: comenzar con señales de reconocimiento, reducir el espacio de búsqueda mediante logs, correlacionar actividad de red con artefactos del sistema y finalmente determinar si existe evidencia suficiente para confirmar una Web Shell.

La principal lección es que **una investigación sólida no depende de un único indicador**. La combinación de IP, User-Agent, rutas, método HTTP, archivo almacenado y solicitudes posteriores proporciona una narrativa técnica mucho más fiable.

También es importante diferenciar entre lo observado y lo inferido. La evidencia permite confirmar la presencia y utilización de la Web Shell, pero no permite afirmar automáticamente persistencia, escalada de privilegios o compromiso completo del servidor sin evidencia adicional.

Desde una perspectiva SOC, este caso refuerza la importancia de:

- correlacionar eventos antes de emitir conclusiones;
- distinguir acceso, ejecución, persistencia y escalada de privilegios;
- preservar evidencia antes de realizar acciones de contención destructivas;
- convertir los indicadores observados en oportunidades de detección;
- documentar las limitaciones de la investigación.

Este laboratorio forma parte de mi formación práctica en Incident Response, análisis de logs y Threat Hunting sobre sistemas Linux.
