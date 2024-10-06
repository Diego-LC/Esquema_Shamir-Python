import random

# Definir el valor primo p para la aritmética modular
p = 257  # Un número primo mayor que 255 (valor máximo de un byte)

# Algoritmo de Euclides extendido para encontrar el inverso modular
def euclides_extendido(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclides_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y  # El inverso modular será el valor de x

# Función para encontrar el inverso modular de a mod p
def inverso_modular(a, p):
    gcd, x, _ = euclides_extendido(a, p)
    if gcd != 1:
        raise ValueError(f"No existe inverso modular para {a} mod {p}")
    return x % p  # Asegurar que el inverso esté dentro del rango mod p

# Función para generar un polinomio con aritmética modular
def generar_polinomio(secreto, k):
    p_coef = [secreto] + [random.randint(0, p-1) for _ in range(k-1)]  # Generar coeficientes mod p

    pol_str = f"{p_coef[0]}"
    for i in range(1, len(p_coef)):
        pol_str += f" + {p_coef[i]}x"
        if i > 1:
            pol_str += f"^{i}"
    print(f"Polinomio del byte {secreto}\t: ", pol_str)  # Imprime el polinomio de forma legible

    return p_coef

# Función para evaluar el polinomio en un punto x con aritmética modular
def evaluar_polinomio(coeficientes, x):
    resultado = 0
    i = 0
    for coef in coeficientes:
        resultado = (resultado + coef * pow(x, i, p)) % p  # Evaluar con aritmética modular
        i += 1
    return resultado

# Generar las n partes del secreto
def dividir_secreto_byte(byte_secreto, n, k):
    coeficientes = generar_polinomio(byte_secreto, k)
    partes = [(i, evaluar_polinomio(coeficientes, i)) for i in range(1, n+1)]
    return partes

# Función para reconstruir el secreto usando interpolación de Lagrange en un campo finito
def reconstruir_secreto(partes, k):
    def lagrange_interpolacion(x, partes):
        suma = 0
        for i, (xi, yi) in enumerate(partes):
            producto = yi
            for j, (xj, _) in enumerate(partes):
                if i != j:
                    # Calcular el término de Lagrange usando aritmética modular
                    numerador = (x - xj) % p
                    denominador = (xi - xj) % p
                    inverso_denominador = inverso_modular(denominador, p)  # Usar inverso modular con Euclides
                    producto = (producto * numerador * inverso_denominador) % p
            suma = (suma + producto) % p
        return suma

    return lagrange_interpolacion(0, partes[:k])

# Función para dividir un texto en partes
def dividir_texto(texto, n, k):
    texto_bytes = texto.encode('utf-8')  # Convertir texto a bytes
    print("\nTexto original: ", texto,", Texto en bytes:", [byte for byte in texto_bytes], "\n")
    
    partes_totales = []
    # Generar n partes para cada byte del texto
    for byte in texto_bytes:
        partes = dividir_secreto_byte(byte, n, k) 
        partes_totales.append(partes)

    return partes_totales

# Reconstruir el texto a partir de las partes
def reconstruir_texto(partes_totales, k):
    reconstruido_bytes = bytearray()

    for partes in partes_totales:
        partes_para_reconstruir = random.sample(partes, k)
        byte_reconstruido = reconstruir_secreto(partes_para_reconstruir, k)
        reconstruido_bytes.append(byte_reconstruido)

    return reconstruido_bytes.decode('utf-8')

# Ejemplo usando input de usuario
print("Ingrese un texto de prueba:")
texto_original = input("Texto: ")
n = 5  # Número de partes
k = 3  # Número mínimo de partes necesarias

# Dividir el texto
partes_totales = dividir_texto(texto_original, n, k)
print("Partes generadas:")
for i, partes in enumerate(partes_totales):
    print(f"Byte {i+1}: {partes}")

# Simular la reconstrucción del texto usando k partes
texto_reconstruido = reconstruir_texto(partes_totales, k)
print("Texto reconstruido:", texto_reconstruido)

# Probar la resistencia a intentos de reconstrucción con menos partes
def prueba_seguridad(partes_totales, k):
    reconstruido_bytes = bytearray()

    for partes in partes_totales:
        # Intentamos reconstruir usando menos de las partes necesarias
        partes_para_reconstruir = random.sample(partes, k - 1)
        byte_reconstruido = reconstruir_secreto(partes_para_reconstruir, k)
        reconstruido_bytes.append(byte_reconstruido)

    try:
        # Intentamos decodificar los bytes como UTF-8
        return reconstruido_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Si ocurre un error, notificamos que la reconstrucción fue fallida
        print("Error: no se pudo decodificar los bytes.")
        print("Reconstrucción incorrecta: ", list(reconstruido_bytes))
        return None

print(f"\nIntento de reconstrucción con {k-1} partes:")
texto_reconstruido_incorrecto = prueba_seguridad(partes_totales, k)
