from flask import render_template, request, redirect, url_for, flash, jsonify
from . import ventas
from formularios import formVenta
from flask import session
from models import Receta, Venta, DetalleVenta, db
import random

ventas_array = []

@ventas.route("/moduloVenta", methods=["GET"])
def modulo_venta():
    form_venta = formVenta.VentaForm()
    form_venta.sabor.choices = get_sabores()  # Actualiza las opciones del campo sabor
    return render_template("moduloVentas/moduloVenta.html", form=form_venta, ventas=ventas_array)

def get_sabores():
    sabores = [(receta.nombre, receta.nombre) for receta in Receta.query.filter_by(estatus=1).all()]
    return sabores

@ventas.route("/realizarVenta", methods=["POST"])
def realizar_venta():
    datos = request.json

    if datos and 'ventas' in datos and isinstance(datos['ventas'], list) and len(datos['ventas']) > 0:
        lista_ventas = datos['ventas']
        id_venta_insertada = None
        primer_venta = lista_ventas[0]

        # Insertar datos en la tabla Venta
        nueva_venta = Venta(
            folio=generar_folio(),
            nombre_cliente=primer_venta.get('nombre'),
            fecha=primer_venta.get("fecha"),
            total=500.0,
        )
        db.session.add(nueva_venta)
        db.session.commit()

        for venta_data in lista_ventas:
            # Obtener el ID de la venta insertada para usarlo en DetalleVenta
            id_venta_insertada = nueva_venta.id

            # Insertar datos en la tabla DetalleVenta
            nuevo_detalle = DetalleVenta(
                sabor=venta_data.get('sabor'),
                tipo_venta=venta_data.get('tipoVenta'),
                precio_unitario=10.0, 
                cantidad=venta_data.get('cantidad'),
                subtotal=100.0, 
                venta_id=id_venta_insertada 
            )
            db.session.add(nuevo_detalle)
            db.session.commit()

        respuesta = {'mensaje': 'Correcto'}
    else:
        respuesta = {'mensaje': 'Incorrecto'}

    return jsonify(respuesta)

def generar_folio():
    folio_existente = True
    while folio_existente:
        nuevo_folio = f"DGT-{random.randint(1000, 9999)}"
        # Verificar si el folio generado ya existe en la base de datos
        if not Venta.query.filter_by(folio=nuevo_folio).first():
            folio_existente = False
    return nuevo_folio

