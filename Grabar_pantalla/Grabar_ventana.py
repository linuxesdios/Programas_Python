import cv2
import numpy as np
import pyautogui
import imageio
from datetime import datetime
import tkinter as tk
from threading import Thread
import time

# Obtiene las dimensiones de la pantalla
screen_width, screen_height = pyautogui.size()

# Calcula las dimensiones de la ventana (usaremos toda la pantalla)
window_width = screen_width
window_height = screen_height

# Obtiene la fecha y hora actual para incluir en el nombre del archivo
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f"Grabacion_{current_datetime}.avi"

# Bandera para indicar si se debe terminar la grabación
should_stop_recording = False

# Función que se ejecuta al cerrar la ventana
def on_closing():
    global should_stop_recording
    should_stop_recording = True
    root.destroy()

# Función principal para la grabación
def start_recording():
    global should_stop_recording
    # Configura el codec y el objeto VideoWriter
    codec = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_file, codec, 20, (window_width, window_height))

    try:
        while not should_stop_recording:
            # Captura de pantalla completa
            screenshot = pyautogui.screenshot()

            # Convierte a un arreglo NumPy
            img_np = np.array(screenshot)

            # Convierte la imagen de BGR a RGB
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Añade el fotograma al archivo de video
            out.write(img_bgr)

            # Espera un corto tiempo antes de tomar otro fotograma
            root.update()  # Actualiza la interfaz gráfica
            time.sleep(0.05)  # Espera 50 milisegundos

    finally:
        # Agrega un mensaje al final del video indicando que la grabación ha finalizado
        end_message = np.zeros((window_height, window_width, 3), dtype=np.uint8)
        cv2.putText(end_message, "Fin de la grabacion, aplicacion de Pablo linuxesdios", (window_width // 4, window_height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        for _ in range(60):  # Agrega el mensaje durante 1 segundo (60 fotogramas)
            out.write(end_message)

        out.release()

        # Convierte el video a formato AVI usando imageio
        with imageio.get_writer('final_' + output_file, fps=20) as writer:
            for i in range(1, int(out.get(cv2.CAP_PROP_FRAME_COUNT)) + 1):
                img_bgr = cv2.imread(output_file)
                writer.append_data(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))

# Crear la ventana
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.attributes('-topmost', True)  # Mantener la ventana en primer plano
root.resizable(0, 0)  # Bloquear la capacidad de redimensionar

# Iniciar la grabación en el hilo principal
start_recording()

# Ejecuta el bucle principal de la interfaz gráfica
root.mainloop()