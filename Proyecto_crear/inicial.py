import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog


class ProyectoVentana(QMainWindow):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		# Configura el diseño de la ventana principal
		layout = QVBoxLayout()
		btn_nuevo_proyecto = QPushButton('Crear Nuevo Proyecto')
		btn_abrir_proyecto = QPushButton('Abrir Proyecto Existente')

		# Conecta los botones a las funciones correspondientes
		btn_nuevo_proyecto.clicked.connect(self.crear_nuevo_proyecto)
		btn_abrir_proyecto.clicked.connect(self.abrir_proyecto)

		# Agrega los botones al diseño
		layout.addWidget(btn_nuevo_proyecto)
		layout.addWidget(btn_abrir_proyecto)

		# Crea un widget para contener el diseño
		central_widget = QWidget()
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)

		self.setWindowTitle('Gestión de Proyectos')
		self.show()

	def crear_nuevo_proyecto(self):
		print('Crear un nuevo proyecto')

	def abrir_proyecto(self):
		GUI = Contratos_App()
		GUI.show()
		


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ventana = ProyectoVentana()
	sys.exit(app.exec_())
