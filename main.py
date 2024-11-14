import random
import math

# José Gerardo Ruiz García - 23719
# Gerardo André Fernández Cruz - 23763
# Andrés Alberto Mazariegos Escobar - 21749

# FLUJO DEL PROGRAMA
# 1. Genera claves pública y privada (RSA).
# 2. Muestra las claves al usuario.
# 3. Solicita un número para encriptar y lo muestra encriptado.
# 4. Pide al usuario ingresar el número encriptado y la clave privada.
# 5. Desencripta el número si la clave privada es correcta, mostrando el resultado o un mensaje de error si es incorrecta.

# Función para verificar si un número es primo.
def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Función para generar un número primo aleatorio en un rango dado.
def generar_primo(rango_inferior, rango_superior):
    if rango_inferior < 2 or rango_inferior >= rango_superior:
        print("Rango inválido para generar número primo.")
        return None

    while True:
        num = random.randint(rango_inferior, rango_superior)
        if es_primo(num):
            return num
        if rango_superior - rango_inferior < 10:
            print("No se encontró un número primo en el rango especificado.")
            return None

# Función para calcular el MCD de dos números utilizando el algoritmo de Euclides
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)

# Función para calcular el inverso modular utilizando el algoritmo extendido de Euclides
# Donde quiero encontrar el inverso de e en modulo phi_n
def inverso_modular(e, phi_n):
    t, new_t = 0, 1
    r, new_r = phi_n, e
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return None
    if t < 0:
        t += phi_n
    return t

# Función para generar las llaves pública y privada de RSA
def generar_llaves(rango_inferior, rango_superior):
    p = generar_primo(rango_inferior, rango_superior)
    q = generar_primo(rango_inferior, rango_superior)
    if not p or not q:
        print("No se pudieron generar dos números primos distintos.")
        return None

    while q == p:
        q = generar_primo(rango_inferior, rango_superior)
        if q is None:
            print("Error: no se pudo encontrar un número primo diferente a p.")
            return None

    # Se multiplica p y q para saber en que mod se encriptará y se desencriptará
    n = p * q
    # Totiente de euler
    phi_n = (p - 1) * (q - 1)
    # Cálculo de e para la llave publica
    e = random.randint(2, phi_n - 1)

    while mcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    # Cálculo de d para la llave privada
    d = inverso_modular(e, phi_n)

    if d is None:
        print("Error al calcular el inverso modular; no se pudo generar las llaves.")
        return None

    # Creación de tuplas de las claves
    clave_publica = (e, n)
    clave_privada = (d, n)
    return clave_publica, clave_privada

# Función para encriptar un carácter o número usando la clave pública
def encriptar_caracter(caracter, clave_publica):
    e, n = clave_publica
    ascii_val = ord(caracter)
    return pow(ascii_val, e, n)

# Función para desencriptar un carácter encriptado usando la clave privada
def desencriptar_caracter(valor_encriptado, clave_privada):
    d, n = clave_privada
    ascii_val = pow(valor_encriptado, d, n)
    return chr(ascii_val)

# Función para encriptar un mensaje completo
def encriptar_mensaje(mensaje, clave_publica):
    mensaje_encriptado = [encriptar_caracter(caracter, clave_publica) for caracter in mensaje]
    return mensaje_encriptado

# Función para desencriptar un mensaje completo
def desencriptar_mensaje(mensaje_encriptado, clave_privada):
    mensaje_desencriptado = ''.join([desencriptar_caracter(caracter, clave_privada) for caracter in mensaje_encriptado])
    return mensaje_desencriptado

# Función donde el programa arranca
if __name__ == "__main__":
    # Se establece el rango de los números en los que se generán los números primos
    rango_inferior = 50
    rango_superior = 100

    resultado = generar_llaves(rango_inferior, rango_superior)
    if resultado:
        clave_publica, clave_privada = resultado
        # Se imprimen las claves publicas y privadas
        print("Clave Pública (e, n):", clave_publica)
        print("Clave Privada (d, n):", clave_privada)

        # Solicitar al usuario que ingrese el mensaje que desea encriptar
        mensaje = input("\nIntroduce un mensaje para encriptar: ")
        mensaje_encriptado = encriptar_mensaje(mensaje, clave_publica)
        print("Mensaje encriptado:", mensaje_encriptado)

        # Solicitar al usuario que ingrese el mensaje encriptado para desencriptar
        mensaje_desencriptado = desencriptar_mensaje(mensaje_encriptado, clave_privada)
        print("Mensaje desencriptado:", mensaje_desencriptado)
    else:
        print("Error en la generación de claves.")