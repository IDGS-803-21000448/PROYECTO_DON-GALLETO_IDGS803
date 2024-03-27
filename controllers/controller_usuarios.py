import models
from models import *
import datetime
from sqlalchemy import text
from models import db


# def agregarUsuario(form):
#     try:
#         db.session.execute(
#         text("CALL agregar_usuario(:nombre, :puesto, :rol, :estatus, :usuario, :contrasena)"),
#         {
#             'nombre': form.nombre.data,
#             'puesto': form.puesto.data,
#             'rol': form.rol.data,
#             'estatus': 'Activo',
#             'usuario': form.usuario.data,
#             'contrasena': form.contrasena.data
#         })
#         db.session.commit()  # Guarda los cambios en la base de datos
#         return True  # Indica que la operación se realizó correctamente
#     except Exception as e:
#         db.session.rollback()  # Deshace los cambios en caso de error
#         # Maneja el error de alguna manera (por ejemplo, registrándolo o lanzándolo nuevamente)
#         print("Error al agregar usuario:", e)
#         return False  # Indica que la operación falló


def agregarUsuario(form):
    try:
        nombre = form.nombre.data
        puesto = form.puesto.data
        rol = form.rol.data
        estatus = 'Activo'
        usuario = form.usuario.data
        contrasena = form.contrasena.data

        # Verificar si la contraseña está vacía
        if contrasena:
            db.session.execute(
                text("CALL agregar_usuario(:nombre, :puesto, :rol, :estatus, :usuario, :contrasena)"),
                {
                    'nombre': nombre,
                    'puesto': puesto,
                    'rol': rol,
                    'estatus': estatus,
                    'usuario': usuario,
                    'contrasena': contrasena
                }
            )
        else:
            db.session.execute(
                text("CALL agregar_usuario(:nombre, :puesto, :rol, :estatus, :usuario, NULL)"),
                {
                    'nombre': nombre,
                    'puesto': puesto,
                    'rol': rol,
                    'estatus': estatus,
                    'usuario': usuario
                }
            )

        db.session.commit()  # Guarda los cambios en la base de datos
        return True  # Indica que la operación se realizó correctamente
    except Exception as e:
        db.session.rollback()  # Deshace los cambios en caso de error
        # Maneja el error de alguna manera (por ejemplo, registrándolo o lanzándolo nuevamente)
        print("Error al agregar usuario:", e)
        return False  # Indica que la operación falló


def modificarUsuario(form, id):
    contrasenaAModificar = form.contrasena.data

    if contrasenaAModificar == '' or contrasenaAModificar is None:
        # Si la contraseña está vacía en el formulario, obtén la contraseña actual del usuario desde la base de datos
        try:
            contrasena_actual = db.session.execute(
                text("SELECT contrasena FROM user WHERE id = :id"),
                {'id': id}
            ).fetchone()[0]  # Obtén la primera columna de la primera fila
            contrasenaAModificar = contrasena_actual
        except Exception as e:
            print(f"Error al obtener la contraseña del usuario con ID {id}:", e)
            return False  # Indica que la operación falló

    try:
        db.session.execute(
            text("CALL modificar_usuario(:p_id, :p_nombre, :p_puesto, :p_rol, :p_estatus, :p_usuario, :p_contrasena)"),
            {
                'p_id': id,
                'p_nombre': form.nombre.data,
                'p_puesto': form.puesto.data,
                'p_rol': form.rol.data,
                'p_estatus': 'Activo',
                'p_usuario': form.usuario.data,
                'p_contrasena': contrasenaAModificar,
            })
        db.session.commit()
        return True  # Indica que la operación se realizó correctamente
    except Exception as e:
        db.session.rollback()  # Deshace los cambios en caso de error
        print(f"Error al modificar usuario con ID {id}:", e)
        return False  # Indica que la operación falló

