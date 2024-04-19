import math
import models
from models import *
from datetime import datetime
from flask import flash, redirect, url_for, Flask
from sqlalchemy import desc

def actualizar_costos():
    # Obtenemos todas las recetas con estatus 1
    recetas = models.Receta.query.filter_by(estatus=1).all()

    # Vamos a recorrer todas las recetas
    for receta in recetas:
        # Obtener los detalles de la receta
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id).all()
        # Obtener los IDs de los ingredientes de la receta seleccionada
        ids_ingredientes = [detalle.tipo_materia_id for detalle in detalles_receta]
        # Obtener los costos de la receta y sus detalles
        costos = models.CostoGalleta.query.filter_by(id=receta.id_precio).first()
            
        factor_ajuste_mano_obra = 0.5  # Factor de ajuste para la mano de obra

        # Inicializar variables
        suma_costos = 0
        cantidad_materias = 0
        costo_mano_obra = 0

        # Realizar la consulta de Materias Prima para cada ID de ingrediente
        for id_ingrediente in ids_ingredientes:
            # Obtener las materias primas que corresponden al ID de ingrediente
            materias = MateriaPrima.query.filter_by(id_tipo_materia=id_ingrediente, estatus=1).all()

            # Si las materias primas existen
            if materias:
                # Obtener el total de precio de la materia
                total_precio_materia = sum(m.precio_compra for m in materias)
                # Obtener el total de cantidades de la materia
                cantidad_materias += len(materias)

                # Puede haber varias compras de la misma materia
                for materia in materias:
                    # Obtenemos el detalle de receta de la receta que estamos iterando
                    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id, tipo_materia_id=id_ingrediente).first()
                    # print("DATOS AUTOMATICO")
                    # print(f"Materia tipo: {materia.tipo}, Medida de la receta: {detalles_receta.unidad_medida}, cantidad de la galleta: {detalles_receta.cantidad_necesaria}")
                    cantidad_materia = convertirCantidades(materia.tipo, detalles_receta.unidad_medida, detalles_receta.cantidad_necesaria)

                    # Calcular el precio por kilogramo/litro
                    precio_por_kg = total_precio_materia / cantidad_materia

                    # Aplicar el factor de ajuste a la mano de obra
                    if costos.mano_obra is None:
                        # Manejar el caso en que el valor de mano_obra sea None, por default será 100
                        mano_obra = costos.mano_obra = 100
                    else:
                        mano_obra = costos.mano_obra

                    # asignamos el factor de ajuste de la mano de obra
                    costo_mano_obra = mano_obra * factor_ajuste_mano_obra

                    # Calcular el costo de los ingredientes
                    costo_ingredientes = ((cantidad_materia * precio_por_kg) + costo_mano_obra) / materia.cantidad_compra

                    # Agregar el costo de la materia a la suma de costos
                    suma_costos += costo_ingredientes

        # Insertar los costos calculados
        insertar_costos(cantidad_materias, suma_costos, receta.id, costos.mano_obra)

def actualizar_costos_por_id(receta_id):
    # Obtener los detalles de la receta
    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
    # Obtener los IDs de los ingredientes de la receta seleccionada
    ids_ingredientes = [detalle.tipo_materia_id for detalle in detalles_receta]
    # Obtener los costos de la receta y sus detalles
    costos = models.CostoGalleta.query.filter_by(id=receta_id).first()

    # Inicializar variables
    suma_costos = 0
    cantidad_materias = 0

    # Realizar la consulta de Materias Prima para cada ID de ingrediente
    for id_ingrediente in ids_ingredientes:
        # Obtener las materias primas que corresponden al ID de ingrediente
        materias = MateriaPrima.query.filter_by(id_tipo_materia=id_ingrediente, estatus=1).all()

        # Si las materias primas existen
        if materias:
            # Obtener el total de precio de la materia
            total_precio_materia = sum(m.precio_compra for m in materias)
            # Obtener el total de cantidades de la materia
            cantidad_materias += len(materias)

            # Puede haber varias compras de la misma materia
            for materia in materias:
                # Obtenemos el detalle de receta de la receta que estamos iterando
                detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id, tipo_materia_id=id_ingrediente).first()
                # print("DATOS AUTOMATICO")
                # print(f"Materia tipo: {materia.tipo}, Medida de la receta: {detalles_receta.unidad_medida}, cantidad de la galleta: {detalles_receta.cantidad_necesaria}")
                cantidad_materia = convertirCantidades(materia.tipo, detalles_receta.unidad_medida, detalles_receta.cantidad_necesaria)

                # Calcular el precio por kilogramo/litro
                precio_por_kg = total_precio_materia / cantidad_materia

                # Calcular el costo de los ingredientes
                costo_ingredientes = ((cantidad_materia * precio_por_kg)) / materia.cantidad_compra

                # Agregar el costo de la materia a la suma de costos
                suma_costos += costo_ingredientes

    # Insertar los costos calculados
    insertar_costos(cantidad_materias, suma_costos, receta_id, costos.mano_obra)

def insertar_costos(cantidad_materias, suma_costos, receta_id, costo_mano_obra):
    # Verificamos que haya materias primas
    rec = Receta.query.get(receta_id)
    if cantidad_materias > 0:
        # Calcular el promedio del total de todos los ingredientes entre la cantidad de ingredientes registrados
        promedio_costos = suma_costos / rec.num_galletas
        # Redondear el promedio del costo al siguiente numero entero, se multiplica por 0.2 para darle una ganancia del 20%
        precio_galleta = math.ceil(promedio_costos * 0.2)

        #Comprobamos que la galleta ya tenga un precio establecido previamente
        costo_existente = CostoGalleta.query.filter_by(id=receta_id).first()

        # Si la galleta ya tiene un precio establecido previamente, actualizamos el valor de la galleta
        if costo_existente:
            costo_existente.precio = precio_galleta
            costo_existente.mano_obra = costo_mano_obra
            costo_existente.fecha_utlima_actualizacion = datetime.now()
        # Si la galleta no tiene un precio establecido previamente, creamos un nuevo objeto CostoGalleta
        else:
            nuevo_costo_galleta = CostoGalleta(
                id=receta_id,
                precio=precio_galleta,
                galletas_disponibles=0,
                mano_obra=costo_mano_obra,
                fecha_utlima_actualizacion=datetime.now()
            )
            db.session.add(nuevo_costo_galleta)

        # Actualizar el id_precio de la receta
        receta_a_actualizar = Receta.query.filter_by(id=receta_id).first()
        if receta_a_actualizar:
            receta_a_actualizar.id_precio = costo_existente.id if costo_existente else nuevo_costo_galleta.id
            db.session.commit()
        else:
            print("Receta no encontrada")

        db.session.commit()
    else:
        pass

def verCostosSugerencias():
    # Obtenemos todas las recetas con estatus 1
    recetas = models.Receta.query.filter_by(estatus=1).all()
    costos_sug = []

    # Vamos a recorrer todas las recetas
    for receta in recetas:
        # Obtener los detalles de la receta
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id).all()
        # Obtener los IDs de los ingredientes de la receta seleccionada
        ids_ingredientes = [detalle.tipo_materia_id for detalle in detalles_receta]
        # Obtener los costos de la receta y sus detalles
        costos = models.CostoGalleta.query.filter_by(id=receta.id).first()
            
        factor_ajuste_mano_obra = 0.5  # Factor de ajuste para la mano de obra

        # Inicializar variables
        suma_costos = 0
        cantidad_materias = 0
        costo_mano_obra = 0

        # Realizar la consulta de Materias Prima para cada ID de ingrediente
        for id_ingrediente in ids_ingredientes:
            # Obtener las materias primas que corresponden al ID de ingrediente
            materias = MateriaPrima.query.filter_by(id_tipo_materia=id_ingrediente, estatus=1).all()

            # Si las materias primas existen
            if materias:
                # Obtener el total de precio de la materia
                total_precio_materia = sum(m.precio_compra for m in materias)
                # Obtener el total de cantidades de la materia
                cantidad_materias += len(materias)

                # Puede haber varias compras de la misma materia
                for materia in materias:
                    # Obtenemos el detalle de receta de la receta que estamos iterando
                    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id, tipo_materia_id=id_ingrediente).first()
                    cantidad_materia = convertirCantidades(materia.tipo, detalles_receta.unidad_medida, detalles_receta.cantidad_necesaria)

                    # Calcular el precio por kilogramo/litro
                    precio_por_kg = total_precio_materia / cantidad_materia

                    # Aplicar el factor de ajuste a la mano de obra
                    if costos.mano_obra is None:
                        # Manejar el caso en que el valor de mano_obra sea None, por default será 100
                        mano_obra = costos.mano_obra = 100
                    else:
                        mano_obra = costos.mano_obra

                    # asignamos el factor de ajuste de la mano de obra
                    costo_mano_obra = mano_obra * factor_ajuste_mano_obra

                    # Calcular el costo de los ingredientes
                    costo_ingredientes = ((cantidad_materia * precio_por_kg) + costo_mano_obra) / materia.cantidad_compra

                    # Agregar el costo de la materia a la suma de costos
                    suma_costos += costo_ingredientes

        # Insertar los costos calculados
        costos_sug.extend(costos_sugeridos(cantidad_materias, suma_costos, receta.id, costos.mano_obra))

    return costos_sug

def costos_sugeridos(cantidad_materias, suma_costos, receta_id, mano_obra):
    # Verificamos que haya materias primas
    costos = []
    rec = Receta.query.get(receta_id)
    if cantidad_materias > 0:
        # Calcular el promedio del total de todos los ingredientes entre la cantidad de ingredientes registrados
        promedio_costos = suma_costos / rec.num_galletas
        # Redondear el promedio del costo al siguiente numero entero, se multiplica por 0.2 para darle una ganancia del 20%
        precio_galleta = math.ceil(promedio_costos * 0.2)
        costos.append(precio_galleta)

    return costos


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