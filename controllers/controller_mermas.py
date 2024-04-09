
from sqlalchemy import not_
import models
from models import *
from datetime import datetime, date
from controllers.controller_alertas import insertarAlertas
from controllers.controller_materia_prima import actualizar_cantidades_tipo

def verificarCaducidades():
    materiasPrimas = MateriaPrima.query.filter_by(estatus = 1).all()  #Obtiene La materia prima que no esta en merma Aún
    fecha_actual = date.today() # Fecha De Hoy
    try:
        for materiaPrima in materiasPrimas:
            dias_para_caducar = (materiaPrima.fecha_caducidad - fecha_actual).days # Cuanros días faltan para que la materia prima Caduque

            if dias_para_caducar <= 0: # Si Caduco Se Agrega la Alerta y se inserta en mermas
                nombre = f"Tienes {materiaPrima.tipo_materia.nombre} caducada"
                descripcion = (f"Hay {materiaPrima.cantidad_disponible}{materiaPrima.tipo} de {materiaPrima.tipo_materia.nombre} que esta "
                               f"caducada del lote {materiaPrima.lote}, y fue colocada como merma ")

                datos = {
                    "materia_prima": materiaPrima.id,
                    "tipo": materiaPrima.tipo,
                    "cantidad": materiaPrima.cantidad_disponible,
                    "descripcion": "Materia Prima a Merma Por Caducidad"
                }
                materiaPrima.cantidad_disponible = 0
                materiaPrima.estatus = 3
                db.session.commit()
                actualizar_cantidades_tipo()
                insertarMermaMateriaPrima(datos)
                insertarAlertas(nombre, descripcion, True)

            elif dias_para_caducar <= 6: # Si Tiene 6 o menos dias a la fecha de caducidad manda la alerta

                nombre = f"Tienes {materiaPrima.tipo_materia.nombre} por caducar"
                descripcion = (f"Hay {materiaPrima.cantidad_disponible}{materiaPrima.tipo} de {materiaPrima.tipo_materia.nombre} que esta a "
                               f"{dias_para_caducar} dias de caducar del lote {materiaPrima.lote}")
                insertarAlertas(nombre, descripcion, True)

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

def insertarMermaGalleta(produccion: Produccion):
    nuevaMerma = models.MemraGalleta(
        produccion_id= produccion.id,
        cantidad= produccion.galletas_disponibles,
        descripcion= "Merma por Caducidad",
        tipo = "pz"
    )

    db.session.add(nuevaMerma)
    db.session.commit()

def getMateriasPrimasSinMerma():

    materiasPrimas = MateriaPrima.query.filter_by(estatus = 1).all()

    return materiasPrimas



def verificarCaducidadesGalletas():
    producciones = Produccion.query.filter_by(estatus = "terminada").all()  #Obtiene La materia prima que no esta en merma Aún
    fecha_actual = date.today() # Fecha De Hoy
    try:
        for produccion in producciones:
            dias_para_caducar = (fecha_actual -produccion.fecha_producido.date()).days # Cuanros días faltan para que la materia prima Caduque

            if dias_para_caducar >= 14 and produccion.galletas_disponibles != 0: # Si Caduco Se Agrega la Alerta y se inserta en mermas
                nombre = f"Tienes Galletas de {produccion.receta.nombre} caducada"
                descripcion = (f"Hay {produccion.galletas_disponibles} galletas de {produccion.receta.nombre} que esta "
                               f"caducada del lote {produccion.lote}, y fue colocada como merma ")

                produccion.receta.Costo_Galleta.galletas_disponibles -=  produccion.galletas_disponibles
                db.session.commit()

                produccion.galletas_disponibles = 0
                db.session.commit()

                insertarMermaGalleta(produccion)
                insertarAlertas(nombre, descripcion, True)

            elif dias_para_caducar >= 12 and produccion.galletas_disponibles != 0:

                nombre = f"Tienes galletas {produccion.receta.nombre} por caducar"
                descripcion = (f"Hay {produccion.galletas_disponibles} galletas de {produccion.receta.nombre}  que estan a "
                               f"{14 - dias_para_caducar} dias de caducar del lote {produccion.lote}")
                insertarAlertas(nombre, descripcion, True)

    except Exception as e:
        print("Error al verificar las caducidades: ", e)