import sys, os ,webbrowser ,subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QComboBox, QDoubleSpinBox, QTextEdit, QRadioButton, QHeaderView
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QIntValidator
import pandas as pd
from PyQt5 import QtWidgets, QtCore
from Funciones_lista import agregar_fila, quitar_fila, eliminar_filas_vacias,agregar_fila_predeterminada
from Funciones_auxiliares import Ajustar_liquidacion,repeticion_menor_valor,Comprobacion_licitado_facturado, comprobar_datos,obtener_posicion_empresa_menor, Ajustar_dinero_IVA, fichero_obra_servicio, Ajustar_Dos_Decimales, setup_validators, Actualizar_tabla, set_TwOfertas, Mod_Tabla_oferta, set_tabla, setup_ui, mostrar_popup_autores, tab, justificacion, Servicios_Activos, Obras_Activos
from Funciones_json import cargar_valores_desde_json, guardar_valores_en_json, Sustituir_cartas_adj_no, Sustituir, Sustituir_temp, Sustituir_cartas
from Funciones_tablas import insertar_tabla_en_documento_inicio, insertar_tabla_en_documento_adjudicacion
from excel import ExcelTableApp ,abrir_ventana_excel_desde_otra_funcion
from Crear_proyecto import Crear_proyecto
from inicial import ProyectoVentana
import time
import json
import re
import docx
import shutil
from PyQt5.QtWidgets import QMessageBox
from lxml import etree
from docx import Document
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView, QFileDialog
from docx.shared import Inches
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from excel import ExcelTableApp  
from datos import resource_path

excel_app_instance = None

class Contratos_App(QMainWindow):
	def __init__(self):
		super().__init__()
		
		valores_fila_seleccionada = None
		
		self.filename = ""
		self.path = ""
		self.archivoJson = ""
		
		# Verifica si se proporcionó al menos un argumento
		if argumentos and len(argumentos) >= 1:
			# Extrae la ruta del directorio y el nombre del archivo (incluyendo la extensión) del argumento
			self.path = os.path.dirname(argumentos[0])
			self.filename = os.path.basename(argumentos[0])
		else:

			# Si no se proporciona un argumento, muestra el diálogo de selección de archivo
			options = QFileDialog.Options()
			options |= QFileDialog.ReadOnly  # Solo permite abrir en modo de solo lectura
			self.filename, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", "", "Text Files (*.PROJPMF);;Text Files (*.txt);;All Files (*)", options=options)

			self.path = os.path.dirname(self.filename) if self.filename else ""  # Extrae el directorio del archivo
		print (self.filename )
		print (self.path  )
		print (self.archivoJson  )
		self.archivoJson = os.path.join(self.path, self.filename)

		setup_ui(self)
		set_tabla(self.TwEmpresas) 
		set_TwOfertas(self.TwOfertas)
		validator = setup_validators(self) 
		self.tabWidget.setCurrentIndex(0)  # Establecer la pestaña 1 como la inicial


		# Conectores
		self.TwOfertas.setRowCount(self.TwEmpresas.rowCount())

		#conectores de ventana
		self.actionAutores.triggered.connect(lambda:mostrar_popup_autores())
		self.actionEsquema_contratos.triggered.connect(lambda: os.startfile(resource_path("Diagrama para sic.pdf")))
		self.actionAyuda_con_contratos.triggered.connect(lambda: webbrowser.open("https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902"))
		self.Guardar.clicked.connect(lambda: guardar_valores_en_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas, self.TwOfertas))
		self.actionAbrir_archivo.triggered.connect(lambda: cargar_valores_desde_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas, self.TwOfertas))
		self.actionNew.triggered.connect(lambda:self.Crear_proyecto())
		#conectores de botones de tab1
		self.Generar_Acta_Inicio.clicked.connect(lambda:self.funciones_acta_anicio())
		self.Generar_Cartas_inv.clicked.connect(lambda: self.funciones_Cartas_inv())
		self.Generar_acta_adj.clicked.connect(lambda: self.funciones_acta_adj())
		self.Generar_carta_adj.clicked.connect(lambda: self.funciones_carta_adj())
		self.Generar_acta_liq.clicked.connect (lambda: self.funciones_acta_liq())
		self.Abrir_carpeta.clicked.connect(lambda: (print("Ruta seleccionada:", self.path), webbrowser.open(self.path+"//1_Salida")))
		self.Abrir_portafirmas.clicked.connect(lambda: webbrowser.open("https://portafirmas.adif.es/ePortafirmas/Inicio.do?cr="))
		
		#conectores de botones de tab2
		self.Generar_replanteo.clicked.connect (lambda: self.funciones_acta_replanteo())
		self.Generar_recepcion.clicked.connect (lambda: self.funciones_acta_recepcion())
		self.Generar_Director.clicked.connect (lambda: self.funciones_acta_Director())
		
		#conectores al realizar cambios en objetos 
		self.TwOfertas.itemChanged.connect(lambda item: Actualizar_tabla(self.TwOfertas, self))
		self.Le5.textChanged.connect(lambda:Ajustar_dinero_IVA(self, self.Le5, self.Le6, self.Le7, validator))
		self.Le32.textChanged.connect(lambda:(Ajustar_dinero_IVA(self, self.Le32, self.Le33, self.Le34, validator),Ajustar_liquidacion(self)))	
		self.Le36.textChanged.connect(lambda:(Ajustar_dinero_IVA(self, self.Le32, self.Le33, self.Le34, validator),Ajustar_liquidacion(self)))	
		self.Le5.editingFinished.connect(lambda: Ajustar_Dos_Decimales(self, self.Le5, self.Le6, self.Le7, validator))
		self.Le32.editingFinished.connect(lambda: Ajustar_Dos_Decimales(self, self.Le32, self.Le33, self.Le34, validator))
		self.Pb_add.clicked.connect(lambda: agregar_fila(self.TwEmpresas))
		self.Pb_remove.clicked.connect(lambda: quitar_fila(self.TwEmpresas))
		self.tabWidget.currentChanged.connect(lambda index: tab(index,self.TwOfertas,self.TwEmpresas,self )) 
		self.Rb1.toggled.connect(lambda:Servicios_Activos(self))
		self.Rb2.toggled.connect(lambda:Obras_Activos(self))


		# carga de datos inicial
		
		cargar_valores_desde_json(self,self.archivoJson, (1, 60), (1, 4), (1, 3),(1, 2),(1, 10),self.TwEmpresas, self.TwOfertas)
		
		# al pulsar cada boton ejecutas estas acciones
	
	def funciones_acta_anicio(self):
		try:
			if comprobar_datos(self, (1, 19)):
				eliminar_filas_vacias(self.TwEmpresas)
				guardar_valores_en_json(self, self.archivoJson, (1, 60), (1, 5), (1, 3), (1, 2), (1, 10), self.TwEmpresas, self.TwOfertas)
				insertar_tabla_en_documento_inicio(fichero_obra_servicio(self.path+"//0_Modelos/Modelo_Inicio_Contrato_serv.docx", self.path+"//0_Modelos/Modelo_Inicio_Contrato_obr.docx", self.Rb1), self.path+"//0_Modelos/Inicio_Contrato_prueba_contabla.docx", "EMPRESAS A LAS QUE SOLICITAR OFERTA", self.TwEmpresas.rowCount())
				Sustituir(self, self.path+"//0_Modelos//Inicio_Contrato_prueba_contabla.docx", self.path+"//1_Salida/Inicio_Contrato.docx", self.archivoJson)
				os.remove(self.path+"//0_Modelos//Inicio_Contrato_prueba_contabla.docx")
		except Exception as e:
			QMessageBox.warning(self, "Warning", "An error occurred. Please check the inputs.")		
	
	def funciones_Cartas_inv(self):
		#try:
			if comprobar_datos(self, (1, 30)):
				eliminar_filas_vacias(self.TwEmpresas)
				guardar_valores_en_json(self,self.archivoJson,        (1, 60),   (1, 5),   (1, 3),    (1, 2),   (1, 10),self.TwEmpresas,self.TwOfertas)
				Sustituir_temp(self,self.path+"//0_Modelos//ModeloCartaInvitacion.docx", self.path+"//0_Modelos//ModeloCartaInvitacion_temp.docx", self.archivoJson)
				Sustituir_cartas(self,self.path+"//0_Modelos//ModeloCartaInvitacion_temp.docx","CartaInvitacion.docx",self.archivoJson)
				os.remove(self.path+"//0_Modelos//ModeloCartaInvitacion_temp.docx")
		#except Exception as e:
			#QMessageBox.warning(self, "Warning", "An error occurred. Please check the inputs.")	
			
	def funciones_carta_adj(self):
		#try:
			if comprobar_datos(self, (1, 30)) and repeticion_menor_valor(self.TwOfertas, float(self.Le26.text())) == 1:
				repeticion_menor_valor(self.TwOfertas,float(self.Le26.text()))
				eliminar_filas_vacias(self.TwEmpresas)
				guardar_valores_en_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas,self.TwOfertas)
				Sustituir_temp(self,self.path+"//0_Modelos//Modelo_carta_no_adjudicatario.docx", self.path+"//0_Modelos//Modelo_carta_no_adjudicatario_temp.docx",self.archivoJson)
				Sustituir_temp(self,self.path+"//0_Modelos//Modelo_carta_adjudicatario.docx", self.path+"//0_Modelos//Modelo_carta_adjudicatario_temp.docx",self.archivoJson)
				Sustituir_cartas_adj_no(self,self.path+"//0_Modelos//Modelo_carta_no_adjudicatario_temp.docx",self.path+"//0_Modelos//Modelo_carta_adjudicatario_temp.docx",obtener_posicion_empresa_menor(self.TwOfertas),"carta_no_adjudicatario.docx","carta_adjudicatario.docx",self.archivoJson)
				os.remove(self.path+"//0_Modelos//Modelo_carta_no_adjudicatario_temp.docx")
				os.remove(self.path+"//0_Modelos//Modelo_carta_adjudicatario_temp.docx")
			else: 
				QMessageBox.warning(self, "error en datos", "Revisa los datos , o falta algun datos o hay 2 ofertas similares y mas bajas")
		#except Exception as e:
			#QMessageBox.warning(self, "Warning", "An error occurred. Please check the inputs.")	
	def funciones_acta_adj(self):
		#try:
			if comprobar_datos(self, (1, 30)) and repeticion_menor_valor(self.TwOfertas, float(self.Le26.text())) == 1:
				eliminar_filas_vacias(self.TwEmpresas)
				guardar_valores_en_json(self,self.archivoJson,        (1, 60),   (1, 5),   (1, 3),    (1, 2),   (1, 10),self.TwEmpresas,self.TwOfertas)
				insertar_tabla_en_documento_adjudicacion( self.path+"//0_Modelos//Modelo_Acta_Resolucion_Adjudicacion.docx",self.path+"//0_Modelos//Modelo_Acta_Resolucion_Adjudicacion_temp.docx", "EMPRESAS A LAS QUE SE LES HA SOLICITADO OFERTA", self.TwEmpresas.rowCount())
				Sustituir(self,self.path+"//0_Modelos//Modelo_Acta_Resolucion_Adjudicacion_temp.docx",self.path+"//1_Salida//Acta_Resolucion_Adjudicacion.docx.docx",self.archivoJson)
				os.remove(self.path+"//0_Modelos//Modelo_Acta_Resolucion_Adjudicacion_temp.docx")
			else :
				QMessageBox.warning(self, "error en datos", "Revisa los datos , o falta algun datos o hay 2 ofertas similares y mas bajas")
		#except Exception as e:
			#QMessageBox.warning(self, "Warning", "An error occurred. Please check the inputs.")
				
	def funciones_acta_liq(self):
		try:
			if comprobar_datos(self, (1, 35)):
				Comprobacion_licitado_facturado(self)
				eliminar_filas_vacias(self.TwEmpresas)
				guardar_valores_en_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas,self.TwOfertas)
				Sustituir(self,self.path+"//0_Modelos//Modelo_Acta_Liquidacion.docx",self.path+"//1_Salida//Acta_Liquidacion.docx",self.archivoJson)
		except Exception as e:
			QMessageBox.warning(self, "Warning", "An error occurred. Please check the inputs.")	
	
	def funciones_acta_replanteo(self):
		try:
			if comprobar_datos(self, (1, 39)):
				eliminar_filas_vacias(self.TwEmpresas)
				guardar_valores_en_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas,self.TwOfertas)
				Sustituir(self,self.path+"//0_Modelos//Modelo_Acta_Replanteo.docx",self.path+"//1_Salida//Acta_Replanteo.docx",self.archivoJson)
		except Exception as e:
			QMessageBox.warning(self, "Warning", "An error occurred. Please check the inputs.")	
			
		
	def funciones_acta_recepcion(self):
		if comprobar_datos(self, (1, 45)):
			eliminar_filas_vacias(self.TwEmpresas)
			guardar_valores_en_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas,self.TwOfertas)
			Sustituir(self,self.path+"//0_Modelos//Modelo_Acta_Recepcion.docx",self.path+"//1_Salida//Acta_Recepcion.docx.docx",self.archivoJson)
		
	def funciones_acta_Director(self):
		if comprobar_datos(self, (1, 23)):
			eliminar_filas_vacias(self.TwEmpresas)
			guardar_valores_en_json(self,self.archivoJson, (1, 60), (1, 5), (1, 3),(1, 2),(1, 10),self.TwEmpresas,self.TwOfertas)
			Sustituir(self,self.path+"//0_Modelos//Modelo_director_obra.docx",self.path+"//1_Salida//Acta_director_obra.docx",self.archivoJson)

	def Crear_proyecto(self):
		
		self.Crear_proyecto = Crear_proyecto()  # Crea una instancia de la segunda ventana
		self.Crear_proyecto.show()
		


if __name__ == "__main__":
	argumentos = sys.argv[1:]
	app = QApplication(sys.argv)
	GUI = Contratos_App()
	GUI.show()
	sys.exit(app.exec_())



