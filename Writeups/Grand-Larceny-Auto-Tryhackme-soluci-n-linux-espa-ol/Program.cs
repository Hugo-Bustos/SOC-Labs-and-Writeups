C#

using System;
using System.Reflection;

namespace GrandLarcenyAutoExploit
{
    class Program 
    {
        static void Main(string[] args) 
        {
            Console.WriteLine("[*] Iniciando exploit para Grand Larceny Auto (TryHackMe)...");

            try
            {
               
                string assemblyPath = "GrandLarcenyAuto.dll";
                var asm = Assembly.LoadFrom(assemblyPath);
                Console.WriteLine($"[+] Ensamblado '{assemblyPath}' cargado correctamente.");

              
                var playerStateType = asm.GetType("GrandLarcenyAuto.PlayerState");
                var vaultType = asm.GetType("GrandLarcenyAuto.SafehouseVault");

                if (playerStateType == null || vaultType == null)
                {
                    Console.WriteLine("[-] Error: No se encontraron los tipos 'PlayerState' o 'SafehouseVault' en la DLL.");
                    return;
                }

            
                var player = Activator.CreateInstance(playerStateType);
                var wantedStarsProp = playerStateType.GetProperty("WantedStars");

                if (wantedStarsProp == null || player == null)
                {
                    Console.WriteLine("[-] Error: No se pudo obtener la propiedad 'WantedStars' o instanciar el jugador.");
                    return;
                }

               
                wantedStarsProp.SetValue(player, 6);
                Console.WriteLine("[+] Variable 'WantedStars' establecida en EXACTAMENTE 6 estrellas.");

              
                var vault = Activator.CreateInstance(vaultType, player);
                var tryOpenMethod = vaultType.GetMethod("TryOpen");

                if (tryOpenMethod == null || vault == null)
                {
                    Console.WriteLine("[-] Error: No se pudo instanciar la bóveda o encontrar el método 'TryOpen'.");
                    return;
                }

              
                Console.WriteLine("[*] Invocando SafehouseVault.TryOpen()...\n");
                var result = tryOpenMethod.Invoke(vault, null);

                Console.WriteLine("================ RESULTADO OBTENIDO ================");
                Console.WriteLine(result);
                Console.WriteLine("====================================================");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[-] Ocurrió un error durante la ejecución: {ex.Message}");
            }
        }
    }
}
