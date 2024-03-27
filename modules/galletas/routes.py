from flask import render_template, request, flash, redirect, url_for
from . import galletas
from controllers.controller_login import requiere_rol
from flask_login import login_required
from models import Receta, RecetaDetalle, MateriaPrima, Tipo_Materia
from formularios import formCosto

cantidades = []

@galletas.route("/costoGalleta", methods=["GET"])
@login_required
@requiere_rol("admin")
def costo_galleta():
    cantidades = []
    galletas = Receta.query.filter_by(estatus=1).all()
    return render_template("moduloGalletas/costoGalleta.html", galletas=galletas)

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

    detalles = RecetaDetalle.query.filter_by(receta_id=galleta_id).all()

    galletas = []

    for detalle in detalles:
        materia_prima = Tipo_Materia.query.get(detalle.id)

        if materia_prima:
            detalle_con_nombre = {
                'id_materia': materia_prima.id,
                'ingrediente': materia_prima.nombre,
                'cantidad': detalle.cantidad_necesaria,
                'medida': detalle.unidad_medida
            }
            cantidades.append(detalle.cantidad_necesaria)
            galletas.append(detalle_con_nombre)

    return render_template("moduloGalletas/modificarPrecio.html", galletas=galletas, nombre_galleta=nombre_galleta, id=galleta_id, form=form)

# @galletas.route("/detalleCosto", methods=["POST"])
# @login_required
# @requiere_rol("admin")
# def detalles_costo():
#     id_materia_lista = request.form.getlist('id_materia[]')

#     materias_primas = []

#     for id_materia in id_materia_lista:
#         materia_prima = MateriaPrima.query.filter_by(id_tipo_materia=id_materia).first()

#         if materia_prima:
#             detalle_materia_prima = {
#                 'id': materia_prima.id,
#                 'precio_compra': materia_prima.precio_compra,
#                 'cantidad_disponible': materia_prima.cantidad_disponible,
#                 'fecha_caducidad': materia_prima.fecha_caducidad,
#                 'lote': materia_prima.lote
#             }
#             materias_primas.append(detalle_materia_prima)
#         else:
#             return f"Materia prima con ID {id_materia} no encontrada", 404

#     return render_template("moduloGalletas/detalleCosto.html", materias_primas=materias_primas)

@galletas.route("/detalleCosto", methods=["POST"])
@login_required
@requiere_rol("admin")
def detalles_costo():
    id_materia_lista = request.form.getlist('id_materia[]')
    id_galleta = request.form.get('id')
    galleta = Receta.query.filter_by(id=id_galleta).first()
    num_galletas = galleta.num_galletas
    form = formCosto.CalculoCompraForm(request.form)
    mano_obra = form.precio_mano_obra.data

    materias_primas = []

    for index, id_materia in enumerate(id_materia_lista):
        materia_prima = MateriaPrima.query.filter_by(id_tipo_materia=id_materia).first()

        if materia_prima:
            detalle_materia_prima = {
                'id': materia_prima.id,
                'precio_compra': materia_prima.precio_compra,
                'cantidad_disponible': materia_prima.cantidad_disponible,
                'fecha_caducidad': materia_prima.fecha_caducidad,
                'lote': materia_prima.lote,
                'costo_ingredientes': (((cantidades[index] * materia_prima.precio_compra) + mano_obra) / materia_prima.cantidad_disponible) / num_galletas
            }
            print(f"ID de materia prima: {materia_prima.id}, Cantidad disponible: {materia_prima.cantidad_disponible}, Precio de compra: {materia_prima.precio_compra}, Cantidades: {cantidades[index]}, Costo ingredientes por galleta: {detalle_materia_prima['costo_ingredientes']}, Mano de Obra: {mano_obra}")
            materias_primas.append(detalle_materia_prima)
        else:
            return f"Materia prima con ID {id_materia} no encontrada", 404

    return render_template("moduloGalletas/detalleCosto.html", materias_primas=materias_primas)