from handler_encriptador import  encriptar_contrasena,desencriptar_contrasena
from handler_Base_datos import  crear_tabla,insertar_datos,imprimir_datos_desencriptados,imprimir_datos_bruto, eliminar_datos_por_codigo, borrar_toda_tabla

contrasena_maestra = "mi_contrasena_maestra"





crear_tabla()
insertar_datos("google", "linuxesdios", "pass1", contrasena_maestra)
insertar_datos("facebook", "pablo", "pass2", contrasena_maestra)
insertar_datos("twitter", "seda", "pass3", contrasena_maestra)
print("bruto")
imprimir_datos_bruto()
print("des")
imprimir_datos_desencriptados(contrasena_maestra)
