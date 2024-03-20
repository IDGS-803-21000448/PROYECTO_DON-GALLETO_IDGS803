
from sqlalchemy import not_
import models
from models import *
from datetime import datetime, date
from controllers.controller_alertas import insertarAlertas

def verificarCaducidades():
    subconsulta_mermas = db.session.query(models.MermaMateriaPrima.materia_prima_id).distinct() # Obtiene las Mermas de Materia Prima

    materiasPrimas = models.MateriaPrima.query.filter(not_(models.MateriaPrima.id.in_(subconsulta_mermas))).all() #Obtiene La materia prima que no esta en merma Aún
    fecha_actual = date.today() # Fecha De Hoy
    try:
        for materiaPrima in materiasPrimas:
            dias_para_caducar = (materiaPrima.fecha_caducidad - fecha_actual).days # Cuanros días faltan para que la materia prima Caduque

            if dias_para_caducar <= 0: # Si Caduco Se Agrega la Alerta y se inserta en mermas
                nombre = f"Tienes {materiaPrima.nombre} caducada"
                descripcion = (f"Hay {materiaPrima.cantidad_disponible} de {materiaPrima.nombre} que esta "
                               f"caducada, y fue colocada como merma ")

                datos = {
                    "materia_prima": materiaPrima.id,
                    "tipo": 1,
                    "cantidad": materiaPrima.cantidad_disponible,
                    "descripcion": "Materia Prima a Merma Por Caducidad"
                }

                insertarMermaMateriaPrima(datos)
                insertarAlertas(nombre, descripcion)

            elif dias_para_caducar <= 6: # Si Tiene 6 o menos dias a la fecha de caducidad manda la alerta

                nombre = f"Tienes {materiaPrima.nombre} por caducar"
                descripcion = (f"Hay {materiaPrima.cantidad_disponible} de {materiaPrima.nombre} que esta a "
                               f"{dias_para_caducar} dias de caducar")
                insertarAlertas(nombre, descripcion)

    except Exception as e:
        print("Error al verificar las caducidades: ", e)


def insertarMermaMateriaPrima(datos: dict):
    nuevaMerma = models.MermaMateriaPrima(
                 materia_prima_id= datos["materia_prima"],
                 tipo= datos["tipo"],
                 cantidad= datos["cantidad"],
                 descripcion= datos["descripcion"]
    )

    db.session.add(nuevaMerma)
    db.session.commit()