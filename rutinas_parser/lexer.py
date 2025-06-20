import re

# Lista de tokens
TOKEN_SPEC = [
    ('NUM',      r'\d+'),
    ('DIA',      r'Lunes|Martes|Miercoles|Jueves|Viernes|Sabado|Domingo'),
    ('GRUPO',    r'Pecho|Espalda|Piernas|Biceps|Triceps|Hombros|Abdomen'),
    ('EJERCICIO', r'Sentadilla|PressBanca|Dominadas|CurlBiceps|Fondos|Plancha|Remo|PressHombro|Crunch'),
    ('CARDIO',   r'Cardio'),
    ('DESCANSO', r'Descanso'),
    ('FLECHA',   r'->'),
    ('PUNTOS',   r':'),
    ('COMA',     r','),
    ('X',        r'x'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACK',   r'\['),
    ('RBRACK',   r'\]'),
    ('MIN',      r'min'),
    ('SKIP',     r'[ \t\n]+'),  # espacios y saltos
    ('MISMATCH', r'.'),         # cualquier otro carácter
]

def lexer(code):
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUM':
            yield ('NUM', int(value))
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            print(f"Advertencia: Caracter no perteneciente a la gramática: {value}")
            continue  # Ignora el caracter y sigue
        else:
            yield (kind, value)