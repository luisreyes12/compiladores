import re
from tabla_simbolos import tabla_de_simbolos

class Token:
    def __init__(self, comp_lexico, nro_linea, lexema):
        self.comp_lexico = comp_lexico
        self.nro_linea = nro_linea
        self.lexema = lexema

def get_comp_lex(lexema):
    for expresion, valor in tabla_de_simbolos.items():
        if re.fullmatch(expresion, lexema):
            return valor
    return 'FAIL'

def lexer(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        content = archivo.read()

    tokens = []
    pattern = '|'.join(f'(?P<{v}>{k})' for k, v in tabla_de_simbolos.items())
    regex = re.compile(pattern)
    linea_actual = 1
    for match in regex.finditer(content):
        comp_lexico = match.lastgroup
        lexema = match.group()
        tokens.append(Token(comp_lexico, linea_actual, lexema))

        linea_actual += lexema.count('\n')

    tokens.append(Token("EOF", linea_actual, "EOF"))
    return tokens
