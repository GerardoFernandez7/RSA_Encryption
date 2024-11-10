import random
import math

# Función para verificar si un número es primo
def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Función para generar un número primo aleatorio en un rango dado
def generar_primo(rango_inferior, rango_superior):
    while True:
        num = random.randint(rango_inferior, rango_superior)
        if es_primo(num):
            return num

# Función para calcular el MCD de dos números utilizando el algoritmo de Euclides
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)

# Función para calcular el inverso modular utilizando el algoritmo extendido de Euclides
def inverso_modular(e, phi_n):
    t, new_t = 0, 1
    r, new_r = phi_n, e
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return None  # No existe inverso modular
    if t < 0:
        t = t + phi_n
    return t

# Función para generar las llaves pública y privada de RSA
def generar_llaves(rango_inferior, rango_superior):
    p = generar_primo(rango_inferior, rango_superior)
    q = generar_primo(rango_inferior, rango_superior)
    while q == p:  # Asegurar que p y q sean diferentes
        q = generar_primo(rango_inferior, rango_superior)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Seleccionar un 'e' que sea coprimo con phi_n
    e = random.randint(2, phi_n - 1)
    while mcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = inverso_modular(e, phi_n)
    if d is None:
        return None  # Error en generación del inverso modular

    clave_publica = (e, n)
    clave_privada = (d, n)
    return clave_publica, clave_privada

# Función para encriptar un número usando la clave pública
def encriptar(numero, clave_publica):
    e, n = clave_publica
    numero_encriptado = pow(numero, e, n)
    return numero_encriptado

# Función para desencriptar un número encriptado usando la clave privada
def desencriptar(numero_encriptado, clave_privada):
    d, n = clave_privada
    numero_desencriptado = pow(numero_encriptado, d, n)
    return numero_desencriptado

# Ejemplo de uso con entrada de usuario
if __name__ == "__main__":
    rango_inferior = 50
    rango_superior = 100

    # Generación de claves
    resultado = generar_llaves(rango_inferior, rango_superior)
    if resultado:
        clave_publica, clave_privada = resultado
        print("Clave Pública:", clave_publica)
        print("Clave Privada:", clave_privada)

        # Solicitar al usuario que ingrese un número para encriptar
        try:
            numero = int(input("Introduce un número para encriptar: "))
            # Encriptar número
            numero_encriptado = encriptar(numero, clave_publica)
            print("Número encriptado:", numero_encriptado)

            # Desencriptar número
            numero_desencriptado = desencriptar(numero_encriptado, clave_privada)
            print("Número desencriptado:", numero_desencriptado)

        except ValueError:
            print("Por favor, introduce un número válido.")
    else:
        print("Error en la generación de claves.")