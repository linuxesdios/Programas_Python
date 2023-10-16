# PROGRAMA REALIZADO POR LINUXESDIOS 
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QHBoxLayout, QSizePolicy
from threading import Timer
from datetime import datetime
from PyQt5.QtGui import QIcon


from Temporizador import Temporizador_infinito, imprimir_fecha_hora_actual
from datos import resource_path

class MiniAplicacion(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Non BLock')
        self.setFixedSize(200, 50)  # Fija el tamaño de la ventana
        icono = QIcon(resource_path("icono.jpg"))

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint & ~Qt.WindowMaximizeButtonHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint) 



        
        
        
        self.setWindowIcon(icono)

        self.btnIniciar = QPushButton('iniciar', self)
        self.btnIniciar.setStyleSheet("width: 10px; height: 40px; background-color: green;")
        self.btnIniciar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Establece política de tamaño fijo

        self.btnParar = QPushButton('parar', self)
        self.btnParar.setStyleSheet("width: 50px; height: 30px; background-color: red;")
        self.btnParar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Establece política de tamaño fijo

        self.txt_caja = QLineEdit(self)
        self.txt_caja.setStyleSheet("width: 30px; height: 40px;")
        self.txt_caja.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Establece política de tamaño fijo
        self.txt_caja.setAlignment(Qt.AlignCenter)
        self.txt_caja.setText("120")

        hbox = QHBoxLayout()  # Layout horizontal
        hbox.addWidget(self.btnIniciar)
        hbox.addWidget(self.btnParar)
        hbox.addWidget(self.txt_caja)

        self.setLayout(hbox)

        self.btnIniciar.clicked.connect(self.on_button1_clicked)
        self.btnParar.clicked.connect(self.on_button2_clicked)
        self.txt_caja.textChanged.connect(self.validate_input)

    def on_button1_clicked(self):
        try:
            tiempo = int(self.txt_caja.text())
        except ValueError:
            self.txt_caja.setText('')  # Si no es un número, limpia el QLineEdit
            return

        # Limita el tiempo entre 1 y 600
        tiempo = max(1, min(tiempo, 600))

        self.temporizador = Temporizador_infinito(tiempo, imprimir_fecha_hora_actual)
        self.temporizador.start()
        self.txt_caja.setStyleSheet("background-color: #80FF80;")

    def on_button2_clicked(self):
        if hasattr(self, 'temporizador'):
            self.temporizador.cancel()
            self.txt_caja.setStyleSheet("background-color: #FF8080;")
        else:
            print("La variable 'temporizador' no está definida")

        

    def validate_input(self):
        # Obtén el texto actual del QLineEdit
        texto = self.txt_caja.text()
        
        # Verifica si el texto es un número válido entre 1 y 600
        try:
            valor = int(texto)
            if valor < 1:
                self.txt_caja.setText('1')
            elif valor > 600:
                self.txt_caja.setText('600')
        except ValueError:
            # Si no es un número, establece el texto a vacío
            self.txt_caja.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiniAplicacion()
    ventana.show()
    sys.exit(app.exec_())