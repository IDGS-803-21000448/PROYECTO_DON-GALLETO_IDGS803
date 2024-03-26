import models
from models import *
import datetime
from sqlalchemy import text
from models import db


def agregar_proveedor(form):
    try:
        db.session.execute(
            text("CALL agregar_proveedor(:nombre, :direccion, :telefono, :nombre_vendedor, :estatus)"),
            {
                'nombre': form.nombre.data,
                'direccion': form.direccion.data,
                'telefono': form.telefono.data,
                'nombre_vendedor': form.nombre_vendedor.data,
                'estatus': 1
            }
        )
        db.session.commit()
        return True  # Indica que la inserción se realizó correctamente
    except Exception as e:
        db.session.rollback()
        print("Error al agregar proveedor:", e)
        return False  # Indica que la inserción falló
