import jwt
import datetime
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash, jsonify, request
import re
import bcrypt

contrasenas_inseguras = {
    "password": True,
    "123456": True,
    "123456789": True,
    "12345678": True,
    "12345": True,
    "qwerty": True,
    "abc123": True,
    "password1": True,
    "admin": True,
    "1234567": True,
    "123123": True,
    "000000": True,
    "password123": True,
    "admin123": True,
    "qwerty123": True,
    "1q2w3e4r": True,
    "login": True,
    "welcome": True,
    "letmein": True,
    "football": True,
    "iloveyou": True,
    "adminadmin": True
}


def requiere_rol(*roles_permitidos):
    def decorador(f):
        @wraps(f)
        def decorado(*args, **kwargs):
            if not current_user.is_authenticated: 
                return redirect(url_for('login.login'))
            if current_user.rol not in roles_permitidos:
                flash('No tienes permiso para acceder a esta página.')
                return redirect(url_for('index.index'))  # Asume que existe una ruta 'index'
            return f(*args, **kwargs)
        return decorado
    return decorador

# Verificacion de Token Multinavegador
def requiere_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Obtener todas las cookies de la solicitud
        cookies = request.cookies
        # Verificar si la cookie de autenticación está presente
        if 'auth_token' in cookies:
            token = cookies['auth_token']
        # Si no se encuentra el token, redirige al usuario al logout
        if not token:
            return redirect(url_for('login.logout'))
        try:
            # Intenta decodificar el token
            data = jwt.decode(token, 'llavesecreta12345', algorithms=["HS256"])
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            flash('El token de autenticación ha expirado.')
            return redirect(url_for('login.logout'))
        except jwt.InvalidTokenError:
            flash('El token de autenticación es inválido.')
            return redirect(url_for('login.logout'))
        except Exception as e:
            print("Excepcion Token:", e)
            flash('Ha ocurrido un error al validar el token de autenticación.')
            return redirect(url_for('login.logout'))
        return f(*args, **kwargs)
    return decorated


def generate_jwt_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expira en 1 hora
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id)  # Asegúrate de que el ID del usuario sea una cadena si no lo es
        }

        token = jwt.encode(
            payload,
            'llavesecreta12345',  # Asegúrate de mantener esta clave segura
            algorithm='HS256'
        )
        # PyJWT v2.0.0+ devuelve una cadena, si estás utilizando una versión anterior, considera decodificar
        return token
    except Exception as e:
        print(f"Error al generar el token JWT: {e}")
        return None

# Verificar que la contraseña no esta dentro del diccionario de contrasenas inseguras, que tenga un caracter especial, una mayuscula y un numero
def es_contrasena_segura(contrasena):
    # Verifica que la contraseña no esté en la lista de contraseñas inseguras
    if contrasenas_inseguras.get(contrasena, False):
        return False, 0
    
    # Verifica que la contraseña tenga al menos un número
    if not re.search(r"\d", contrasena):
        return False, 1
    
    # Verifica que la contraseña tenga al menos una mayúscula
    if not re.search(r"[A-Z]", contrasena):
        return False, 2
    
    # Verifica que la contraseña tenga al menos un carácter especial
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
        return False, 3
    
    return True, 4

def encriptar_contrasena(contrasena):
    # Genera una sal (salt) aleatoria y luego hashea la contraseña con la sal
    salt = bcrypt.gensalt()
    contraseña_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
    return contraseña_encriptada


def verificar_contrasena(contraseña_ingresada, contraseña_encriptada):
    # Asegurarse de que la contraseña encriptada esté en formato bytes
    if isinstance(contraseña_encriptada, str):
        contraseña_encriptada_bytes = contraseña_encriptada.encode('utf-8')
    else:
        contraseña_encriptada_bytes = contraseña_encriptada

    print(contraseña_encriptada_bytes)
    
    # Verifica si la contraseña ingresada coincide con la contraseña encriptada
    return bcrypt.checkpw(contraseña_ingresada.encode('utf-8'), contraseña_encriptada_bytes)



