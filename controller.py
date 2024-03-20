import json
from http.client import HTTPException

from sqlalchemy import not_

import models
from models import *
from datetime import datetime, date

def obtenerPedidos():
    return True

def obtenerMateriaPrima():
    return True

def verificarPermisos(rol, modulo, accion):
    return True


def verificarCaducidades():
    subconsulta_mermas = db.session.query(models.Merma.materia_prima_id).distinct()

    materiasPrimas = models.MateriaPrima.query.filter(not_(models.MateriaPrima.id.in_(subconsulta_mermas))).all()
    fecha_actual = date.today()
    materia_caducada = []
    materia_caducar = []
    try:
        for materiaPrima in materiasPrimas:
            dias_para_caducar = (materiaPrima.fecha_caducidad - fecha_actual).days
            datos_materia_prima  = {
                "nombre": materiaPrima.nombre,
                "cantidad_discponible": materiaPrima.cantidad_disponible
            }

            if dias_para_caducar <= 0:
               materia_caducada.append(datos_materia_prima)
            elif dias_para_caducar <= 6:
                materia_caducar.append(datos_materia_prima)
        return {"Materia Prima Por Caducar": materia_caducar, "Materia Prima Caducada": materia_caducada}
    except Exception as e:
        print("Error:", e)
        return {"Error": e}

def solicitarProduccion():
    return True


def producir():
    return True
