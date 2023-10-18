from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
import os
import shutil
from datos import resource_path
import sys
from PyQt5.QtWidgets import QApplication



class Crear_proyecto(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		

	def initUI(self):
		layout = QVBoxLayout()
		self.setFixedSize(500, 200)
		self.setWindowTitle('Creando Proyecto')
		self.setWindowIcon(QIcon('icono.jpg'))

	# Widget para el nombre del proyecto
		self.datos_texto_input = QLineEdit(self)
		self.datos_texto_input.setPlaceholderText('Nombre del proyecto')
		layout.addWidget(self.datos_texto_input)


		# Crear un layout horizontal para la entrada de ruta y el botón
		ruta_layout = QHBoxLayout()
		plantilla_layout = QHBoxLayout()

		# Cuadro de texto para ingresar la ruta
		self.ruta_input = QLineEdit(self)
		self.ruta_input.setPlaceholderText('Ingresa una ruta')
		ruta_layout.addWidget(self.ruta_input)

		# Botón para abrir un cuadro de diálogo y seleccionar una ruta
		boton_seleccionar_ruta = QPushButton('Seleccionar Ruta', self)
		boton_seleccionar_ruta.clicked.connect(self.seleccionar_ruta)
		ruta_layout.addWidget(boton_seleccionar_ruta)

		# Agregar el layout horizontal al layout principal
		layout.addLayout(ruta_layout)


		# selecione plantilla
		self.plantilla_input = QLineEdit(self)
		self.plantilla_input.setPlaceholderText('ingresa plantilla')
		plantilla_layout.addWidget(self.plantilla_input)
		
		
		
		
		# Botón para abrir un cuadro de diálogo y seleccionar una P
		boton_seleccionar_plantilla = QPushButton('Seleccionar plantilla (NO OBLIGATORIO)', self)
		boton_seleccionar_plantilla.clicked.connect(self.seleccionar_plantilla)
		plantilla_layout.addWidget(boton_seleccionar_plantilla)
		
		layout.addLayout(plantilla_layout)

		# Botón para generar el proyecto
		boton_generar_proyecto = QPushButton('Generar Proyecto', self)
		boton_generar_proyecto.clicked.connect(self.Generar_proyecto)
		boton_generar_proyecto.setStyleSheet("background-color: green; color: white;")
		layout.addWidget(boton_generar_proyecto)

		self.setLayout(layout)

	def seleccionar_ruta(self):
		options = QFileDialog.Options()
		ruta_seleccionada = QFileDialog.getExistingDirectory(self, "Seleccionar directorio", options=options)
		if ruta_seleccionada:
			self.ruta_input.setText(ruta_seleccionada)
			
	def seleccionar_plantilla(self):
		options = QFileDialog.Options()
		archivo_seleccionado, _ = QFileDialog.getOpenFileName(self, "Seleccionar plantilla", "", "Archivos potecto (*.PROJPMF);;Todos los archivos (*)", options=options)
		if archivo_seleccionado:
			self.plantilla_input.setText(archivo_seleccionado)
        
	def imprimir_ruta_datos(self):
		ruta = self.ruta_input.text()
		datos_texto = self.datos_texto_input.text()
		if ruta and datos_texto:
			print("Ruta ingresada:", ruta)
			print("Datos de texto ingresados:", datos_texto)
		else:
			QMessageBox.warning(self, "Campos vacíos", "Por favor, ingresa una ruta y datos de texto.")
			
	def Generar_proyecto(self):
		ruta = self.ruta_input.text()
		nombre_proyecto = self.datos_texto_input.text()

		if not ruta or not nombre_proyecto:
			QMessageBox.warning(self, "Campos vacíos", "Por favor, ingresa una ruta y un nombre de proyecto.")
			return

		ruta_proyecto = os.path.join(ruta, nombre_proyecto)

		try:
			os.makedirs(ruta_proyecto)
			os.makedirs(ruta_proyecto+"/0_Modelos")
			os.makedirs(ruta_proyecto+"/1_Salida")
			os.makedirs(ruta_proyecto+"/2_proyecto")
			os.makedirs(ruta_proyecto+"/3_cartas_invitaciones")
			os.makedirs(ruta_proyecto+"/4_ofertas")
			os.makedirs(ruta_proyecto+"/5_cartas_adjudicacion")
			os.makedirs(ruta_proyecto+"/7_segudidad_y_salud")
			print("Esqueleto creado exitosamente en:", ruta_proyecto)
			try:
				mensaje = f"Proyecto creado exitosamente en: {os.path.normpath(ruta_proyecto)}"
				QMessageBox.information(self, "Proyecto Creado", mensaje)
				
				# Copiar el archivo a la carpeta con otro nombre
				nombre_archivo_copiado = nombre_proyecto + ".PROJPMF"
				print("hola1")
				if self.plantilla_input.text():
					ruta_archivo_copiado = os.path.join(ruta_proyecto, nombre_archivo_copiado)
					shutil.copy(self.plantilla_input.text(), ruta_archivo_copiado)
				else:
					ruta_archivo_copiado = os.path.join(ruta_proyecto, nombre_archivo_copiado)
					shutil.copy(resource_path("modelo.PROJPMF"), ruta_archivo_copiado)

				print("hola2")
				# aqui tengo que meter todos los word
				shutil.copy(resource_path("ModeloCartaInvitacion.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "ModeloCartaInvitacion.docx"))
				shutil.copy(resource_path("Modelo_Acta_Liquidacion.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_Acta_Liquidacion.docx"))
				shutil.copy(resource_path("Modelo_Acta_Recepcion.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_Acta_Recepcion.docx"))
				shutil.copy(resource_path("Modelo_Acta_Replanteo.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_Acta_Replanteo.docx"))
				shutil.copy(resource_path("Modelo_Acta_Resolucion_Adjudicacion.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_Acta_Resolucion_Adjudicacion.docx"))
				shutil.copy(resource_path("Modelo_carta_adjudicatario.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_carta_adjudicatario.docx"))
				shutil.copy(resource_path("Modelo_carta_no_adjudicatario.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_carta_no_adjudicatario.docx"))
				shutil.copy(resource_path("Modelo_director_obra.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_director_obra.docx"))
				shutil.copy(resource_path("Modelo_Inicio_Contrato_obr.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_Inicio_Contrato_obr.docx"))
				shutil.copy(resource_path("Modelo_Inicio_Contrato_serv.docx"), os.path.join(ruta_proyecto+"/0_Modelos" , "Modelo_Inicio_Contrato_serv.docx"))
				
				print(f"Archivo copiado a: {ruta_archivo_copiado}")
			except OSError as error:
				QMessageBox.warning(self, "Error al crear el proyecto", f"No se pudo crear el proyecto: {error}")

			# Cerrar la ventana al finalizar la función
			self.close()	
		except OSError as error:
			print(f"No se pudo crear el proyecto: {error}")
if __name__ == "__main__":
	app = QApplication(sys.argv)
	ventana = Crear_proyecto()
	ventana.show()
	sys.exit(app.exec_())
