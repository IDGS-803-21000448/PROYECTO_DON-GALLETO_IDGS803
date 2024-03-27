from flask import render_template, request, flash, redirect, url_for
from . import galletas
from controllers.controller_login import requiere_rol
from flask_login import login_required
from models import Receta, RecetaDetalle, MateriaPrima, Tipo_Materia
from formularios import formCosto

@galletas.route("/costoGalleta", methods=["GET"])
@login_required
@requiere_rol("admin")
def costo_galleta():
    galletas = Receta.query.filter_by(estatus=1).all()
    return render_template("moduloGalletas/costoGalleta.html", galletas=galletas)

@galletas.route("/modificarPrecioPagina", methods=["GET", "POST"])
@login_required
@requiere_rol("admin")
def detalle_costo():
    galleta_id = request.form.get('id')
    galleta = Receta.query.filter_by(id=galleta_id).first()

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

    detalles = RecetaDetalle.query.filter_by(receta_id=galleta_id).all()

    galletas = []

    for detalle in detalles:
        materia_prima = Tipo_Materia.query.get(detalle.id)

        if materia_prima:
            detalle_con_nombre = {
                'ingrediente': materia_prima.nombre,
                'cantidad': detalle.cantidad_necesaria,
                'medida': detalle.unidad_medida
            }
            galletas.append(detalle_con_nombre)

    return render_template("moduloGalletas/modificarPrecio.html", galletas=galletas, nombre_galleta=nombre_galleta, id=galleta_id, form=form)
