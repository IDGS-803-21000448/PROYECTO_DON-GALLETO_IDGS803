from flask import render_template, request, flash, redirect, url_for, flash, jsonify
from modules.dashboard.routes import obtenerCostos
from . import galletas
from controllers.controller_login import requiere_rol, requiere_token
from flask_login import login_required
from models import Receta, RecetaDetalle, MateriaPrima, Tipo_Materia, CostoGalleta, db
from formularios import formCosto
import math
from datetime import datetime
from sqlalchemy import desc
from controllers.controller_costo import actualizar_costos, actualizar_costos_por_id

cantidades = []

@galletas.route("/costoGalleta", methods=["GET", "POST"])
@login_required
@requiere_token
@requiere_rol("admin", "venta")
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
@requiere_token
@requiere_rol("admin", "venta")
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
@requiere_token
@requiere_rol("admin", "venta")
def actualizar_precio():
    galleta_id = request.form.get('id')
    form = formCosto.CalculoCompraForm()
    galleta = Receta.query.filter_by(id=galleta_id).first()
    costos = CostoGalleta.query.filter_by(id=galleta_id).first()
    mano_obra = costos.mano_obra if costos and costos.mano_obra else 0


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

    return render_template("moduloGalletas/modificarPrecio.html", galletas=galletas_det, nombre_galleta=nombre_galleta, id=galleta_id, form=form, mano_obra=mano_obra)

@galletas.route("/detalleCosto", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "venta")
def detalles_costo():
    #Obtenemos los id de los ingredientes de la materia, estos id se envian desde el frontend
    id_materia_lista = request.form.getlist('id_materia[]')
    # Obtenemos el id de la receta a la que le vamos a asignar/modificar el precio
    id_galleta = request.form.get('id')
    #Obtenemos el valor de la mano de obra que ingresó el usuario
    form = formCosto.CalculoCompraForm(request.form)
    # Asignamos a esta variable el valor ingresado por el usuario a mano de obra
    mano_obra = form.precio_mano_obra.data

    if not mano_obra:  # Verificar si mano de obra está vacío
        flash('Por favor, ingrese el costo de mano de obra', 'warning')
        return redirect(url_for('galletas.costo_galleta'))

    #Inicializamos variables
    suma_costos = 0
    cantidad_materias = 0

    # Vamos a recorrer cada id de materia que recibimos del forntend
    for id_materia in id_materia_lista:
        # Buscamos las materias primas que corresponden al id de materia que recibimos
        materias = MateriaPrima.query.filter_by(id_tipo_materia=id_materia, estatus=1).all()

        # Obtenemos el factor de ajuste de la mano de obra
        factor_ajuste_mano_obra = 0.5 

        # Verificar si las materias primas existen
        if materias:
            # Obtener el total de precio de la materia, para esto busca todos los ingredientes de la materia que se han comprado
            # y calcula el total de precio de la materia, es decir, la suma de costo total de todas las veces que se ha comprado la materia
            total_precio_materia = sum(m.precio_compra for m in materias)
            # Obtener el total de cantidades de la materia, para esto busca todos los ingredientes de la materia que se han comprado
            cantidad_materias += len(materias)

            # Puede haber varias compras de la misma materia, por esto, se recorre cada una de ellas a continuación
            for materia in materias:
                # Obtener el id de la materia, lo obtenemos del arreglo que se recibió del frontend
                # Este arreglo es una variable global que llenamos en la función anterior a esta.
                # Contiene el tipo de medida que necesitaa cada ingrediente de la receta
                cantidad_galleta = cantidades[id_materia_lista.index(id_materia)]
                # Obtener los datos del detalle de recetas para obtener algunos de sus campos
                receta_detalle = RecetaDetalle.query.filter_by(receta_id=id_galleta, tipo_materia_id=id_materia).first()
                # Hay materias que se registraron en una medida pero la receta ocupa otra, por tanto, llamamos la función
                # convertirCantidades para convertir la cantidad del ingrediente a la cantidad que originalmente fue registrado
                # dicho ingrediente en materia prima
                # print("DATOS MANUAL")
                # print(f"Materia tipo: {materia.tipo}, Medida de la receta: {receta_detalle.unidad_medida}, cantidad de la galleta: {cantidad_galleta}")
                cantidad_materia = convertirCantidades(materia.tipo, receta_detalle.unidad_medida, cantidad_galleta)

                # Calculamos el precio por kilogramo/litro de cada ingrediente
                precio_por_kg = total_precio_materia / cantidad_materia

                # Aplicar el factor de ajuste a la mano de obra
                costo_mano_obra = mano_obra * factor_ajuste_mano_obra

                # Calcular el costo de los ingredientes utilizados en la receta con el ajuste de la mano de obra
                costo_ingredientes = ((cantidad_materia * precio_por_kg) + costo_mano_obra) / materia.cantidad_compra

                # Sumar el costo de los ingredientes a la suma de costos de la materia
                suma_costos += costo_ingredientes
        else:
            continue

    # Comprobamos que hay materias primas para la receta
    if cantidad_materias > 0:
        # Calcular el promedio del total de todos los ingredientes entre la cantidad de ingredientes registrados
        promedio_costos = suma_costos / cantidad_materias
        # Redondear el promedio del costo al siguiente numero entero, se multiplica por 0.2 para darle una ganancia del 20%
        precio_galleta = math.ceil(promedio_costos * 0.2)

        #Comprobamos que la galleta ya tenga un precio establecido previamente
        costo_existente = CostoGalleta.query.filter_by(id=id_galleta).first()

        # Si la galleta ya tiene un precio establecido previamente, actualizamos el valor de la galleta
        if costo_existente:
            costo_existente.precio = precio_galleta
            costo_existente.mano_obra = mano_obra
            costo_existente.fecha_utlima_actualizacion = datetime.now()
        # Si la galleta no tiene un precio establecido previamente, creamos un nuevo objeto CostoGalleta
        else:
            nuevo_costo_galleta = CostoGalleta(
                id=id_galleta,
                precio=precio_galleta,
                galletas_disponibles=0,
                mano_obra=mano_obra,
                fecha_utlima_actualizacion=datetime.now()
            )
            db.session.add(nuevo_costo_galleta)

        # Actualizar el id_precio de la receta
        receta_a_actualizar = Receta.query.filter_by(id=id_galleta).first()
        if receta_a_actualizar:
            receta_a_actualizar.id_precio = costo_existente.id if costo_existente else nuevo_costo_galleta.id
            db.session.commit()
        else:
            flash('Receta no encontrada', 'warning')

        db.session.commit()
    else:
        pass

    return redirect(url_for('galletas.costo_galleta'))

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


@galletas.route("/act_precios", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "venta")
def act_precios():
    try:
        actualizar_costos()
        return redirect(url_for("galletas.costo_galleta")), 302
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@galletas.route("/act_individual", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "venta")
def act_individual():
    try:
        id_receta = request.form.get('id')

        if id_receta is not None:
            actualizar_costos_por_id(int(id_receta))
            return redirect(url_for("galletas.costo_galleta"))
        else:
            return print({"error": "ID de receta no proporcionado"}), 400
    except Exception as e:
        return print({"error": str(e)}), 500

@galletas.route("/verSugeridos", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "venta")
def verSugeridos():
    try:
        galletas = Receta.query.filter_by(estatus=1).all()
        costos_Receta = obtenerCostos()
        costos_modificados = {}
        for receta in costos_Receta:
            cantidad_galletas = receta[3]
            costo_modificado = list(receta)
            costo_modificado[2] = math.ceil(costo_modificado[2] * 1.20 / cantidad_galletas)
            costos_modificados[receta[0]] = tuple(costo_modificado)
        galletas_arreglo = []
        for galleta in galletas:
            galleta_info = {
                'id': galleta.id,
                'nombre': galleta.nombre,
                'precio': costos_modificados[galleta.id][2]
            }
            galletas_arreglo.append(galleta_info)
        return render_template("moduloGalletas/precioSugerido.html", galletas=galletas_arreglo)
    except Exception as e:
        return print(e)

