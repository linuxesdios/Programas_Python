#realizado por pablo
import cv2
import numpy as np
import pyautogui
import imageio
import keyboard
import time
from threading import Thread
from datetime import datetime

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

# Función para manejar la presión de teclas en segundo plano
def check_key_presses():
    global should_stop_recording
    while True:
        if keyboard.is_pressed('q'):
            should_stop_recording = True
            break
        time.sleep(0.1)

# Inicia un hilo para verificar las teclas en segundo plano
key_thread = Thread(target=check_key_presses)
key_thread.start()

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

except KeyboardInterrupt:
    pass
finally:
    # Agrega un mensaje al final del video indicando que la grabación ha finalizado
    end_message = np.zeros((window_height, window_width, 3), dtype=np.uint8)
    cv2.putText(end_message, "Fin de la grabacion, apliacion de Pablo linuxesdios", (window_width // 4, window_height // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    for _ in range(60):  # Agrega el mensaje durante 1 segundo (20 fotogramas)
        out.write(end_message)

    out.release()

    # Convierte el video a formato AVI usando imageio
    with imageio.get_writer('final_' + output_file, fps=20) as writer:
        for i in range(1, int(out.get(cv2.CAP_PROP_FRAME_COUNT)) + 1):
            img_bgr = cv2.imread(output_file)
            writer.append_data(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))

    # Detiene el hilo de verificación de teclas
    key_thread.join()
