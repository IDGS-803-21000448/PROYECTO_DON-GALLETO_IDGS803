from flask import render_template, request, flash, redirect, url_for
from . import galletas
from controllers.controller_login import requiere_rol, requiere_token
from flask_login import login_required
from models import Receta, RecetaDetalle, MateriaPrima, Tipo_Materia, CostoGalleta, db
from formularios import formCosto
import math
from datetime import datetime

cantidades = []

@galletas.route("/costoGalleta", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin")
def costo_galleta():
    cantidades = []
    galletas = Receta.query.filter_by(estatus=1).all()

    precios_galletas = {}
    costos = CostoGalleta.query.all()
    for costo in costos:
        precios_galletas[costo.id] = costo.precio

    galletas_arreglo = []
    for galleta in galletas:
        galleta_info = {
            'id': galleta.id,
            'nombre': galleta.nombre,
            'precio': precios_galletas.get(galleta.id, 0)
        }
        galletas_arreglo.append(galleta_info)

    return render_template("moduloGalletas/costoGalleta.html", galletas=galletas_arreglo)

@galletas.route("/modificarPrecioPagina", methods=["GET", "POST"])
@login_required
@requiere_rol("admin")
def detalle_costo():
    galleta_id = request.form.get('id')
    galleta = Receta.query.filter_by(id=galleta_id).first()
    cantidades = []

    if not galleta:
        return "Galleta no encontrada", 404

    form = formCosto.CalculoCompraForm()

    form.sabor.data = galleta.nombre

    return render_template("moduloGalletas/modificarPrecio.html", form=form)

@galletas.route("/actualizarPrecio", methods=["GET", "POST"])
@login_required
@requiere_rol("admin")
def actualizar_precio():
    galleta_id = request.form.get('id')
    form = formCosto.CalculoCompraForm()
    galleta = Receta.query.filter_by(id=galleta_id).first()

    if not galleta:
        return "Galleta no encontrada", 404

    nombre_galleta = galleta.nombre

    detalles = RecetaDetalle.query.filter_by(receta_id=galleta.id).all()

    galletas_det = []

    for detalle in detalles:
        materia_prima = Tipo_Materia.query.get(detalle.tipo_materia_id)

        if materia_prima:
            detalle_con_nombre = {
                'id_receta': galleta_id,
                'id_materia': materia_prima.id,
                'ingrediente': materia_prima.nombre,
                'cantidad': detalle.cantidad_necesaria,
                'medida': detalle.unidad_medida
            }
            cantidades.append(detalle.cantidad_necesaria)
            galletas_det.append(detalle_con_nombre)
            print(f"ID Receta: {detalle_con_nombre['id_receta']}, ID Materia: {detalle_con_nombre['id_materia']}, Ingrediente: {detalle_con_nombre['ingrediente']}, Cantidad: {detalle_con_nombre['cantidad']}, Medida: {detalle_con_nombre['medida']}")

    return render_template("moduloGalletas/modificarPrecio.html", galletas=galletas_det, nombre_galleta=nombre_galleta, id=galleta_id, form=form)

@galletas.route("/detalleCosto", methods=["POST"])
@login_required
@requiere_rol("admin")
def detalles_costo():
    id_materia_lista = request.form.getlist('id_materia[]')
    id_galleta = request.form.get('id')
    form = formCosto.CalculoCompraForm(request.form)
    mano_obra = form.precio_mano_obra.data

    materias_primas = []
    suma_costos = 0  # Inicializar la suma de costos
    unidades_recetas_procesadas = set()  # Conjunto para rastrear las unidades de recetas procesadas

    for id_materia in id_materia_lista:
        materia_prima = MateriaPrima.query.filter_by(id_tipo_materia=id_materia).first()

        if materia_prima:
            cantidad_galleta = cantidades[id_materia_lista.index(id_materia)]
            detalles_procesados = set() 

            for detalle_receta in RecetaDetalle.query.filter_by(receta_id=id_galleta).all():
                if detalle_receta not in unidades_recetas_procesadas:
                    unidades_recetas_procesadas.add(detalle_receta)
                    unidad_medida_galleta = detalle_receta.unidad_medida
                    unidad_medida_materia = materia_prima.tipo

                    cantidad_materia = convertirCantidades(unidad_medida_materia, unidad_medida_galleta, cantidad_galleta)

                    detalle_materia_prima = {
                        'id': materia_prima.id,
                        'precio_compra': materia_prima.precio_compra,
                        'cantidad_compra': materia_prima.cantidad_compra,
                        'cantidad_disponible': materia_prima.cantidad_disponible,
                        'fecha_caducidad': materia_prima.fecha_caducidad,
                        'lote': materia_prima.lote,
                        'tipo': materia_prima.tipo,
                        'unidad_receta': unidad_medida_galleta,
                        'costo_ingredientes': (cantidad_materia * materia_prima.precio_compra + mano_obra) / materia_prima.cantidad_compra
                    }

                    if detalle_receta not in detalles_procesados:
                        detalles_procesados.add(detalle_receta)
                        materias_primas.append(detalle_materia_prima)
                        suma_costos += detalle_materia_prima['costo_ingredientes']

    # Calcula el promedio de costos y el precio de la galleta
    promedio_costos = suma_costos / len(materias_primas)
    precio_galleta = math.ceil(promedio_costos * 0.2)
    print(precio_galleta)

    # Verifica si ya existe un registro con el mismo id_precio en la tabla CostoGalleta
    costo_existente = CostoGalleta.query.filter_by(id=id_galleta).first()

    if costo_existente:
        # Si ya existe, actualiza el precio de la galleta en lugar de crear uno nuevo
        costo_existente.precio = precio_galleta
        costo_existente.mano_obra = mano_obra
        costo_existente.fecha_utlima_actualizacion = datetime.now()
    else:
        # Si no existe, crea un nuevo registro en la tabla CostoGalleta
        nuevo_costo_galleta = CostoGalleta(
            id=id_galleta,
            precio=precio_galleta,
            galletas_disponibles=0,
            mano_obra=mano_obra,
            fecha_utlima_actualizacion=datetime.now()
        )
        db.session.add(nuevo_costo_galleta)

    # Actualiza la tabla Recetas con el nuevo id_precio correspondiente
    receta_a_actualizar = Receta.query.filter_by(id=id_galleta).first()
    if receta_a_actualizar:
        receta_a_actualizar.id_precio = costo_existente.id if costo_existente else nuevo_costo_galleta.id
        db.session.commit()
    else:
        print("Receta no encontrada")

    db.session.commit()

    return render_template("moduloGalletas/detalleCosto.html", materias_primas=materias_primas, suma_costos=suma_costos, promedio_costos=promedio_costos)

def convertirCantidades(tipo1, tipo2, cantidad):
    if (tipo1 == "g" or tipo1 == "ml") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad * 1000
    elif (tipo1 == "kg" or tipo1 == "l") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 1000

    return cantidad
