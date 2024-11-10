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

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(2, phi_n - 1)
    while mcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = inverso_modular(e, phi_n)
    if d is None:
        print("Error al calcular el inverso modular; no se pudo generar las llaves.")
        return None

    clave_publica = (e, n)
    clave_privada = (d, n)
    return clave_publica, clave_privada

# Función para encriptar un número usando la clave pública
def encriptar(numero, clave_publica):
    e, n = clave_publica
    if not isinstance(numero, int) or numero <= 0:
        print("Error: El número a encriptar debe ser un entero positivo.")
        return None
    if numero >= n:
        print("Error: El número a encriptar debe ser menor que n.")
        return None
    return pow(numero, e, n)

# Función para desencriptar un número encriptado usando la clave privada
def desencriptar(numero_encriptado, clave_privada):
    d, n = clave_privada
    if not isinstance(numero_encriptado, int) or numero_encriptado <= 0:
        print("Error: El número encriptado debe ser un entero positivo.")
        return None
    if numero_encriptado >= n:
        print("Error: El número encriptado debe ser menor que n.")
        return None
    return pow(numero_encriptado, d, n)

# Ejemplo de uso con entrada de usuario
if __name__ == "__main__":
    rango_inferior = 50
    rango_superior = 100

    resultado = generar_llaves(rango_inferior, rango_superior)
    if resultado:
        clave_publica, clave_privada = resultado
        print("Clave Pública (e, n):", clave_publica)
        print("Clave Privada (d, n):", clave_privada)

        try:
            numero = int(input("\nIntroduce un número para encriptar (debe ser menor que n): "))
            numero_encriptado = encriptar(numero, clave_publica)
            if numero_encriptado is not None:
                print("Número encriptado:", numero_encriptado)

                # Solicitar el número encriptado y clave privada para desencriptar
                numero_a_desencriptar = int(input("\nIntroduce el número encriptado para desencriptar: "))
                d_ingresado = int(input("Introduce el valor de 'd' de la clave privada: "))
                n_ingresado = int(input("Introduce el valor de 'n' de la clave privada: "))

                # Verificar si la clave privada ingresada es correcta
                if (d_ingresado, n_ingresado) == clave_privada:
                    numero_desencriptado = desencriptar(numero_a_desencriptar, clave_privada)
                    print("Número desencriptado:", numero_desencriptado)
                else:
                    print("Error: La clave privada ingresada es incorrecta.")
            else:
                print("Error: No se pudo encriptar el número.")

        except ValueError:
            print("Por favor, introduce un número válido.")
    else:
        print("Error en la generación de claves.")
