import re
import tkinter as tk
from tkinter import filedialog
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

def abrir_archivo(nombre_archivo, modo):
    return open(nombre_archivo, modo)

def leer_archivo(archivo):
    return archivo.read().split('\n')

def error(nro_linea, lex):
    print("### Dr. JSON detectó ###")
    print(f'  * Ocurrió un error inesperado en la linea {nro_linea}')
    print(f'  * Se encontró: {lex}')
    print("-------------------------------------------")

def lexer(ruta_archivo):
    archivo = abrir_archivo(ruta_archivo, 'r')
    content = leer_archivo(archivo)
    separadores = r'([,:])'
    tokens_array = []
    nro_linea = 0
    
    archivo_salida = abrir_archivo("output.txt", "w")

    for texto in content:
        espacios_inicio = len(texto) - len(texto.lstrip())
        indentacion = texto[:espacios_inicio]

        listado_de_elementos = re.split(separadores, texto.strip())
        nro_linea += 1

        tokens_linea = []

        for lexema in listado_de_elementos:
            if lexema.strip():
                comp_lexico = get_comp_lex(lexema.strip())
                if comp_lexico == 'FAIL':
                    error(nro_linea, lexema)
                    continue
                else:
                    t = Token(comp_lexico, nro_linea, lexema)
                    tokens_array.append(t)
                    tokens_linea.append(t.comp_lexico)

        if tokens_linea:
            archivo_salida.write(indentacion + " ".join(tokens_linea) + "\n")
    
    archivo_salida.close()
    return tokens_array

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona el archivo JSON de entrada",
        filetypes=[("Archivos de texto", "*.txt *.json"), ("Todos los archivos", "*.*")]
    )

    if ruta_archivo:
        lexer(ruta_archivo)
        print("✅ Análisis léxico finalizado. Revisa el archivo output.txt.")
    else:
        print("⚠️ No se seleccionó ningún archivo.")
