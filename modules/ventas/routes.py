from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from . import ventas
from formularios import formVenta
from flask import session
from models import Receta, Venta, DetalleVenta, db
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from controllers.controller_login import requiere_rol
from flask_login import login_required

ventas_array = []

@ventas.route("/moduloVenta", methods=["GET"])
@login_required
@requiere_rol("admin")
def modulo_venta():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("moduloVentas/vistaVentas.html", ventas=ventas)

@ventas.route("/nuevaVenta", methods=["GET"])
@login_required
@requiere_rol("admin")
def nueva_venta():
    form_venta = formVenta.VentaForm()
    form_venta.sabor.choices = get_sabores()  # Actualiza las opciones del campo sabor
    return render_template("moduloVentas/moduloVenta.html", form=form_venta, ventas=ventas_array)

def get_sabores():
    sabores = [(receta.nombre, receta.nombre) for receta in Receta.query.filter_by(estatus=1).all()]
    return sabores

@ventas.route("/realizarVenta", methods=["POST"])
@login_required
@requiere_rol("admin")
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

@ventas.route("/generarTicket", methods=["GET"])
@login_required
@requiere_rol("admin")
def generar_ticket():
    folio = request.args.get('folio')

    if not folio:
        return jsonify({'error': 'Folio no especificado'})

    # Obtener los datos de la venta y los detalles correspondientes
    venta = Venta.query.filter_by(folio=folio).first()
    detalles = DetalleVenta.query.filter_by(venta_id=venta.id).all()

    response = make_response()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={folio}.pdf'

    # Crear el PDF
    p = canvas.Canvas(response.stream, pagesize=letter)
    
    # Encabezado
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(4.25 * inch, 10 * inch, "GALLETOSAURIO S.A. de C.V.")
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(4.25 * inch, 9.7 * inch, "Ticket de Compra")

    p.setFont("Helvetica", 10)
    p.drawString(0.5 * inch, 9.3 * inch, f"Fecha: {venta.fecha.strftime('%d/%m/%Y')}")
    p.drawString(5.5 * inch, 9.3 * inch, f"Folio: {venta.folio}")
    p.drawString(0.5 * inch, 8.9 * inch, f"Nombre del Cliente: {venta.nombre_cliente}")

    # Línea de separación
    p.line(0.5 * inch, 8.7 * inch, 7.5 * inch, 8.7 * inch)

    # Encabezados de columna
    p.drawString(0.5 * inch, 8.5 * inch, "Cantidad")
    p.drawString(2 * inch, 8.5 * inch, "Producto")
    p.drawString(3.5 * inch, 8.5 * inch, "Precio Unitario")
    p.drawString(5.5 * inch, 8.5 * inch, "Subtotal")

    # Detalles de la Compra
    y = 8.2 * inch
    for detalle in detalles:
        p.drawString(0.5 * inch, y, f"{detalle.cantidad} {detalle.tipo_venta}")
        p.drawString(2 * inch, y, f"{detalle.sabor}")  # Asumiendo que hay un nombre en el producto
        p.drawString(3.5 * inch, y, f"${detalle.precio_unitario:.2f}")
        p.drawString(5.5 * inch, y, f"${detalle.subtotal:.2f}")
        y -= 0.3 * inch

    # Línea de separación antes del total
    p.line(0.5 * inch, y + 0.15 * inch, 7.5 * inch, y + 0.15 * inch)

    # Total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(0.5 * inch, y - 0.5 * inch, "TOTAL:") # Separación aumentada aquí
    p.drawString(5.5 * inch, y - 0.5 * inch, f"${venta.total:.2f}")

    # Agradecimiento
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(2.5 * inch, y - 0.8 * inch, "GRACIAS POR SU COMPRA :)") # Separación aumentada aquí

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response
