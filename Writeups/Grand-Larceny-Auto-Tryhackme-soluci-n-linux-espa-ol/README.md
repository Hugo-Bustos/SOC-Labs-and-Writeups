# Grand-Larceny-Auto-Tryhackme-soluci-n-linux-espa-ol

![TryHackMe](https://img.shields.io/badge/TryHackMe-Room-Red?style=for-the-badge)
![Reverse Engineering](https://img.shields.io/badge/Reverse_Engineering-Purple?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![.NET SDK](https://img.shields.io/badge/.NET_8.0-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)
![C#](https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=c-sharp&logoColor=white)

Este repositorio contiene el análisis técnico y la resolución paso a paso para la sala "Grand Larceny Auto" en TryHackMe.

A diferencia del enfoque convencional que sugiere utilizar un entorno Windows para ejecutar el juego, esta solución se aborda desde Linux realizando análisis estático sobre el código compilado e interactuando con él mediante Reflection.

Resumen del desafío

    Categoría: Reverse Engineering / .NET Logic Flaw

    Dificultad: Fácil / Intermedia

    Objetivo: Abrir la bóveda del refugio (safehouse vault) | CTF


# 1. Inspección Inicial de Archivos

Al descargar y extraer el archivo comprimido del reto (GrandLarcenyAuto.zip), encontramos la estructura típica de un proyecto compilado con el motor Godot:

    GrandLarcenyAuto.exe y GrandLarcenyAuto.pck

    data_GrandLarcenyAuto_windows_x86_64/

        GodotSharp.dll

        GrandLarcenyAuto.dll

Insight Técnico:

La presencia de GodotSharp.dll junto a GrandLarcenyAuto.dll nos indica que el motor utiliza el runtime de .NET (C#) en lugar de scripts interpretados en GDScript. Toda la lógica del jugador, reglas de negocio y mecánicas de la bóveda residen en GrandLarcenyAuto.dll.

# 2. Análisis Técnico: El Logic Flaw

Al inspeccionar el ensamblado GrandLarcenyAuto.dll con un descompilador de .NET, la atención se centra en la clase SafehouseVault y su método TryOpen().

El flujo simplificado de dicho método es el siguiente:

```
public string TryOpen() 
{
    // 1. Validación del nivel de búsqueda
    if (player.WantedStars < 6) 
    {
        return "The vault stays shut... You need SIX stars. Good luck.";
    }

    // 2. Derivación de la clave de cifrado
    byte[] key = CryptoUtil.DeriveKey("stars=" + player.WantedStars);
    
    // 3. Desencriptación del mensaje
    byte[] plain = CryptoUtil.Xor(SealedBlob, key);
    return "VAULT UNSEALED\n" + Encoding.UTF8.GetString(plain);
}
```

# 3. El por qué  de la vulnerabilidad

Existe una desalineación entre la validación de entrada y la generación de la clave criptográfica:

    La condición (< 6): Acepta cualquier valor de WantedStars que sea 6 o superior (WantedStars >= 6).

    La clave de cifrado: Se genera dinámicamente según la cadena "stars=" + player.WantedStars.

El contenido de la bóveda (SealedBlob) fue cifrado originalmente con la clave derivada de stars=6. Esto genera el siguiente comportamiento:

    Con < 6 estrellas: La bóveda no se abre (retorna el mensaje de advertencia).

    Con > 6 estrellas (ej. 7 u 8): Pasa la validación inicial, pero genera una clave errónea (ej. stars=7), corrompiendo la desencriptación.

    Con EXACTAMENTE 6 estrellas (WantedStars = 6): Cumple la condición y deriva la clave correcta que revela la bandera.

# 4. Explotación en Linux

Para resolver el desafío en Linux sin emuladores (como Wine), utilizamos el SDK de .NET (en caso que no tengas el comando de instalación en debian/ubuntu es: sudo apt update && sudo apt install -y dotnet-sdk-8.0) para cargar la DLL del juego en memoria y forzar la variable del jugador.

Paso 1: Configurar el proyecto

Creación de la aplicación de consola e importación de librerías:

```
# Crear un proyecto de consola en C#
dotnet new console -o runner

# Copiar los ensamblados del juego al proyecto
cp data_GrandLarcenyAuto_windows_x86_64/GrandLarcenyAuto.dll runner/
cp data_GrandLarcenyAuto_windows_x86_64/GodotSharp.dll runner/

cd runner

```
Paso 2: Código del Exploit (Program.cs)

Reemplazamos el archivo Program.cs con el siguiente script que utiliza System.Reflection para instanciar las clases, asignar WantedStars = 6 e invocar el método de apertura:

C#

using System;
using System.Reflection;

class Program 
{
    static void Main() 
    {
        // 1. Cargar el ensamblado .NET del juego
        var asm = Assembly.LoadFrom("GrandLarcenyAuto.dll");
        
        // 2. Obtener las referencias de las clases
        var playerStateType = asm.GetType("GrandLarcenyAuto.PlayerState")!;
        var vaultType = asm.GetType("GrandLarcenyAuto.SafehouseVault")!;
        
        // 3. Instanciar el estado del jugador y forzar las 6 estrellas
        var player = Activator.CreateInstance(playerStateType)!;
        var wantedStarsProp = playerStateType.GetProperty("WantedStars")!;
        wantedStarsProp.SetValue(player, 6);

        // 4. Instanciar la bóveda e invocar el método TryOpen()
        var vault = Activator.CreateInstance(vaultType, player)!;
        var result = vaultType.GetMethod("TryOpen")!.Invoke(vault, null);

        // 5. Imprimir el resultado desencriptado
        Console.WriteLine("\n[+] Resultado Obtenido:");
        Console.WriteLine(result);
    }
}

Paso 3: Ejecución

Ejecutamos en nuestra terminal: 
dotnet run

Paso 4: Lectura de la flag. 
THM{h0tf1x3d_my_0wn_w4nt3d_l3v3l}

# 5. Conclusiones:
Este desafío es un gran ejemplo de cómo los errores de lógica de negocio pueden comprometer una aplicación aunque se utilicen algoritmos de cifrado seguros. Asimismo, demuestra la flexibilidad del ecosistema .NET en Linux, permitiendo auditar y manipular ensamblados compilados para Windows sin depender del sistema operativo original. A nivel personal encontré interesante el reto porque me permitió extender mi conocimiento del reverse engineering del cual todavía estoy aprendiendo, éxito a todos en sus proyectos y/o desafíos.

```
 |\_/|    
 (. .)
  =w= (\  
 / ^ \//  Atte Hev.
(|| ||)
,""_""_ .
```
