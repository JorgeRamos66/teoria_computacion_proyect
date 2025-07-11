from lexer import lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        else:
            raise SyntaxError(f"Se esperaba {expected_type}, se encontró {self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'}")

    def parse_rutina(self):
        dias = []
        while self.pos < len(self.tokens):
            dias.append(self.parse_dia())
        if len(dias) == 1:
            return {'Rutina': dias[0]}
        return {'Rutina': dias}


    def parse_dia(self):
        dia = self.match('DIA')[1]
        self.match('PUNTOS')
        actividad = self.parse_actividad()
        return {'Dia': {'nombre': dia, 'actividad': actividad}}

    def parse_actividad(self):
        actividades = [self.parse_actividad_simple()]
        while self.peek('PUNTOYCOMA'):
            self.match('PUNTOYCOMA')
            actividades.append(self.parse_actividad_simple())

        if len(actividades) == 1:
            return actividades[0]
        else:
            return {'tipo': 'multiple', 'actividades': actividades}

    def parse_actividad_simple(self):
        if self.peek('GRUPO'):
            grupo = self.match('GRUPO')[1]
            self.match('FLECHA')
            ejercicios = self.parse_ejercicios()
            duracion = self.parse_duracion_opt()
            actividad = {'grupo': grupo, 'ejercicios': ejercicios}
            if duracion:
                actividad['duracion'] = duracion
            return actividad
        elif self.peek('CARDIO'):
            self.match('CARDIO')
            duracion = self.parse_duracion_opt()
            actividad = {}
            if duracion:
                actividad['duracion'] = duracion
            return {'cardio': actividad} if actividad else {'cardio': None}
        elif self.peek('DESCANSO'):
            self.match('DESCANSO')
            duracion = self.parse_duracion_opt()
            actividad = {}
            if duracion:
                actividad['duracion'] = duracion
            return {'descanso': actividad} if actividad else {'descanso': None}
        else:
            raise SyntaxError("Actividad inválida")



    def parse_ejercicios(self):
        ejercicios = [self.parse_ejercicio()]
        while self.peek('COMA'):
            self.match('COMA')
            ejercicios.append(self.parse_ejercicio())
        # Si después de un ejercicio viene otro EJERCICIO sin coma, es error
        if self.peek('EJERCICIO'):
            raise SyntaxError("Se esperaba ',' entre ejercicios")
        return ejercicios

    def parse_ejercicio(self):
        nombre = self.match('EJERCICIO')[1]
        self.match('LPAREN')
        series = self.parse_numero()
        self.match('X')
        repeticiones = self.parse_numero()
        self.match('RPAREN')
        return {
            'Ejercicio': {
                'nombre': nombre,
                'SeriesRep': {
                    'series': series,
                    'reps': repeticiones
                }
            }
        }

    def parse_duracion_opt(self):
        if self.peek('LBRACK'):
            self.match('LBRACK')
            minutos = self.match('NUM')[1]
            if self.peek('MIN') and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'RBRACK':
                self.match('MIN')
            elif self.peek('MIN'):
                raise SyntaxError("Se esperaba ']' después de 'min'")
            else:
                encontrado = self.tokens[self.pos][1] if self.pos < len(self.tokens) else 'EOF'
                raise SyntaxError(f"Se esperaba min, se encontró {encontrado}")
            self.match('RBRACK')
            return f"{minutos} Minutos"
        else:
            return None

    def parse_numero(self):
        num = self.match('NUM')[1]
        return {'Numero': num}

    def peek(self, tipo):
        return self.pos < len(self.tokens) and self.tokens[self.pos][0] == tipo
