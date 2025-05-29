class Token:
    def __init__(self, comp_lexico, nro_linea, lexema):
        self.comp_lexico = comp_lexico
        self.nro_linea = nro_linea
        self.lexema = lexema

    def __str__(self):
        return f"{self.comp_lexico} {self.nro_linea} {self.lexema}"

def lexer(path):
    import re
    tokens = []
    errores = []

    expresiones = [
        ("L_CORCHETE", re.compile(r"\[")),
        ("R_CORCHETE", re.compile(r"\]")),
        ("L_LLAVE", re.compile(r"\{")),
        ("R_LLAVE", re.compile(r"\}")),
        ("COMA", re.compile(r",")),
        ("DOS_PUNTOS", re.compile(r":")),
        ("STRING", re.compile(r'"[^"]*"')),
        ("NUMBER", re.compile(r"[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?")),
        ("PR_TRUE", re.compile(r"(true|TRUE)")),
        ("PR_FALSE", re.compile(r"(false|FALSE)")),
        ("PR_NULL", re.compile(r"(null|NULL)")),
    ]

    with open(path, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nro_linea = 1
    for linea in lineas:
        linea = linea.strip()
        while linea:
            match = None
            for tipo, exp in expresiones:
                match = exp.match(linea)
                if match:
                    lexema = match.group(0)
                    tokens.append(Token(tipo, nro_linea, lexema))
                    linea = linea[match.end():].lstrip()
                    break
            if not match:
                errores.append(f"Error léxico en línea {nro_linea}: {linea}")
                break
        nro_linea += 1

    tokens.append(Token("EOF", nro_linea, "EOF"))
    return tokens, errores