from PyQt5.QtGui import QDoubleValidator, QIntValidator
import sys, os
from PyQt5.QtWidgets import QHeaderView ,QTableWidgetItem, QTableWidget, QApplication
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QIntValidator ,QValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QComboBox, QDoubleSpinBox, QTextEdit, QRadioButton, QHeaderView
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton
from Funciones_lista import agregar_fila, quitar_fila, eliminar_filas_vacias
from PyQt5.QtWidgets import QAbstractItemView, QFileDialog
from docx.shared import Inches
from PyQt5.QtWidgets import QMessageBox
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml.etree import tostring
from docx.shared import Pt
import PyQt5.QtWidgets as QtWidgets
from datos import resource_path

def setup_validators(window):
    validator = QDoubleValidator()
    validator.setDecimals(2)
    validator.setNotation(QDoubleValidator.StandardNotation)
    validator.setRange(-999999.99, 999999.99)
    validator.setLocale(window.Le5.locale())
    window.Le5.setValidator(validator)
    window.Le6.setValidator(validator)
    return validator

def Ajustar_dinero_IVA(window, Input, Iva, total, validator):
	text = Input.text().replace(",", ".")
	parts = text.split(".")

	# Asegurarse de que haya máximo dos partes (parte entera y parte decimal)
	if len(parts) > 1 and len(parts[1]) > 2:
		# Obtener la parte entera y los primeros dos dígitos de la parte decimal
		formatted_text = parts[0] + "." + parts[1][:2]
		Input.setText(formatted_text)

		return
	try:
		if text:
			resultado = float(text)
			resultado_iva = resultado * 0.21
			resultado_total = resultado * 1.21

			Iva.setText("{:.2f}".format(resultado_iva))
			total.setText("{:.2f}".format(resultado_total))
			Input.setText(text)
			justificacion(window)
          
	except ValueError:
		QMessageBox.information( None,"Importe vacio", "Este importe esta vacio")
		Input.setText("0.00")

def Ajustar_liquidacion(window):
	try:
		window.Le39.setText("{:.2f}".format(abs(float(window.Le26.text()) - float(window.Le32.text())-float(window.Le36.text()))))
		
		window.Le33.setText("{:.2f}".format(float(window.Le32.text()) * 0.21))
		window.Le34.setText("{:.2f}".format(float(window.Le32.text()) * 1.21))
		
		window.Le37.setText("{:.2f}".format(float(window.Le36.text()) * 0.21))
		window.Le38.setText("{:.2f}".format(float(window.Le36.text()) * 1.21))
		
		window.Le40.setText("{:.2f}".format(float(window.Le39.text()) * 0.21))
		window.Le41.setText("{:.2f}".format(float(window.Le39.text()) * 1.21))
		print("entre1")
		try:
			porcentaje = float(window.Le26.text())
			print("entre2")
			if porcentaje != 0.0:
				print("entre3")
				print((str(float(window.Le32.text()) / float(window.Le26.text()))))
				window.Le42.setText("{:.2f}".format((100 * (float(window.Le32.text())) / float(window.Le26.text()))))
		except ValueError:
			print("La cadena no es un número válido en formato float.")
		if (float(window.Le26.text()) - float(window.Le32.text())+float(window.Le36.text()))>0:
			
			window.Le44.setText ("0.00")
			window.Le45.setText ("0.00")
			window.Le46.setText ("0.00")
			window.Le47.setText ( window.Le39.text())
			window.Le48.setText("{:.2f}".format(float(window.Le47.text()) * 0.21))
			window.Le49.setText("{:.2f}".format(float(window.Le47.text()) * 1.21))
		elif (float(window.Le26.text()) - float(window.Le32.text())+float(window.Le36.text())) == 0:
			window.Le44.setText ("0.00")
			window.Le45.setText ("0.00")
			window.Le46.setText ("0.00")			
			window.Le47.setText ("0.00")
			window.Le48.setText ("0.00")
			window.Le49.setText ("0.00")			
		else :	
			window.Le44.setText (window.Le39.text())
			window.Le45.setText("{:.2f}".format(float(window.Le44.text()) * 0.21))
			window.Le46.setText("{:.2f}".format(float(window.Le44.text()) * 1.21))
			window.Le47.setText ("0.00")
			window.Le48.setText ("0.00")
			window.Le49.setText ("0.00")

			
			
			
		if (float(window.Le32.text()) - float(window.Le26.text())) < 0:
			window.Le43.setText(window.Le24.text())
		elif float(window.Le36.text()) == 0:
			window.Le43.setText("")
		else:
			window.Le43.setText("Adif")

	except ValueError:
		# Manejo del error en caso de que ocurra un ValueError
		# Puedes imprimir un mensaje de error o realizar alguna otra acción
		print("Error: Valor no válido ingresado.")

def Ajustar_Dos_Decimales(window, Input, Iva, total, validator):
	text = Input.text().replace(",", ".")
	parts = text.split(".")

	if len(parts) >= 2:
		# Obtener la parte entera y los primeros dos dígitos de la parte decimal
		decimal_part = parts[1][:2]
	else:
		# Agregar una parte decimal de ceros
		decimal_part = "00"

	formatted_text = "{}.{}".format(parts[0], decimal_part)
	Input.setText(formatted_text)


	
def set_TwOfertas(table_oferta):
	table_oferta.setColumnCount(2)  # Definir 2 columnas
	table_oferta.setHorizontalHeaderLabels(['Empresa', 'Oferta'])
	header = table_oferta.horizontalHeader()
	header.setSectionResizeMode(QHeaderView.Stretch)
	
	validator = QDoubleValidator(decimals=2)
	delegate = QStyledItemDelegate()
	table_oferta.setItemDelegateForColumn(0, delegate)
	
	for row in range(table_oferta.rowCount()):
		item = table_oferta.item(row, 0)
		item.setFlags(item.flags() & ~Qt.ItemIsEditable)

	
def set_tabla(table_empresa):
	table_empresa.setRowCount(5)  # Definir 10 filas
	table_empresa.setColumnCount(4)  # Definir 5 columnas
	table_empresa.setHorizontalHeaderLabels(['Empresa', 'NIF', 'Email', 'Persona'])
	table_empresa.setVerticalHeaderLabels(['Emp1', 'Emp2', 'Emp3', 'Emp4', 'Emp5'])
	header = table_empresa.horizontalHeader()
	header.setSectionResizeMode(QHeaderView.Stretch)

	
def setup_ui(window):
	while True:
		try:
			uic.loadUi(resource_path("actas.ui"), window)
			ultima_carpeta = os.path.basename(window.path)
			window.setWindowTitle("Contratos de patrimonio Centro Adif - "+ ultima_carpeta)
			window.setWindowIcon(QIcon(resource_path("icono.jpg")))
			break  # Salir del bucle si la carga es exitosa
		except Exception as e:
			print("Error al cargar la interfaz de usuario:", str(e))
			window.path = QFileDialog.getExistingDirectory(None, "Seleccionar ruta de proyecto")
			print("Ruta seleccionada:", window.path)
			
def mostrar_popup_autores():
	popup = QMessageBox()
	popup.setWindowTitle("Autores")
	popup.setWindowIcon(QIcon(resource_path("icono.jpg")))
	popup.setIconPixmap(QPixmap(resource_path("Autor.jpg")))
	popup.setText("<center> Esta Aplicacion ha sido realizada por <br>Pablo Martin fernandez <br>desarrollada para la Jefatura de Patrimonio centro</center>")
	popup.exec_()
	


def tab(index, TwOfertas,TwEmpresas,window):
	eliminar_filas_vacias(TwEmpresas)
	if index == 0:
		tab_inicio()
	elif index == 1:
		ActasGenerales(TwOfertas,TwEmpresas,window)
	elif index == 2:
		ActasObra()
	elif index == 3:
		Firmas()
def fichero_obra_servicio(ruta_obra, ruta_serv, rb1):
    if rb1.isChecked():
        return ruta_obra
    else:
        return ruta_serv
			 
def  tab_inicio():
	print("tab_inicio")        
def  ActasGenerales(TwOfertas,TwEmpresas,window):
	 Mod_Tabla_oferta(TwOfertas,TwEmpresas,window)

def  Mod_Tabla_oferta(TwOfertas,TwEmpresas,window):

	
	datos_columna = []
	for fila in range(TwEmpresas.rowCount()):
		item = TwEmpresas.item(fila, 0)
		if item is not None:
			datos_columna.append(item.text())

	# Establecer el número de filas en la tabla de destino
	TwOfertas.setRowCount(len(datos_columna))
	
	# Agregar los datos copiados a la tabla de destino
	for fila, dato in enumerate(datos_columna):
		item = QTableWidgetItem(dato)
		TwOfertas.setItem(fila, 0, item)
	#blogqueo de columna 0
	for row in range(TwOfertas.rowCount()):
		item = TwOfertas.item(row, 0)
		item.setFlags(item.flags() & ~Qt.ItemIsEditable)
		
	window.Le30.setText(str(TwOfertas.rowCount()))
	window.Le29.setText(str(Contador_de_empresas(TwOfertas)))
	window.Le26.setText(str(Get_menor_valor(TwOfertas))) 
	window.Le24.setText(str(obtener_nombre_empresa_menor(TwOfertas)))
	window.Le25.setText(window.Le5.text())
	
	
def Actualizar_tabla(TwOfertas, window):
	validator = QIntValidator()
	delegate = QStyledItemDelegate()
	TwOfertas.setItemDelegateForColumn(0, delegate)
	window.Le30.setText(str(TwOfertas.rowCount()))
	window.Le29.setText(str(Contador_de_empresas(TwOfertas)))
	window.Le26.setText(str(Get_menor_valor(TwOfertas)))
	window.Le24.setText(str(obtener_nombre_empresa_menor(TwOfertas)))
	window.Le25.setText(window.Le5.text())
	window.Le27.setText(Vez_y_media(window))
	window.Le28.setText(setenta(window))


def  ActasObra():
	print("ActasObra")
def  Firmas():
	print("Firmas")

def comprobar_datos(self, rango_le):
	alguno_vacio = False

	for i in range(*rango_le):
		line_edit_name = f"Le{i}"
		line_edit = getattr(self, line_edit_name)

		if line_edit.text() == "":
			alguno_vacio = True
			break

	if alguno_vacio:
		QMessageBox.warning(None,  "Campos vacíos", "Falta rellenar algun dato, porfavor revise todos los campos" )
		return False
	else:
		QMessageBox.information( None,"Campos llenos", "Todos los campos rellenos ,obteniendo fichero")
		return True
		
		
def Contador_de_empresas(table_widget):
	contador = 0

	for row in range(table_widget.rowCount()):
		item = table_widget.item(row, 1)
		if item is not None and len(item.text()) > 0:
			contador += 1

	return contador
	
def Get_menor_valor(table_widget):
	menor_valor = float('inf')

	for row in range(table_widget.rowCount()):
		item = table_widget.item(row, 1)
		if item is not None and len(item.text()) > 0:
			valor_str = item.text().replace(',', '.')  # Reemplazar coma por punto
			if valor_str.strip():  # Verificar si el texto no está vacío después de eliminar espacios
				try:
					valor = float(valor_str)
				except ValueError:
					QMessageBox.warning(None,  "error en tipo de dato", "error en tipo de dato" )
				else:
					if valor < menor_valor:
						menor_valor = valor
	return menor_valor
def repeticion_menor_valor(table_widget,valor_buscar):
	contador_repeticiones = 0

	for row in range(table_widget.rowCount()):
		item = table_widget.item(row, 1)
		if item is not None and len(item.text()) > 0:
			valor_str = item.text().replace(',', '.')  # Reemplazar coma por punto
			if valor_str.strip():  # Verificar si el texto no está vacío después de eliminar espacios
				try:
					valor = float(valor_str)
				except ValueError:
					QMessageBox.warning(None,  "error adjudicacion", "Exinten dos empresas  con el minimo valor" )
					
				else:
					if valor == valor_buscar:
						contador_repeticiones += 1
	return contador_repeticiones

def Vez_y_media(window):
	cadena = str (window.Le26.text())
	cadena_limpia = cadena.replace("€", "")
	try:
		valor = float(cadena_limpia)
		return ("{:.2f}".format(valor*1.5))
		

	except ValueError:
		print("Error: The value entered in Le5 is not a valid number.")
		
def setenta(window):
	cadena = str (window.Le26.text())
	cadena_limpia = cadena.replace("€", "")
	try:
		valor = float(cadena_limpia)
		return ("{:.2f}".format(valor*0.7))
		

	except ValueError:
		print("Error: The value entered in Le5 is not a valid number.")

def obtener_nombre_empresa_menor(table_widget):
	menor_valor = float('inf')
	nombre_menor_valor = None

	for row in range(table_widget.rowCount()):
		item_valor = table_widget.item(row, 1)
		item_nombre = table_widget.item(row, 0)

		if item_valor is not None and item_nombre is not None:
			valor_str = item_valor.text().replace(',', '.')  # Reemplazar coma por punto

			if valor_str.strip() and valor_str.replace('.', '').isdigit():  # Verificar si el texto no está vacío y es un número
				valor = float(valor_str)

				if valor < menor_valor:
					menor_valor = valor
					nombre_menor_valor = item_nombre.text()
	return nombre_menor_valor
	
	
def obtener_posicion_empresa_menor(table_widget):
	primera_fila = 4
	menor_valor = None
	posicion_menor_valor = None

	for row in range(table_widget.rowCount()):
		item_valor = table_widget.item(row, 1)

		if item_valor is not None:
			valor_str = item_valor.text().replace(',', '.')  # Reemplazar coma por punto

			if valor_str.strip() and valor_str.replace('.', '').isdigit():  # Verificar si el texto no está vacío y es un número
				valor = float(valor_str)

				if menor_valor is None or valor < menor_valor:
					menor_valor = valor
					posicion_menor_valor = row

	return posicion_menor_valor+1

def justificacion(window): 
	if window.Rb1.isChecked():
		window.Te4.setText(f"El contrato de la obra es por importe de {window.Le5.text()} euros, no superando por tanto el límite de 15.000 € establecido.")
	else:      
		window.Te4.setText(f"El contrato de la obra es por importe de {window.Le5.text()} euros, no superando por tanto el límite de 40.000 € establecido.")

def Servicios_Activos(window):
	window.tabWidget.setTabVisible(2, False)
	justificacion(window)

def Obras_Activos(window):
	window.tabWidget.setTabVisible(2, True)
	justificacion(window)
def Comprobacion_licitado_facturado(window):
	if (window.Le32.text()==window.Le26.text()):
		return (1)
	else:
		QMessageBox.information( None,"Precio de liciatacion diferente ", "El Precio de liciatacion diferente al de adjudicacion  ten cuidado") 
