import re

class UNOParser:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tokens = self.tokenize()
        self.index = 0

    def tokenize(self):
        # Tokeniza la entrada en partes relevantes
        tokens = re.findall(r'\b\w+\b|[+*-]', self.input_str)
        return tokens

    def parse_card(self):
        """
        Parsea una carta de UNO
        <CARD> -> <COLOR> <NUMBER> | <SPECIAL>
        <COLOR> -> rojo | azul | verde | amarillo
        <NUMBER> -> 0-9
        <SPECIAL> -> "cualquier carta especial" (representación simplificada)
        """
        if self.index >= len(self.tokens):
            return None

        color = self.tokens[self.index]
        self.index += 1

        if color in ["rojo", "azul", "verde", "amarillo"]:
            if self.index < len(self.tokens):
                numero = self.tokens[self.index]
                if numero.isdigit():
                    self.index += 1
                    return {"tipo": "carta", "color": color, "numero": numero}

        # Ver si es una carta especial
        if color.lower() == "cualquier carta especial":
            self.index += 1
            return {"tipo": "especial", "descripcion": color}

        print(f"Error de sintaxis en carta: {color}")
        return None

    def parse_juego(self):
        """
        Parsea el juego completo
        <JUEGO> -> <CARTAS> <REGLAS>
        <CARTAS> -> <CARTA>*
        <REGLAS> -> <REGLA>*
        """
        cartas = []
        reglas = []

        # Primero, parseamos las cartas
        while self.index < len(self.tokens):
            if self.tokens[self.index] in ["rojo", "azul", "verde", "amarillo"]:
                carta = self.parse_card()
                if carta:
                    cartas.append(carta)
                else:
                    break
            else:
                break

        # Ahora parseamos las reglas
        while self.index < len(self.tokens):
            regla = self.parse_regla()
            if regla:
                reglas.append(regla)
            else:
                break

        if cartas or reglas:
            return {"cartas": cartas, "reglas": reglas}
        else:
            return None

    def parse_regla(self):
        """
        Parsea una regla del juego
        <REGLA> -> "No jugar cartas que no coincidan en color o número" 
                  | "Robar una carta si no puede jugar" 
                  | "Ganar al quedar sin cartas"
                  | ...
        """
        regla_str = ' '.join(self.tokens[self.index:self.index+10]).strip()
        known_rules = [
            "No jugar cartas que no coincidan en color o número",
            "Robar una carta si no puede jugar",
            "Ganar al quedar sin cartas"
        ]

        if regla_str in known_rules:
            # Avanzar los tokens correspondientes
            self.index += len(regla_str.split())
            return {"tipo": "regla", "descripcion": regla_str}
        else:
            print(f"Regla desconocida: {regla_str}")
            return None

def main():
    # Ejemplo de entrada válida
    entrada_uno = """
    rojo 3 azul 5 verde 7
    No jugar cartas que no coincidan en color o número
    Robar una carta si no puede jugar
    Ganar al quedar sin cartas
    """

    parser = UNOParser(entrada_uno)
    resultado = parser.parse_juego()

    if resultado:
        print("Juego parseado correctamente:")
        print("\nCartas:")
        for carta in resultado['cartas']:
            print(f"- {carta}")
        print("\nReglas:")
        for regla in resultado['reglas']:
            print(f"- {regla['descripcion']}")
    else:
        print("Error al parsear el juego")

if __name__ == "__main__":
    main()