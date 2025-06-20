from lexer import lexer
from parser import Parser
import pprint

code = """
Lunes: Pecho -> PressBanca(4x10), Fondos(3x12) [45min]
Martes: Cardio [30min]
Miércoles: Espalda -> Remo(4x10), Dominadas(3x8)
Jueves: Descanso
"""

tokens = lexer(code)
parser = Parser(tokens)
ast = parser.parse_rutina()

pprint.pprint(ast)
