from lexer import lexer
from parser import Parser

with open("rutina.txt", "r", encoding="utf-8") as f:
    code = f.read()

tokens = lexer(code)
parser = Parser(tokens)
ast = parser.parse_rutina()

import pprint
pprint.pprint(ast)
