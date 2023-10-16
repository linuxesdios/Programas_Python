import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Para PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Para desarrollo
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Llamar a la función resource_path
    file_path = resource_path("ejemplo.pdf")
    print(f"Intentando abrir el archivo en: {file_path}")

    try:
        os.startfile(file_path)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
