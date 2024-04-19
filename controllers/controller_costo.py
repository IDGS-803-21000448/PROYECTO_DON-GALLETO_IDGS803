import math
import models
from models import *
from datetime import datetime
from flask import flash, redirect, url_for, Flask
from sqlalchemy import desc
from modules.dashboard.routes import obtenerCostos

def actualizar_costos():
    # Obtenemos todas las recetas con estatus 1
    recetas = models.Receta.query.filter_by(estatus=1).all()
    recetas_id = [receta.id for receta in recetas]
    costos = obtenerCostos()
    id = 0

    for idx, costo in enumerate(costos):
        id = recetas_id[idx]
        insertar_costos(id, costo[2])

def actualizar_costos_por_id(receta_id):
    id = receta_id
    costos = obtenerCostos()
    cos = 0.0

    for i in costos:
        if i[0] == id:
            cos = i[2]
    insertar_costos(id, cos)

def insertar_costos(receta_id, costo):
    # Verificamos que haya materias primas
    rec = Receta.query.get(receta_id)

    precio_galleta = math.ceil(costo * 1.20 / rec.num_galletas)

    # Comprobamos que la galleta ya tenga un precio establecido previamente
    costo_existente = CostoGalleta.query.filter_by(id=receta_id).first()

    # Si la galleta ya tiene un precio establecido previamente, actualizamos el valor de la galleta
    if costo_existente:
        costo_existente.precio = precio_galleta
        costo_existente.mano_obra = 0
        costo_existente.fecha_utlima_actualizacion = datetime.now()
        db.session.commit()  # Guardar los cambios en la base de datos
    # Si la galleta no tiene un precio establecido previamente, creamos un nuevo objeto CostoGalleta
    else:
        nuevo_costo_galleta = CostoGalleta(
            id=receta_id,
            precio=precio_galleta,
            galletas_disponibles=0,
            mano_obra=0,
            fecha_utlima_actualizacion=datetime.now()
        )
        db.session.add(nuevo_costo_galleta)
        db.session.commit()  # Guardar los cambios en la base de datos

        # Actualizar el id_precio de la receta
        receta_a_actualizar = Receta.query.filter_by(id=receta_id).first()
        if receta_a_actualizar:
            receta_a_actualizar.id_precio = nuevo_costo_galleta.id
            db.session.commit()
        else:
            print("Receta no encontrada")

def convertirCantidades(tipo1, tipo2, cantidad):
    if (tipo1 == "g" or tipo1 == "ml") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad * 1000
    elif (tipo1 == "kg" or tipo1 == "l") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 1000
    elif(tipo1 == "pz") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad / 1000
        cantidad = cantidad / 50
    elif(tipo1 == "pz") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 50
    elif(tipo1 == "g" or tipo1 == "ml") and (tipo2 == "pz"):
        cantidad = cantidad * 50
    elif(tipo1 == "kg" or tipo1 == "l") and (tipo2 == "pz"):
        cantidad = cantidad * 0.050

    return cantidad