![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Library-Cryptography-red?style=for-the-badge&logo=pypi&logoColor=white)
![Cybersecurity](https://img.shields.io/badge/Topic-Cybersecurity-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completado-success?style=for-the-badge)

# Cifrado Simétrico con Python (Fernet) 

Este es un script interactivo escrito en Python que demuestra cómo funciona la criptografía simétrica utilizando la biblioteca `cryptography`. 

El programa genera una clave secreta única, pide al usuario un mensaje por consola, lo cifra (haciéndolo ilegible) y luego lo vuelve a descifrar para demostrar el proceso completo.

## ¿Cómo funciona?

1. **Generación de llave:** Crea una clave criptográfica aleatoria de 32 bytes en formato Base64.
2. **Entrada interactiva:** Solicita al usuario el texto que desea proteger.
3. **Cifrado (AES-128-CBC):** Convierte el texto plano en un *token* cifrado e ilegible.
4. **Descifrado:** Utiliza la misma clave inicial para revertir el proceso y recuperar el texto original.

## Requisitos previos

Para ejecutar este script, necesitas tener Python instalado y la librería `cryptography`. Puedes instalarla fácilmente ejecutando este comando en tu terminal:

```bash
pip install cryptography
```
## Acceso al código en Py
[Enlace Código](<./cryptography/Example with Fernet/CodeF.py>)
