from lexer import lexer
from parser import Parser

import os
ruta = os.path.join(os.path.dirname(__file__), "rutina.txt")
with open(ruta, "r", encoding="utf-8") as f:

    code = f.read()

tokens = lexer(code)
parser = Parser(tokens)
ast = parser.parse_rutina()

import pprint
pprint.pprint(ast)
