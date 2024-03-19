import models
from models import *
import datetime
from sqlalchemy import text
from models import db


def agregarUsuario(form):
    try:
        db.session.execute(
        text("CALL agregar_usuario(:nombre, :puesto, :rol, :estatus, :usuario, :contrasena)"),
        {
            'nombre': form.nombre.data,
            'puesto': form.puesto.data,
            'rol': form.rol.data,
            'estatus': 'Activo',
            'usuario': form.usuario.data,
            'contrasena': form.contrasena.data
        })
        db.session.commit()  # Guarda los cambios en la base de datos
        return True  # Indica que la operación se realizó correctamente
    except Exception as e:
        db.session.rollback()  # Deshace los cambios en caso de error
        # Maneja el error de alguna manera (por ejemplo, registrándolo o lanzándolo nuevamente)
        print("Error al agregar usuario:", e)
        return False  # Indica que la operación falló


def modificarUsuario(form):
    try:
        db.session.execute(
            text("CALL modificar_usuario(:id, :nombre, :puesto, :rol, :estatus, :usuario, :contrasena)"),
            {
                'id': form.id.data,
                'nombre': form.nombre.data,
                'puesto': form.puesto.data,
                'rol': form.rol.data,
                'estatus': form.estatus.data,
                'usuario': form.usuario.data,
                'contrasena': form.contrasena.data
            }
        )
        db.session.commit()  # Guarda los cambios en la base de datos
        return True  # Indica que la operación se realizó correctamente
    except Exception as e:
        db.session.rollback()  # Deshace los cambios en caso de error
        # Maneja el error de alguna manera (por ejemplo, registrándolo o lanzándolo nuevamente)
        print("Error al modificar usuario:", e)