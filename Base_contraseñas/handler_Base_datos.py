import sqlite3
from handler_encriptador import  encriptar_contrasena,desencriptar_contrasena

def crear_tabla():
    # Conexión a la base de datos y creación de la tabla
    conexion = sqlite3.connect("bd1.db")
    try:
        conexion.execute("""create table tabla_contrasenas (
                              codigo integer primary key autoincrement,
                              pag text,
                              usuario text,
                              contraseña text
                        )""")
        print("Se creó la tabla tabla_contrasenas")
    except sqlite3.OperationalError:
        print("La tabla tabla_contrasenas ya existe")
    conexion.close()

def insertar_datos(pag, usuario, contrasena, contrasena_maestra):
    # Conexión a la base de datos y inserción de datos
    conexion = sqlite3.connect("bd1.db")
    # Encriptar las contrasenas
    contrasena_encriptada = encriptar_contrasena(contrasena, contrasena_maestra)
    usuario_encriptado = encriptar_contrasena(usuario, contrasena_maestra)
    datos = [(pag, usuario_encriptado, contrasena_encriptada)]
    conexion.executemany("INSERT INTO tabla_contrasenas(pag, usuario, contraseña) VALUES (?, ?, ?)", datos)
    conexion.commit()
    conexion.close()

def imprimir_datos_desencriptados(contrasena_maestra):
    # Conexión a la base de datos y obtención de datos
    conexion = sqlite3.connect("bd1.db")
    cursor = conexion.execute("SELECT codigo, pag, usuario, contraseña FROM tabla_contrasenas")
    for fila in cursor:
        codigo, pag, usuario_encriptado, contrasena_encriptada = fila
        # Desencriptar la contraseña y el usuario
        usuario_desencriptado = desencriptar_contrasena(usuario_encriptado, contrasena_maestra)
        contrasena_desencriptada = desencriptar_contrasena(contrasena_encriptada, contrasena_maestra)
        print(f"Código: {codigo}, Página: {pag}, Usuario: {usuario_desencriptado}, Contraseña: {contrasena_desencriptada}")
    conexion.close()

def Get_datos_desencriptados(contrasena_maestra):
    # Crear una lista para almacenar los datos desencriptados
    datos_desencriptados = []

    # Conexión a la base de datos y obtención de datos
    conexion = sqlite3.connect("bd1.db")
    cursor = conexion.execute("SELECT codigo, pag, usuario, contraseña FROM tabla_contrasenas")
    for fila in cursor:
        codigo, pag, usuario_encriptado, contrasena_encriptada = fila
        # Desencriptar la contraseña y el usuario
        usuario_desencriptado = desencriptar_contrasena(usuario_encriptado, contrasena_maestra)
        contrasena_desencriptada = desencriptar_contrasena(contrasena_encriptada, contrasena_maestra)
        
        # Agregar los datos desencriptados a la lista
        datos_desencriptados.append({
            'codigo': codigo,
            'pagina': pag,
            'usuario': usuario_desencriptado,
            'contrasena': contrasena_desencriptada
        })

    conexion.close()
    
    # Devolver los datos desencriptados como un diccionario
    return datos_desencriptados


def imprimir_datos_bruto():
    # Conexión a la base de datos y obtención de datos
    conexion = sqlite3.connect("bd1.db")
    cursor = conexion.execute("select codigo, pag, usuario, contraseña from tabla_contrasenas")
    for fila in cursor:
        print(fila)
    conexion.close()



def eliminar_datos_por_codigo(codigo):
    # Conexión a la base de datos y eliminación de datos
    conexion = sqlite3.connect("bd1.db")
    cursor = conexion.execute("SELECT * FROM tabla_contrasenas WHERE codigo = ?", (codigo,))
    if cursor.fetchone():
        conexion.execute("DELETE FROM tabla_contrasenas WHERE codigo = ?", (codigo,))
        conexion.commit()
        print(f"Registro con código {codigo} eliminado.")
    else:
        print(f"No se encontró un registro con código {codigo}.")
    conexion.close()

def borrar_toda_tabla():
    # Conexión a la base de datos y borrado de la tabla
    conexion = sqlite3.connect("bd1.db")
    conexion.execute("DELETE FROM tabla_contrasenas")
    conexion.commit()
    print("Se han eliminado todos los registros de la tabla.")
    conexion.close()
