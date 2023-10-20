from handler_encriptador import  encriptar_contrasena,desencriptar_contrasena
from handler_Base_datos import  crear_tabla,insertar_datos,Get_datos_desencriptados,imprimir_datos_desencriptados,imprimir_datos_bruto, eliminar_datos_por_codigo, borrar_toda_tabla
import sys
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout
import sqlite3
from cryptography.fernet import InvalidToken



class Aplicacion_base_contrasenas(QWidget):
    def __init__(self, parent=None):
        super(Aplicacion_base_contrasenas, self).__init__(parent)

        self.contrasena_maestra = "mi_contrasena_maestra"
        # Creamos una tabla en donde organizaremos los datos
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(['Paguina', 'Usuario', 'Contrasena']) # Tabla con 3 columnas
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.IbPag = QLabel("Paguina:") # 
        self.txtPag = QLineEdit()
        self.txtPag.setPlaceholderText("Paguina")

        self.lblUsuario = QLabel("Usuario:") # 
        self.txtUsuario = QLineEdit()
        self.txtUsuario.setPlaceholderText("Usuario de la paguina")

        self.lblContrasena = QLabel("Contrasena:") # 
        self.txtContrasena = QLineEdit()
        self.txtContrasena.setPlaceholderText("Contrasena de la la paguina")

        self.lblMaestra = QLabel("Contrasena Maestra:") # 
        self.txtMaestra = QLineEdit()
        self.txtMaestra.setPlaceholderText("contraseña maestra")
        self.txtMaestra.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        grid = QGridLayout() # Declaramo sun gridlayout en donde ingresaremos todos los widget
        grid.addWidget(self.IbPag, 0, 0)
        grid.addWidget(self.txtPag, 0, 1)
        grid.addWidget(self.lblUsuario, 1, 0)
        grid.addWidget(self.txtUsuario, 1, 1)
        grid.addWidget(self.lblContrasena, 2, 0)
        grid.addWidget(self.txtContrasena, 2, 1)
        grid.addWidget(self.lblMaestra, 3, 0)
        grid.addWidget(self.txtMaestra, 3, 1)

        btnCargar = QPushButton('Cargar Datos') # Boton para cargar y mostrar los datos
        btnCargar.clicked.connect(lambda: self.cargarDatos(self.txtMaestra.text())) # función al hacer click sobre el boton


        btnInsertar = QPushButton('Insertar') # Boton agregar datos
        #btnInsertar.clicked.connect(self.insertarDatos) # función al hacer click sobre el boton
        btnInsertar.clicked.connect(lambda: ventana.insertar_datos(ventana.txtPag.text(),ventana.txtUsuario.text(),ventana.txtContrasena.text(),ventana.txtMaestra.text()))
        
        btnEliminar = QPushButton('Eliminar') # Boton para eliminar datos
        #btnEliminar.clicked.connect(self.eliminarDatos)

        hbx = QHBoxLayout() # Declaramos un QHBoxLayout
        # Agregamos los elementos al layout
        hbx.addWidget(btnCargar)
        hbx.addWidget(btnInsertar)
        hbx.addWidget(btnEliminar)

        vbx = QVBoxLayout()
        vbx.addLayout(grid)
        vbx.addLayout(hbx)
        vbx.setAlignment(Qt.AlignTop)
        vbx.addWidget(self.table)

        self.setWindowTitle("Base de Datos de Contrasenas") # Titulo de la ventana
        self.resize(450, 450) # Tamaño de la ventana
        self.setLayout(vbx) # Layout de la ventana

        # Método para agregar datos a la base de datos
    def cargarDatos(self, contrasena_maestra):
            if not contrasena_maestra:
                # Mostrar un cuadro de diálogo con el mensaje de contraseña vacía
                QMessageBox.warning(self, "Contraseña vacía", "La contraseña no puede estar vacía.")
                self.table.setRowCount(0)
                return  # Salir de la función si la contraseña está vacía
            try:
                datos_desencriptados = Get_datos_desencriptados(contrasena_maestra)

                # Limpiar la tabla antes de mostrar nuevos datos
                self.table.setRowCount(0)

                # Insertar los datos desencriptados en la tabla
                for row_position, datos in enumerate(datos_desencriptados):
                    self.table.insertRow(row_position)
                    self.table.setItem(row_position, 0, QTableWidgetItem(datos['pagina']))
                    self.table.setItem(row_position, 1, QTableWidgetItem(datos['usuario']))
                    self.table.setItem(row_position, 2, QTableWidgetItem(datos['contrasena']))
            except InvalidToken:
                # Mostrar un cuadro de diálogo con el mensaje de contraseña no válida
                self.table.setRowCount(0)
                QMessageBox.critical(self, "Contraseña no válida", "La contraseña ingresada no es válida. Por favor, intenta nuevamente.")
    
    def insertar_datos(self, pag, usuario, contrasena, contrasena_maestra):
        # Verificar si algún campo está vacío
        if not pag or not usuario or not contrasena or not contrasena_maestra:
            QMessageBox.warning(self, "Campos vacíos", "Todos los campos deben estar llenos.")
            return  # Salir de la función si algún campo está vacío
        try:
            # Conexión a la base de datos y comprobación de la contraseña maestra
            conexion = sqlite3.connect("bd1.db")
            cursor = conexion.execute("SELECT contraseña FROM tabla_contrasenas LIMIT 1")
            primera_fila = cursor.fetchone()
            if primera_fila:
                primera_contraseña_encriptada = primera_fila[0]
                try:
                    desencriptar_contrasena(primera_contraseña_encriptada, contrasena_maestra)
                except InvalidToken:
                    QMessageBox.critical(self, "Contraseña maestra incorrecta", "La contraseña maestra ingresada no es válida.")
                    return  # Salir de la función si la contraseña maestra no es válida

            # Encriptar las contraseñas
            contrasena_encriptada = encriptar_contrasena(contrasena, contrasena_maestra)
            usuario_encriptado = encriptar_contrasena(usuario, contrasena_maestra)

            datos = [(pag, usuario_encriptado, contrasena_encriptada)]
            conexion.executemany("INSERT INTO tabla_contrasenas(pag, usuario, contraseña) VALUES (?, ?, ?)", datos)
            conexion.commit()
            conexion.close()

            QMessageBox.information(self, "Inserción exitosa", "Los datos se han insertado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error al insertar datos", f"Ha ocurrido un error al insertar datos: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Aplicacion_base_contrasenas()
    ventana.show()
    sys.exit(app.exec_())