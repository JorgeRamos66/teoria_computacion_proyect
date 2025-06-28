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
    ('PUNTOYCOMA', r';'),
    ('COMA',     r','),
    ('X',        r'x'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACK',   r'\['),
    ('RBRACK',   r'\]'),
    ('MIN',      r'min'),
    ('SKIP',     r'[ \t\n]+'),  # espacios y saltos
    ('MISMATCH', r'[a-zA-Z_]+'),         # cualquier otro carácter
]

def lexer(code):
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
    tokens = []
    error_lexico = False
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUM':
            num = int(value)
            if 1 <= num <= 120:
                tokens.append(('NUM', num))
            else:
                print(f"Advertencia: Número fuera de rango (1-120): {num}")
                error_lexico = True
                continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            print(f"Advertencia: Palabra no válida en la gramática: {value}")
            error_lexico = True
            continue
        else:
            tokens.append((kind, value))
    return tokens, error_lexico