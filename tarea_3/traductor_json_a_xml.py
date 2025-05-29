import json
import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
from xml.dom import minidom

def dict_to_xml_element(tag_name, value):
    """Convierte una clave y su valor a un elemento XML."""
    element = ET.Element(tag_name)

    if isinstance(value, dict):
        for key, val in value.items():
            child = dict_to_xml_element(key, val)
            element.append(child)
    elif isinstance(value, list):
        if not value:
            return ET.Element(tag_name)  # Lista vacía -> etiqueta vacía
        else:
            for item in value:
                child_tag = tag_name[:-1] if tag_name.endswith('s') else "item"
                element.append(dict_to_xml_element(child_tag, item))
    else:
        element.text = str(value)

    return element

def prettify(elem):
    """Devuelve un string con el XML con indentación."""
    rough_string = ET.tostring(elem, 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="    ")

def seleccionar_archivo():
    """Abre ventana para seleccionar un archivo JSON/TXT."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON or TXT files", "*.json *.txt")]
    )
    return file_path

def main():
    json_path = seleccionar_archivo()
    if not json_path:
        print("No se seleccionó ningún archivo.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error de sintaxis JSON: {e}")
            return

    root_key = next(iter(data))
    root_element = dict_to_xml_element(root_key, data[root_key])

    xml_str = prettify(root_element)

    # Siempre guardar como "traducido.xml"
    with open("traducido.xml", 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print("Traducción completada. Archivo generado: traducido.xml")

if __name__ == "__main__":
    main()
