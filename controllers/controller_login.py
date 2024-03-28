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

def requiere_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verifica si hay un token en el encabezado de autorización
        if 'Cookie' in request.headers:
            cookie = request.headers['Cookie'].split(";")[0]
            if 'auth_token=' in cookie:
                token = cookie.split('auth_token=')[1].strip()
        if not token:
            return redirect(url_for('login.logout'))
        try:
            # Intenta decodificar el token
            data = jwt.decode(token, 'llavesecreta12345', algorithms=["HS256"])
            current_user = data['sub']
        except:
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



