class AnalizadorDeComandos:
    def __init__(self, diccionario_, reglas_):
        self.diccionario = diccionario_
        self.reglas = reglas_
        self.lex = {}
        self.accion_key = None
        self.objeto_key = None
        self.valor_key = None

    def _analisis_lexico(self, commands_normalizados):
            self.lex = {}
            for key, values in self.diccionario.items():
                for command in commands_normalizados:
                    if command in values:
                        self.lex[key] = command

            self.accion_key = None
            self.objeto_key = None
            self.valor_key = None

            for key in self.lex.keys():
                if key.startswith("accion_"):
                    self.accion_key = key
                elif key.startswith("objeto_"):
                    self.objeto_key = key
                elif key == "valor":
                    self.valor_key = key

    def _validacion(self, frase):
        if not self.accion_key or not self.objeto_key:
            return False, f"Faltan la Acción en la frase: '{frase}'"

        roles_compatibles = self.reglas[self.accion_key]

        if self.objeto_key not in roles_compatibles:
            return False, (f"La Acción '{self.lex[self.accion_key]}' ({self.accion_key}) no es compatible "
                           f"con el Objeto '{self.lex[self.objeto_key]}' ({self.objeto_key}).")

        return True, "FRASE VÁLIDA."

    def analizar(self, frase):
        commands = frase.split(" ")
        commands_minus = [c.lower() for c in commands]

        self._analisis_lexico(commands_minus)

        valido, mensaje = self._validacion(frase)

        print("-" * 40)
        print(f"FRASE ANALIZADA: '{frase}'")
        print(f"Roles Léxicos Encontrados: {self.lex}")
        print("-" * 40)

        if valido:
            print(f"{mensaje}")
            accion = self.lex.get(self.accion_key)
            objeto = self.lex.get(self.objeto_key)
            valor = self.lex.get(self.valor_key)

            print(f"Acción: {accion.upper()}, Objeto: '{objeto.upper()}'", end="")
            if valor:
                print(f", Valor: {valor.upper()}")
            else: print("")
        else:
            print(f"ERROR: {mensaje}")

if __name__ == '__main__':
    from config import DICCIONARIO, REGLAS
    analizador = AnalizadorDeComandos(DICCIONARIO, REGLAS)

    analizador.analizar("Sube el volumen ")
