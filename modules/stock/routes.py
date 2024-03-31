from . import stock
from flask import render_template, request
from controllers.controller_login import requiere_rol
from flask_login import login_required
from controllers.controller_login import requiere_token
from models import db, CostoGalleta, Receta


@stock.route('/moduloStock')
@login_required
@requiere_token
def modulo_stock():
    # Consulta para obtener nombre de galletas y id_precio de Receta
    recetas_con_precio = db.session.query(Receta.nombre, Receta.id_precio).filter(Receta.id_precio.isnot(None)).all()

    galletas = []

    for nombre_galleta, id_precio in recetas_con_precio:
        costo_galleta = CostoGalleta.query.filter_by(id=id_precio).first()
        if costo_galleta:
            galletas.append({
                'nombre': nombre_galleta,
                'cantidad_disponible': costo_galleta.galletas_disponibles
            })

    return render_template('moduloStock/vistaStock.html', galletas=galletas)