from flask import render_template
from flask import render_template, request, jsonify, url_for, redirect, flash
from models import db, Receta, Produccion
from . import produccion
from controllers.controller_login import requiere_rol
from flask_login import login_required
from datetime import datetime

@produccion.route("/produccion", methods=["GET"])
@login_required
@requiere_rol("admin")
def vista_produccion():
    recetas = Receta.query.filter_by(estatus=1).all()
    solcitudes = Produccion.query.filter_by(estatus='solicitud').all()
    solicitudes_canceladas = Produccion.query.filter_by(estatus='cancelada').all()
    
    return render_template("moduloProduccion/produccion.html", recetas=recetas, solicitudes=solcitudes, solicitudes_canceladas=solicitudes_canceladas)


@produccion.route("/agregarProduccion", methods=["POST"])
@login_required
@requiere_rol("admin")
def procesar_solicitud():
    
    return redirect(url_for("produccion.vista_produccion"))


@produccion.route("/postergarProduccion", methods=["POST"])
@login_required
@requiere_rol("admin")
def postergar_produccion():
    
    
    return redirect(url_for("produccion.vista_produccion"))

@produccion.route("/cancelarProduccion", methods=["POST"])
@login_required
@requiere_rol("admin")
def cancelar_produccion():
    id_solicitud = request.form['solicitud_id']
    
    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'cancelada'
    db.session.commit()
    
    return redirect(url_for("produccion_blueprint.vista_produccion"))