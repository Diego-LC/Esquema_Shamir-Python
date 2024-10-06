# Shamir's Secret Sharing

Este proyecto implementa el esquema de compartición de secretos de Shamir en Python. El esquema permite dividir un secreto en varias partes, de modo que solo un número mínimo de partes puede reconstruir el secreto.

## Funciones Principales

### `euclides_extendido(a, b)`

Implementa el algoritmo de Euclides extendido para encontrar el inverso modular.

### `inverso_modular(a, p)`

Encuentra el inverso modular de `a` mod `p` utilizando el algoritmo de Euclides extendido.

### `generar_polinomio(secreto, k)`

Genera un polinomio aleatorio de grado `k-1` con coeficientes en aritmética modular.

### `evaluar_polinomio(coeficientes, x)`

Evalúa un polinomio en un punto `x` utilizando aritmética modular.

### `dividir_secreto_byte(byte_secreto, n, k)`

Genera `n` partes de un byte secreto utilizando un polinomio de grado `k-1`.

### `reconstruir_secreto(partes, k)`

Reconstruye el secreto utilizando interpolación de Lagrange en un campo finito.

### `dividir_texto(texto, n, k)`

Divide un texto en `n` partes, donde se necesitan al menos `k` partes para reconstruir el texto.

### `reconstruir_texto(partes_totales, k)`

Reconstruye el texto original a partir de las partes generadas.

## Ejemplo de Uso

El script `sharmir.py` incluye un ejemplo interactivo donde el usuario puede ingresar un texto, que luego se divide en partes y se reconstruye.

```python
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
```

## Prueba de Seguridad

El script también incluye una función para probar la resistencia del esquema a intentos de reconstrucción con menos partes de las necesarias.

```python
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
```

## Requisitos

  - Python 3.x

## Ejecución

Para ejecutar el script, simplemente se debe correr sharmir.py en el entorno de Python:

```cmd
python sharmir.py
```
