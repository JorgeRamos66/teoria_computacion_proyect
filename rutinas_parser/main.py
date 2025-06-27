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
        tokens, error_lexico = lexer(linea)
        if error_lexico:
            print(f"Advertencia: Línea {i} tiene errores léxicos y no será procesada.")
            continue
        parser = Parser(tokens)
        resultado = parser.parse_rutina()
        resultados_validos.append(resultado)
    except SyntaxError as e:
        print(f"Advertencia: Línea {i} no corresponde a la gramática de tipo 2. Detalle: {e}")

def imprimir_arbol(arbol, prefijo="", es_ultimo=True):
    if isinstance(arbol, dict):
        claves = list(arbol.keys())
        for i, clave in enumerate(claves):
            es_ult = (i == len(claves) - 1)
            rama = "└── " if es_ult else "├── "
            print(prefijo + rama + str(clave))
            nuevo_prefijo = prefijo + ("    " if es_ult else "│   ")
            imprimir_arbol(arbol[clave], nuevo_prefijo, True)
    elif isinstance(arbol, list):
        for i, item in enumerate(arbol):
            es_ult = (i == len(arbol) - 1)
            rama = "└── " if es_ult else "├── "
            print(prefijo + rama + f"[{i}]")
            nuevo_prefijo = prefijo + ("    " if es_ult else "│   ")
            imprimir_arbol(item, nuevo_prefijo, True)
    else:
        print(prefijo + "└── " + str(arbol))
print("Árboles de derivación de las rutinas válidas:")
for arbol in resultados_validos:
    imprimir_arbol(arbol)
    print('-' * 40)
