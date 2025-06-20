import re

# Lista de tokens
TOKEN_SPEC = [
    ('NUM',      r'\d+'),
    ('DIA',      r'Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo'),
    ('GRUPO',    r'Pecho|Espalda|Piernas|Bíceps|Tríceps|Hombros|Abdomen'),
    ('EJERCICIO', r'Sentadilla|PressBanca|Dominadas|CurlBíceps|Fondos|Plancha|Remo|PressHombro|Crunch'),
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
            raise RuntimeError(f'Caracter inesperado: {value}')
        else:
            yield (kind, value)
