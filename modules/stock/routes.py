from . import stock
from flask import render_template, request
from controllers.controller_login import requiere_rol
from flask_login import login_required
from controllers.controller_login import requiere_token
from models import db, CostoGalleta, Receta
import math


@stock.route('/moduloStock')
@login_required
@requiere_token
@requiere_rol('admin', "inventario", "produccion", "venta")
def modulo_stock():
    # Consulta para obtener nombre de galletas y id_precio de Receta
    recetas_con_precio = db.session.query(Receta.nombre, Receta.id_precio).filter(Receta.id_precio.isnot(None), Receta.estatus==1).all()

    galletas = []

    for nombre_galleta, id_precio in recetas_con_precio:
        costo_galleta = CostoGalleta.query.filter_by(id=id_precio).first()
        if costo_galleta:
            # obtiene la cantidad de galletas que hay en 700 gramos
            cantidad_700_gramos = math.ceil(700 / 30.0)
            print(cantidad_700_gramos)

            # obtiene la cantidad de galletas que hay en 1000 gramos
            cantidad_1000_gramos = math.ceil(1000 / 30.0)
            print(cantidad_1000_gramos)

            # calcula el precio por cantidad de galletas en 700 gramos con un descuento del 10%
            precio_700_gramos = math.ceil((costo_galleta.precio * cantidad_700_gramos) * 0.9)
            print(precio_700_gramos)

            # calcula el precio por cantidad de galletas en 1000 gramos con descuento de 15%
            precio_1000_gramos = math.ceil((costo_galleta.precio * cantidad_1000_gramos) * 0.85)
            print(precio_1000_gramos)

            galletas.append({
                'nombre': nombre_galleta,
                'cantidad_disponible': costo_galleta.galletas_disponibles,
                'precio_unitario': costo_galleta.precio, 
                'precio_pkt_700': precio_700_gramos,
                'precio_pkt_1000': precio_1000_gramos
            })

    return render_template('moduloStock/vistaStock.html', galletas=galletas)