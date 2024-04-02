import models
from models import db


def obtenerAlertas():

    return alertas

def insertarAlertas(nombre, descripcion, merma = False):
    nuevaAlerta = models.Alerta(
            nombre = f"{nombre}",
            descripcion = f"{descripcion} ",
            estatus = 0
    )
    if merma:
        alerta_existente = models.Alerta.query.filter_by(descripcion=descripcion).first()
        if not alerta_existente:
            nuevaAlerta = models.Alerta(
                nombre=nombre,
                descripcion=descripcion,
                estatus=0
            )
            db.session.add(nuevaAlerta)
    else:
        db.session.add(nuevaAlerta)
    db.session.commit()