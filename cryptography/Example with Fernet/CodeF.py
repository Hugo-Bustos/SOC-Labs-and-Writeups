from cryptography.fernet import Fernet

clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

print(f"Tu clave secreta generada es: {clave.decode('utf-8')}\n")
#Aqui abajo escribimos el mensaje que queremos cifrar
mensaje_original = input("Escribe lo que deseas cifrar:  ")
print ("\n Procesando...\n")

mensaje_en_bytes = mensaje_original.encode('utf-8')
mensaje_cifrado = cipher_suite.encrypt(mensaje_en_bytes)

print("--- MENSAJE CIFRADO ---")
print(mensaje_cifrado.decode('utf-8')) 
print("-------------------------\n")

mensaje_descifrado_bytes = cipher_suite.decrypt(mensaje_cifrado)
mensaje_final = mensaje_descifrado_bytes.decode('utf-8')

print("--- MENSAJE DESCIFRADO ---")
print(mensaje_final)
print("-------------------------")

#Señalar que al ejecutar el código en nuestra terminal nos arrojará, la clave secreta en base 64 correspondiente que necesita la otra persona para desencriptar nuestro mensaje secreto.
#Aparecerá el mensaje en su código cifrado y descifrado. 
