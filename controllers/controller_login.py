from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

def requiere_rol(*roles_permitidos):
    def decorador(f):
        @wraps(f)
        def decorado(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.rol not in roles_permitidos:
                flash('No tienes permiso para acceder a esta página.')
                return redirect(url_for('index'))  # Asume que existe una ruta 'index'
            return f(*args, **kwargs)
        return decorado
    return decorador

