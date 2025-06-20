from lexer import lexer
from parser import Parser

import os
ruta = os.path.join(os.path.dirname(__file__), "rutina.txt")

# Lee todo el archivo y guarda las líneas
with open(ruta, encoding='utf-8') as f:
    lineas = f.readlines()

resultados_validos = []

# Verifica cada línea individualmente y guarda solo las válidas
for i, linea in enumerate(lineas, 1):
    try:
        tokens = lexer(linea)
        parser = Parser(tokens)
        resultado = parser.parse_rutina()
        resultados_validos.extend(resultado)
    except SyntaxError as e:
        print(f"Advertencia: Línea {i} no corresponde a la gramática de tipo 2. Detalle: {e}")

# Muestra solo los resultados válidos
import pprint
print("Rutinas válidas encontradas:")
pprint.pprint(resultados_validos)
