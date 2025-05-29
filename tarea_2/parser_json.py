from super_dr_lexer import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_actual = self.tokens[self.pos]

    def avanzar(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.token_actual = self.tokens[self.pos]

    def emparejar(self, esperado):
        if self.token_actual.comp_lexico == esperado:
            self.avanzar()
        else:
            self.error(f"Se esperaba {esperado}, pero se encontró {self.token_actual.comp_lexico}")
            self.panic_mode([esperado])

    def error(self, mensaje):
        print(f"[ERROR SINTÁCTICO] Línea {self.token_actual.nro_linea}: {mensaje}")

    def panic_mode(self, sincronizacion):
        while self.token_actual.comp_lexico not in sincronizacion and self.token_actual.comp_lexico != "EOF":
            self.avanzar()
        if self.token_actual.comp_lexico in sincronizacion:
            self.avanzar()

    def parse(self):
        self.json()
        if self.token_actual.comp_lexico == "EOF":
            print("El archivo es sintácticamente correcto.")
        else:
            self.error("Contenido inesperado después del fin del JSON.")

    def json(self):
        self.element()

    def element(self):
        if self.token_actual.comp_lexico == "L_LLAVE":
            self.object()
        elif self.token_actual.comp_lexico == "L_CORCHETE":
            self.array()
        else:
            self.error("Se esperaba un objeto o un arreglo.")
            self.panic_mode(["L_LLAVE", "L_CORCHETE"])

    def array(self):
        self.emparejar("L_CORCHETE")
        if self.token_actual.comp_lexico != "R_CORCHETE":
            self.element_list()
        self.emparejar("R_CORCHETE")

    def element_list(self):
        self.element()
        while self.token_actual.comp_lexico == "COMA":
            self.emparejar("COMA")
            self.element()

    def object(self):
        self.emparejar("L_LLAVE")
        if self.token_actual.comp_lexico != "R_LLAVE":
            self.attributes_list()
        self.emparejar("R_LLAVE")

    def attributes_list(self):
        self.attribute()
        while self.token_actual.comp_lexico == "COMA":
            self.emparejar("COMA")
            self.attribute()

    def attribute(self):
        if self.token_actual.comp_lexico == "STRING":
            self.emparejar("STRING")
            self.emparejar("DOS_PUNTOS")
            self.attribute_value()
        else:
            self.error("Se esperaba una clave tipo STRING.")
            self.panic_mode(["COMA", "R_LLAVE"])

    def attribute_value(self):
        if self.token_actual.comp_lexico in ["STRING", "NUMBER", "PR_TRUE", "PR_FALSE", "PR_NULL"]:
            self.avanzar()
        elif self.token_actual.comp_lexico == "L_LLAVE":
            self.object()
        elif self.token_actual.comp_lexico == "L_CORCHETE":
            self.array()
        else:
            self.error("Valor de atributo inválido.")
            self.panic_mode(["COMA", "R_LLAVE", "R_CORCHETE"])