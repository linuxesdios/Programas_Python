import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem

        
def agregar_fila(table_widget):
    row_count = table_widget.rowCount()
    table_widget.insertRow(row_count)
    table_widget.setVerticalHeaderLabels([f"Emp{i+1}" for i in range(row_count + 1)])
    
def agregar_fila_predeterminada(table_widget, valores):
    row_count = table_widget.rowCount()
    table_widget.insertRow(row_count)
    
    # Asigna los valores a la nueva fila
    for col, valor in enumerate(valores):
        item = QTableWidgetItem(str(valor))
        table_widget.setItem(row_count, col, item)
    
    # Actualiza las etiquetas de las filas
    table_widget.setVerticalHeaderLabels([f"Emp{i+1}" for i in range(row_count + 1)])   
     
def agregar_fila_excel(self):
	row_count = self.table_widget.rowCount()
	self.table_widget.insertRow(row_count)
	self.table_widget.setVerticalHeaderLabels([f"Emp{i+1}" for i in range(row_count + 1)])

	# Obtener la fila seleccionada
	selected_row = self.table_widget.currentRow()
	if selected_row != -1:  # Asegura que se ha seleccionado una fila
		for col_index in range(self.table_widget.columnCount()):
			item = self.table_widget.item(selected_row, col_index)
			new_item = QTableWidgetItem(item.text())
			self.table_widget.setItem(row_count, col_index, new_item)
			
def quitar_fila(table_widget):
    row_count = table_widget.rowCount()
    if row_count > 0:
        table_widget.removeRow(row_count - 1)
def eliminar_filas_vacias(table_empresa):
    filas_vacias = []

    for fila in range(table_empresa.rowCount()):
        fila_vacia = True
        for columna in range(table_empresa.columnCount()):
            item = table_empresa.item(fila, columna)
            if item is not None and item.text():
                fila_vacia = False
                break

        if fila_vacia:
            filas_vacias.append(fila)

    # Eliminar las filas vacías en orden inverso para evitar problemas con el índice
    for fila in reversed(filas_vacias):
        table_empresa.removeRow(fila)
# ~ def guardar_tabla(table_widget, file_path):
    # ~ guardar_datos_csv(table_widget, file_path)
