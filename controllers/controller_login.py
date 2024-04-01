import jwt
import datetime
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash, jsonify, request


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



