from cryptography.fernet import Fernet
import os

clave_global = None

def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as clave_file:
        clave_file.write(clave)
    return clave

def cargar_clave():
    global clave_global
    if clave_global is None:
        with open("clave.key", "rb") as clave_file:
            clave_global = clave_file.read()
    return clave_global

def encriptar_texto(texto):
    clave = cargar_clave()
    f = Fernet(clave)
    texto_encriptado = f.encrypt(texto.encode())
    return texto_encriptado.decode()

def desencriptar_texto(texto_encriptado):
    clave = cargar_clave()
    f = Fernet(clave)
    texto_desencriptado = f.decrypt(texto_encriptado.encode())
    return texto_desencriptado.decode()

# # Generar la clave y guardarla en un archivo
# generar_clave()

# # Ejemplo de encriptar el texto
# texto_original = "mysql+pymysql://donGalleto:1234@127.0.0.1/proyecto_don_galleto"
# texto_encriptado = encriptar_texto(texto_original)
# print("Texto encriptado:", texto_encriptado)