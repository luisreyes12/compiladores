tabla_de_simbolos = {
    r'\{': 'L_LLAVE',
    r'\}': 'R_LLAVE',
    r'\[': 'L_CORCHETE',
    r'\]': 'R_CORCHETE',
    r',': 'COMA',
    r':': 'DOS_PUNTOS',
    r'"[^"]*"': 'LITERAL_CADENA',
    r'true|TRUE': 'PR_TRUE',
    r'false|FALSE': 'PR_FALSE',
    r'null|NULL': 'PR_NULL',
    r'[0-9]+(\.[0-9]+)?((e|E)(\+|-)?[0-9]+)?': 'LITERAL_NUM'
}