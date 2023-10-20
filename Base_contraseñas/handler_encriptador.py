import base64
import hashlib
from cryptography.fernet import Fernet

def obtener_clave_maestra_hash(contrasena_maestra):
    # Generar un hash de la contraseña maestra
    return hashlib.sha256(contrasena_maestra.encode()).digest()

def generar_clave_encriptacion(contrasena_maestra, salt):
    clave_maestra_hash = obtener_clave_maestra_hash(contrasena_maestra)
    return base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', clave_maestra_hash, salt, 100000))

def encriptar_contrasena(contrasena, contrasena_maestra):
    salt = b'salt'  # Cambia esto a un valor aleatorio y único
    clave_encriptacion = generar_clave_encriptacion(contrasena_maestra, salt)
    cipher_suite = Fernet(clave_encriptacion)
    contrasena_encriptada = cipher_suite.encrypt(contrasena.encode())
    return contrasena_encriptada

def desencriptar_contrasena(contrasena_encriptada, contrasena_maestra):
    salt = b'salt'  # Debe ser el mismo que se usó en la encriptación
    clave_encriptacion = generar_clave_encriptacion(contrasena_maestra, salt)
    cipher_suite = Fernet(clave_encriptacion)
    contrasena_desencriptada = cipher_suite.decrypt(contrasena_encriptada).decode()
    return contrasena_desencriptada