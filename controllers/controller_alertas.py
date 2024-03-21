import models
from models import db


def obtenerAlertas():

    return alertas

def insertarAlertas(nombre, descripcion):
    nuevaAlerta = models.Alerta(
            nombre = f"{nombre}",
            descripcion = f"{descripcion} ",
            estatus = 1
    )
    db.session.add(nuevaAlerta)
    db.session.commit()