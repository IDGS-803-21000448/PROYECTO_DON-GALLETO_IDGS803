from . import solicitud_produccion
from flask import render_template, request, jsonify, url_for, redirect, flash
#from formularios import formSolicitudProduccion
from controllers.controller_login import requiere_rol
from flask_login import login_required, current_user
from models import db, Receta, Produccion
import json
from datetime import datetime
from controllers.controller_login import requiere_token


@solicitud_produccion.route("/solicitudProduccion", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "venta", "produccion")
def vista_recetas():
    recetas = Receta.query.filter_by(estatus=1).all()
    solcitudes = Produccion.query.all()

    return render_template("moduloProduccion/solicitudProduccion.html", recetas=recetas, solicitudes=solcitudes)

@solicitud_produccion.route("/agregarSolicitud", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "venta", "produccion")
def agregar_solicitud():
    # id_receta = request.form.get("receta_id")
    id_receta = request.form['receta_id']

    receta = Receta.query.get(id_receta)
    if not receta or receta.id_precio is None:
        flash('La receta no tiene precio, debe asignar un precio antes de procesar la solicitud.', 'error')
        return redirect(url_for("solicitudProduccion.vista_recetas"))

    nueva_solicitud = Produccion(
        receta_id=id_receta,
        estatus='solicitud',
        cantidad=1, # Este dato falta por confirmar qué es
        fecha_solicitud=datetime.now(),
        fecha_producido=None,
        fecha_postergado=None,
        empleadoSolicitante = current_user.nombre
    )
    
    db.session.add(nueva_solicitud)
    db.session.commit()
    flash("Solicitud de producción agregada", "info")

    return redirect(url_for("solicitudProduccion.vista_recetas"))
