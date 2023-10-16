
from time import sleep
from threading import Timer
from datetime import datetime
import pyautogui

class Temporizador_infinito:
    """
    A Thread that executes infinitely
    """
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)
        
    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        
    def start(self):
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        
    def cancel(self):
        self.thread.cancel()

def imprimir_fecha_hora_actual():
    pyautogui.press("f13")
    print("Pulsado f13")
    print(datetime.today())



