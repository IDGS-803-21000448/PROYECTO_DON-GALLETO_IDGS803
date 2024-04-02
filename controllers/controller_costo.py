
import math
import models
from models import *
from datetime import datetime
from flask import flash, redirect, url_for, Flask
from sqlalchemy import desc

def actualizar_costos():
    recetas = models.Receta.query.filter_by(estatus=1).all()

    materias_primas = []
    suma_costos = 0

    cantidad_materias = 0

    for receta in recetas:
        costos = models.CostoGalleta.query.filter_by(id=receta.id).first()
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id).all()
        ids_ingredientes = [detalle.tipo_materia_id for detalle in detalles_receta]
        factor_ajuste_mano_obra = 0.5 # Factor de ajuste para la mano de obra

        # Realizar la consulta de Materias Prima para cada ID de ingrediente
        for id_ingrediente in ids_ingredientes:
            materias = MateriaPrima.query.filter_by(id_tipo_materia=id_ingrediente, estatus=1).all()

            if materias:
                total_precio_materia = sum(m.precio_compra for m in materias)
                cantidad_materias += len(materias)

                for materia in materias:
                    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id).first()
                    cantidad_materia = convertirCantidades(materia.tipo, detalles_receta.unidad_medida, detalles_receta.cantidad_necesaria)

                    precio_por_kg = total_precio_materia / cantidad_materia

                    # Aplicar el factor de ajuste a la mano de obra
                    costos = CostoGalleta.query.filter_by(id=receta.id).first()
                    if costos.mano_obra is None:
                        mano_obra = costos.mano_obra = 100
                        costos.mano_obra = mano_obra * factor_ajuste_mano_obra

                    # Calcular el costo de los ingredientes utilizados en la receta con el ajuste de la mano de obra
                    costo_ingredientes = ((cantidad_materia * precio_por_kg) + costos.mano_obra) / materia.cantidad_compra

                    detalle_materia_prima = {
                        'id': materia.id,
                        'precio_compra': materia.precio_compra,
                        'cantidad_compra': materia.cantidad_compra,
                        'cantidad_disponible': materia.cantidad_disponible,
                        'precio_por_kg': precio_por_kg, 
                        'fecha_caducidad': materia.fecha_caducidad,
                        'lote': materia.lote,
                        'tipo': materia.tipo,
                        'unidad_receta': detalles_receta.unidad_medida,
                        'costo_ingredientes': costo_ingredientes
                    }
                    materias_primas.append(detalle_materia_prima)
                    suma_costos += costo_ingredientes
                    insertar_costos(cantidad_materias, suma_costos, receta.id, costos.mano_obra)
            else:
                flash('No se encontraron materias primas activas para este tipo de materia', 'warning')

def insertar_costos(cantidad_materias, suma_costos, receta_id, costo_mano_obra):
    if cantidad_materias > 0:
        promedio_costos = suma_costos / cantidad_materias
        precio_galleta = math.ceil(promedio_costos * 0.2)

        costo_existente = CostoGalleta.query.filter_by(id=receta_id).first()

        if costo_existente:
            costo_existente.precio = precio_galleta
            costo_existente.mano_obra = costo_mano_obra
            costo_existente.fecha_utlima_actualizacion = datetime.now()
        else:
            nuevo_costo_galleta = CostoGalleta(
                id=receta_id,
                precio=precio_galleta,
                galletas_disponibles=0,
                mano_obra=costo_mano_obra,
                fecha_utlima_actualizacion=datetime.now()
            )
            db.session.add(nuevo_costo_galleta)

        receta_a_actualizar = Receta.query.filter_by(id=receta_id).first()
        if receta_a_actualizar:
            receta_a_actualizar.id_precio = costo_existente.id if costo_existente else nuevo_costo_galleta.id
            db.session.commit()
        else:
            print("Receta no encontrada")

        db.session.commit()
    else:
        flash('No se encontraron detalles de materia prima para calcular el costo de la galleta', 'warning')

def convertirCantidades(tipo1, tipo2, cantidad):
    if (tipo1 == "g" or tipo1 == "ml") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad * 1000
    elif (tipo1 == "kg" or tipo1 == "l") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 1000

    return cantidad