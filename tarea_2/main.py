import tkinter as tk
from tkinter import filedialog
from super_dr_lexer import lexer
from parser_json import Parser

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Seleccionar archivo JSON")
    return archivo

def main():
    archivo_entrada = seleccionar_archivo()
    if not archivo_entrada:
        print("No se seleccionó ningún archivo.")
        return

    tokens, errores = lexer(archivo_entrada)
    if errores:
        print("Errores léxicos encontrados:")
        for e in errores:
            print(e)
        return

    parser = Parser(tokens)
    parser.parse()

if __name__ == "__main__":
    main()