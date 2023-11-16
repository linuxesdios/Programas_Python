import sys
from PyQt5.QtWidgets import QHeaderView,QAbstractItemView,QMessageBox,QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QComboBox, QDialogButtonBox, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3

class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de Proyectos y Facturas")
        self.setGeometry(100, 100, 800, 600)  # Establece la geometría inicial (ancho x alto)
        self.setFixedSize(800, 600)  # Fija el tamaño de la ventana
        self.setStyleSheet("background-color: white;")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout_principal = QVBoxLayout(self.central_widget)

        # Conectar a la base de datos SQLite
        self.conn = sqlite3.connect("mi_base_de_datos.db")
        self.cursor = self.conn.cursor()

        # Crear las tablas si no existen
        self.create_tables()

        # Crear widgets de la interfaz de usuario
        self.create_ui()

        # Cargar datos en el combo de proyectos y en la tabla al inicio
        self.load_projects()
        self.load_data()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Proyectos (
                ProyectoID INTEGER PRIMARY KEY AUTOINCREMENT,
                NumeroProyecto INTEGER,
                Nombre TEXT NOT NULL,
                Descripcion TEXT,
                Presupuesto DECIMAL(10, 2)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Facturas (
                FacturaID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProyectoID INTEGER,
                Fecha DATE,
                Monto DECIMAL(10, 2),
                Descripcion TEXT,
                FOREIGN KEY (ProyectoID) REFERENCES Proyectos (ProyectoID)
            )
        ''')

        self.conn.commit()

    def create_ui(self):
        # Crear el desplegable para seleccionar proyectos
        self.combo_proyectos = QComboBox(self)
        self.combo_proyectos.setFixedHeight(40)
        self.combo_proyectos.setStyleSheet("background-color: #BBDEFB; color: black;")
        self.combo_proyectos.currentIndexChanged.connect(self.load_data)
        self.layout_principal.addWidget(self.combo_proyectos)

    # Crear la tabla para mostrar las facturas
        self.tabla_facturas = QTableWidget(self)
        self.tabla_facturas.setColumnCount(4)  # 4 columnas en total ('ID', 'Fecha', 'Monto', 'Descripción')
        self.tabla_facturas.setHorizontalHeaderLabels(['Nº de factura', 'Fecha', 'Monto', 'Descripción'])

        # Fijar el tamaño de la primera columna ('Nº de factura')
        self.tabla_facturas.setColumnWidth(0, 100)  # Ajusta el valor según tu preferencia

        # Configurar el modo de redimensionamiento para las otras columnas
        self.tabla_facturas.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Columna 1 estirada
        self.tabla_facturas.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Columna 2 estirada
        self.tabla_facturas.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Columna 3 ajustada al contenido

        # Centrar el texto y los valores solo en las columnas 1, 2 y 3
        for i in range(1, 4):  # Empezar desde la columna 1 hasta la columna 3
            self.tabla_facturas.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        
        self.tabla_facturas.setStyleSheet("background-color: #E0E0E0;")
        self.tabla_facturas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout_principal.addWidget(self.tabla_facturas)

        # Crear botón para agregar facturas en una fila separada
        self.boton_agregar_factura = QPushButton("Agregar Factura", self)
        self.boton_agregar_factura.clicked.connect(self.agregar_factura)
        self.layout_principal.addWidget(self.boton_agregar_factura)
        self.boton_agregar_factura.setStyleSheet("background-color: #4CAF50; color: white;")

        # Etiqueta para mostrar el restante del presupuesto
        self.label_restante = QLabel(self)
 
        self.layout_principal.addWidget(self.label_restante)

        # Botones para crear proyectos, editar proyectos, borrar facturas y borrar proyectos
        self.layout_botones = QHBoxLayout()

        self.boton_crear_proyecto = QPushButton("Crear Proyecto", self)
        self.boton_crear_proyecto.clicked.connect(self.crear_proyecto)
        self.layout_botones.addWidget(self.boton_crear_proyecto)
        self.boton_crear_proyecto.setStyleSheet("background-color: #8BC34A; color: white;")

        self.boton_editar_proyecto = QPushButton("Editar Proyecto", self)
        self.boton_editar_proyecto.clicked.connect(self.editar_proyecto)
        self.layout_botones.addWidget(self.boton_editar_proyecto)
        self.boton_editar_proyecto.setStyleSheet("background-color: #FFFF99; color:  black;")

        self.boton_borrar_factura = QPushButton("Borrar Factura", self)
        self.boton_borrar_factura.clicked.connect(self.borrar_factura)
        self.layout_botones.addWidget(self.boton_borrar_factura)
        self.boton_borrar_factura.setStyleSheet("background-color: #FFCDD2; color: black;")

        self.boton_borrar_proyecto = QPushButton("Borrar Proyecto", self)
        self.boton_borrar_proyecto.clicked.connect(self.borrar_proyecto)
        self.layout_botones.addWidget(self.boton_borrar_proyecto)
        self.boton_borrar_proyecto.setStyleSheet("background-color: #FFCDD2; color:  black;")

        self.layout_principal.addLayout(self.layout_botones)

        # Etiquetas para mostrar datos del proyecto
        self.label_numero_proyecto = QLabel(self)
        self.layout_principal.addWidget(self.label_numero_proyecto)

        self.label_nombre_proyecto = QLabel(self)
        self.layout_principal.addWidget(self.label_nombre_proyecto)

        self.label_descripcion_proyecto = QLabel(self)
        self.layout_principal.addWidget(self.label_descripcion_proyecto)

        self.label_presupuesto_proyecto = QLabel(self)
        self.label_presupuesto_proyecto.setFont(QFont('Arial', 12)) 
        self.layout_principal.addWidget(self.label_presupuesto_proyecto)

        self.label_restante = QLabel(self)
        self.label_restante.setFont(QFont('Arial', 12, QFont.Bold)) 
        self.layout_principal.addWidget(self.label_restante)


    def load_projects(self):
        self.combo_proyectos.clear()
        self.cursor.execute('SELECT ProyectoID, NumeroProyecto, Nombre FROM Proyectos')
        proyectos = self.cursor.fetchall()

        for proyecto in proyectos:
            self.combo_proyectos.addItem(f"{proyecto[1]} - {proyecto[2]}", proyecto[0])

    def load_data(self):
        proyecto_id = self.combo_proyectos.currentData()
        self.tabla_facturas.setRowCount(0)

        if proyecto_id is not None:
            # Cargar facturas
            self.cursor.execute('SELECT FacturaID, Fecha, Monto, Descripcion FROM Facturas WHERE ProyectoID = ?', (proyecto_id,))
            facturas = self.cursor.fetchall()

            for factura in facturas:
                row_position = self.tabla_facturas.rowCount()
                self.tabla_facturas.insertRow(row_position)

                for i, item in enumerate(factura):
                    self.tabla_facturas.setItem(row_position, i, QTableWidgetItem(str(item)))


            # Obtener datos del proyecto
            datos_proyecto = self.get_datos_proyecto(proyecto_id)

            if datos_proyecto:
                numero_proyecto, nombre_proyecto, descripcion_proyecto, presupuesto_proyecto = datos_proyecto
                restante_presupuesto = self.get_presupuesto_proyecto(proyecto_id) - self.get_gastos_proyecto(proyecto_id)

                # Mostrar datos del proyecto
                self.label_numero_proyecto.setText(f"Número de Proyecto: {numero_proyecto}")
                self.label_nombre_proyecto.setText(f"Nombre: {nombre_proyecto}")
                self.label_descripcion_proyecto.setText(f"Descripción: {descripcion_proyecto}")
                self.label_presupuesto_proyecto.setText(f"Presupuesto: {presupuesto_proyecto:.2f} €")
                self.label_restante.setText(f"Restante del Presupuesto: {restante_presupuesto:.2f} €")
            else:
                self.label_numero_proyecto.setText("Número de Proyecto: N/A")
                self.label_nombre_proyecto.setText("Nombre: N/A")
                self.label_descripcion_proyecto.setText("Descripción: N/A")
                self.label_presupuesto_proyecto.setText("Presupuesto: N/A")
                self.label_restante.setText("Restante del Presupuesto: N/A")

    # ...

    def get_presupuesto_proyecto(self, proyecto_id):
        self.cursor.execute('SELECT Presupuesto FROM Proyectos WHERE ProyectoID = ?', (proyecto_id,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado is not None and resultado[0] is not None else 0.0

    def get_gastos_proyecto(self, proyecto_id):
        self.cursor.execute('SELECT SUM(Monto) FROM Facturas WHERE ProyectoID = ?', (proyecto_id,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado is not None and resultado[0] is not None else 0.0
    
    def get_datos_proyecto(self, proyecto_id):
        self.cursor.execute('SELECT NumeroProyecto, Nombre, Descripcion, Presupuesto FROM Proyectos WHERE ProyectoID = ?', (proyecto_id,))
        return self.cursor.fetchone()
    
    def agregar_factura(self):
        proyecto_id = self.combo_proyectos.currentData()
        if proyecto_id is not None:
            dialogo = DialogoFactura(self, proyecto_id)
            if dialogo.exec_():
                fecha = dialogo.fecha.text()
                monto_str = dialogo.monto.text()
                descripcion = dialogo.descripcion.text()

                try:
                    monto = float(monto_str.replace(",", "."))  # Reemplazar coma por punto
                except ValueError:
                    QMessageBox.critical(self, 'Error', 'El monto no es un número válido.')
                    return

                self.cursor.execute('''
                    INSERT INTO Facturas (ProyectoID, Fecha, Monto, Descripcion)
                    VALUES (?, ?, ?, ?)
                ''', (proyecto_id, fecha, monto, descripcion))

                self.conn.commit()
                self.load_data()

    def crear_proyecto(self):
        dialogo = DialogoProyecto(self)
        if dialogo.exec_():
            numero_proyecto = dialogo.numero_proyecto.text()
            nombre = dialogo.nombre.text()
            descripcion = dialogo.descripcion.text()
            presupuesto_str = dialogo.presupuesto.text()

            try:
                presupuesto = float(presupuesto_str.replace(",", "."))  # Reemplazar coma por punto
            except ValueError:
                QMessageBox.critical(self, 'Error', 'El presupuesto no es un número válido.')
                return

            self.cursor.execute('''
                INSERT INTO Proyectos (NumeroProyecto, Nombre, Descripcion, Presupuesto)
                VALUES (?, ?, ?, ?)
            ''', (numero_proyecto, nombre, descripcion, presupuesto))

            self.conn.commit()
            self.load_projects()

    def editar_proyecto(self):
        proyecto_id = self.combo_proyectos.currentData()
        if proyecto_id is not None:
            dialogo = DialogoEditarProyecto(self, proyecto_id)
            if dialogo.exec_():
                nombre = dialogo.nombre.text()
                descripcion = dialogo.descripcion.text()
                presupuesto_str = dialogo.presupuesto.text()

                try:
                    presupuesto = float(presupuesto_str.replace(",", "."))  # Reemplazar coma por punto
                except ValueError:
                    # Mostrar un cuadro de diálogo de error
                    QMessageBox.critical(self, 'Error', 'El monto no es un número válido.')
                    return

                self.cursor.execute('''
                    UPDATE Proyectos 
                    SET Nombre = ?, Descripcion = ?, Presupuesto = ?
                    WHERE ProyectoID = ?
                ''', (nombre, descripcion, presupuesto, proyecto_id))

                self.conn.commit()
                self.load_projects()

    def borrar_factura(self):
        # Mostrar cuadro de diálogo de confirmación
        respuesta = QMessageBox.question(self, 'Confirmar Borrado', '¿Estás seguro de que deseas borrar la factura?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Procesar la respuesta del usuario
        if respuesta == QMessageBox.Yes:
            selected_row = self.tabla_facturas.currentRow()
            if selected_row >= 0:
                factura_id = int(self.tabla_facturas.item(selected_row, 0).text())
                self.cursor.execute('DELETE FROM Facturas WHERE FacturaID = ?', (factura_id,))
                self.conn.commit()
                self.load_data()

    def borrar_proyecto(self):
        # Mostrar cuadro de diálogo de confirmación
        respuesta = QMessageBox.question(self, 'Confirmar Borrado', '¿Estás seguro de que deseas borrar el proyecto?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Procesar la respuesta del usuario
        if respuesta == QMessageBox.Yes:
            proyecto_id = self.combo_proyectos.currentData()
            if proyecto_id is not None:
                self.cursor.execute('DELETE FROM Proyectos WHERE ProyectoID = ?', (proyecto_id,))
                self.conn.commit()
                self.load_projects()

class DialogoFactura(QDialog):
    def __init__(self, parent=None, proyecto_id=None):
        super().__init__(parent)

        self.setWindowTitle("Agregar Factura")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QFormLayout(self)

        self.fecha = QLineEdit(self)
        self.monto = QLineEdit(self)
        self.descripcion = QLineEdit(self)

        self.layout.addRow("Fecha:", self.fecha)
        self.layout.addRow("Monto:", self.monto)
        self.layout.addRow("Descripción:", self.descripcion)

        self.boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.boton_box.accepted.connect(self.accept)
        self.boton_box.rejected.connect(self.reject)

        self.layout.addRow(self.boton_box)

class DialogoProyecto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Crear Proyecto")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QFormLayout(self)

        self.numero_proyecto = QLineEdit(self)
        self.nombre = QLineEdit(self)
        self.descripcion = QLineEdit(self)
        self.presupuesto = QLineEdit(self)

        self.layout.addRow("Número de Proyecto:", self.numero_proyecto)
        self.layout.addRow("Nombre:", self.nombre)
        self.layout.addRow("Descripción:", self.descripcion)
        self.layout.addRow("Presupuesto:", self.presupuesto)

        self.boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.boton_box.accepted.connect(self.accept)
        self.boton_box.rejected.connect(self.reject)

        self.layout.addRow(self.boton_box)

class DialogoEditarProyecto(QDialog):
    def __init__(self, parent=None, proyecto_id=None):
        super().__init__(parent)

        self.setWindowTitle("Editar Proyecto")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QFormLayout(self)

        self.nombre = QLineEdit(self)
        self.descripcion = QLineEdit(self)
        self.presupuesto = QLineEdit(self)

        self.layout.addRow("Nombre:", self.nombre)
        self.layout.addRow("Descripción:", self.descripcion)
        self.layout.addRow("Presupuesto:", self.presupuesto)

        self.boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.boton_box.accepted.connect(self.accept)
        self.boton_box.rejected.connect(self.reject)

        self.layout.addRow(self.boton_box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec_())
