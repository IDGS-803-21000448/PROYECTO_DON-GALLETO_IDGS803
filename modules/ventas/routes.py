from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from . import ventas
from formularios import formVenta
from flask import session
from models import Receta, Venta, DetalleVenta, db, CostoGalleta, Turnos, Salidas
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from controllers.controller_login import requiere_rol
from flask_login import login_required, current_user
import datetime

ventas_array = []

@ventas.route("/moduloVenta", methods=["GET"])
@login_required
@requiere_rol("admin")
def modulo_venta():
    form_filtro = formVenta.FiltroVentaForm()
    form_salida = formVenta.SalidaForm()
    form_cerrarTurno = formVenta.CerrarTurnoForm()

    id_turno = request.args.get('turno_id')

    if id_turno:
            # obtener el turno
        turno = Turnos.query.filter_by(id=id_turno).first()

        if not turno:
            flash("No se encontro el turno")
            return redirect(url_for("ventas.turnos"))
        elif turno.estatus != 'En turno':
            flash("El turno ya se cerro")
            return redirect(url_for("ventas.turnos"))
        else:
            salidas = Salidas.query.filter_by(id_turno=id_turno).order_by(Salidas.id.desc()).all()
            ventas = Venta.query.filter_by(id_turno=id_turno).order_by(Venta.id.desc()).all()

            # obtener total de ventas del turno
            total_ventas = 0
            for venta in ventas:
                total_ventas += venta.total

            # obtener total de salidas del turno
            total_salidas = 0
            for salida in salidas:
                total_salidas += salida.cantidad

            fondo_caja = turno.fondo_caja + total_ventas - total_salidas
            return render_template("moduloVentas/vistaVentas.html", ventas=ventas, form_filtro=form_filtro, salidas=salidas, form_salida=form_salida, form_cerrar=form_cerrarTurno, fondo_caja=fondo_caja)
    else:
        # obtener ultimo turno del usuario
        turnoLocalizado = Turnos.query.filter_by(id_usuario=current_user.id).order_by(Turnos.id.desc()).first()

        if turnoLocalizado.estatus == 'En turno':
            return redirect(url_for("ventas.modulo_venta") + f"?turno_id={turnoLocalizado.id}")
        else:
            flash("Debes abrir un turno primero")
            return redirect(url_for("ventas.turnos"))    


@ventas.route("/nuevaVenta", methods=["GET"])
@login_required
@requiere_rol("admin")
def nueva_venta():
    form_venta = formVenta.VentaForm()
    form_venta.sabor.choices = get_sabores()  # Actualiza las opciones del campo sabor
    return render_template("moduloVentas/moduloVenta.html", form=form_venta, ventas=ventas_array)

def get_sabores():
    galletas = Receta.query.filter_by(estatus=1).all()
    sabores = []
    for receta in galletas:
        precio = CostoGalleta.query.filter_by(id=receta.id_precio).first()
        sabores.append(((receta.nombre, precio.id, precio.precio, precio.galletas_disponibles), receta.nombre))

    print(sabores)
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
        total_str = str(primer_venta.get('total'))
        totalVenta = float(total_str.replace('$', ''))

        #en lista venta agrupar y sumar subtotales y cantidades segun su galleta_id
        ventas_agrupadas = {}
        for venta_data in lista_ventas:
            id_galleta = venta_data.get('galleta_id')
            if id_galleta not in ventas_agrupadas:
                ventas_agrupadas[id_galleta] = {'cantidad': 0, 'subtotal': 0, 'sabor': f'{venta_data.get("sabor")}', 'precio_unitario': f'{venta_data.get("precio_unitario")}'}
            ventas_agrupadas[id_galleta]['cantidad'] += float(venta_data.get('cantidad'))
            ventas_agrupadas[id_galleta]['subtotal'] += float(venta_data.get('subtotal').replace('$', ''))

        #validar si hay galletas disponibles segun la cantidad de en ventas_agrupadas
        for id_galleta, datos in ventas_agrupadas.items():
            id_costo = id_galleta
            precio = float(datos.get('precio_unitario'))
            subtotal = float(datos.get('subtotal'))
            cantidadVendida = subtotal / precio
            cantidadStock = CostoGalleta.query.filter_by(id=id_costo).first().galletas_disponibles
            if cantidadVendida >= cantidadStock:
                flash(f'No hay sufucientes galletas de {datos.get("sabor")} en stock', 'error')
                respuesta = {'mensaje': 'Stock', 'galleta': f'{datos.get("sabor")}'}
                return jsonify(respuesta)
            
        # obtener utlimo turno del usuario actual
        ultimo_turno_usuario = Turnos.query.filter_by(id_usuario=current_user.id).order_by(Turnos.id.desc()).first()

        if ultimo_turno_usuario and ultimo_turno_usuario.estatus == 'En turno':
            id_turno = ultimo_turno_usuario.id
        else:
            flash("Debes abrir un turno primero")
            return redirect(url_for("ventas.turnos"))                    

        # Insertar datos en la tabla Venta
        nueva_venta = Venta(
            folio=generar_folio(),
            nombre_cliente=primer_venta.get('nombre'),
            fecha=primer_venta.get("fecha"),
            total=totalVenta,
            id_turno=id_turno
        )

        db.session.add(nueva_venta)
        db.session.commit()

        for venta_data in lista_ventas:
            # Obtener el ID de la venta insertada para usarlo en DetalleVenta
            id_venta_insertada = nueva_venta.id

            #Restar cantidad de galletas en inventario
            id_costo = venta_data.get('galleta_id')
            precio = float(venta_data.get('precio_unitario'))
            subtotal = float(venta_data.get('subtotal').replace('$', ''))

            cantidadVendida = subtotal / precio
            #actualizar la cantidad de galletas_disponibles de la tabla costogalletas
            costo_galletas = CostoGalleta.query.filter_by(id=id_costo).first()
            costo_galletas.galletas_disponibles -= cantidadVendida
            db.session.commit()

            # Insertar datos en la tabla DetalleVenta
            nuevo_detalle = DetalleVenta(
                sabor=venta_data.get('sabor'),
                tipo_venta=venta_data.get('tipoVenta'),
                precio_unitario=float(venta_data.get('precio_unitario')), 
                cantidad=int(venta_data.get('cantidad')),
                subtotal=float(venta_data.get('subtotal').replace('$', '')), 
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

@ventas.route("/turnos", methods=["GET"])
@login_required
def turnos():
    form_turnos = formVenta.TurnoForm()
    id_usuario = current_user.id
    turnos = Turnos.query.filter_by(id_usuario=id_usuario).order_by(Turnos.id).all()
    return render_template("moduloVentas/vistaTurnos.html", turnos=turnos, form_turnos=form_turnos)

@ventas.route("/abrirNuevoTurno", methods=["POST"])
@login_required
@requiere_rol("admin", "venta")
def abrir_nuevo_turno():
    turno_form = formVenta.TurnoForm(request.form)
    id_usuario = current_user.id
    turnos = Turnos.query.filter_by(id_usuario=id_usuario).order_by(Turnos.id).all()

    if turno_form and turno_form.validate():
        #Verificar si hay turnos abiertos
        for turno in turnos:
            if turno.estatus == 'En turno':
                flash("Ya cuentas con un turno abierto")
                return redirect(url_for("ventas.turnos"))
            
        #Abrir turno
        turno = Turnos(id_usuario=id_usuario, fecha=datetime.datetime.now(), estatus='En turno', fondo_caja=float(turno_form.montoInicial.data), venta_total=0, salidas_totales=0, total_final=0)
        db.session.add(turno)
        db.session.commit()

        #obtener el id del ultimo turno agregado
        ultimo_turno_id = Turnos.query.order_by(Turnos.id.desc()).first().id

        response = redirect(url_for("ventas.modulo_venta") + f"?turno_id={ultimo_turno_id}")
        return response
    else:
        flash("Ocurrio un error al abrir turno, el turno debe tener un minimo de $1,000.00 en caja")

    return redirect(url_for("ventas.turnos"))

@ventas.route("/cerrarTurno", methods=["POST"])
@login_required
@requiere_rol("admin", "venta")
def cerrar_turno():
    datos = formVenta.CerrarTurnoForm(request.form)
    print(datos)
    id_turno = int(datos.idTurno.data)

    try:
        # obtener turno
        turno = Turnos.query.filter_by(id=id_turno).first()
        
        # obtener ventas del turno
        ventas = Venta.query.filter_by(id_turno=id_turno).all()

        # obtener salidas del turno
        salidas = Salidas.query.filter_by(id_turno=id_turno).all()

        # obtener total de ventas del turno
        total_ventas = 0
        for venta in ventas:
            total_ventas += venta.total

        # obtener total de salidas del turno
        total_salidas = 0
        for salida in salidas:
            total_salidas += salida.cantidad

        # cerrar turno
        turno.estatus = 'Completado'
        turno.venta_total = total_ventas
        turno.salidas_totales = total_salidas
        turno.total_final = turno.fondo_caja + total_ventas - total_salidas
        db.session.commit()

        return redirect(url_for("ventas.turnos"))
    except Exception as e:
        flash("Ocurrio un error al cerrar el turno")
        return redirect(url_for("ventas.modulo_venta") + f"?turno_id={id_turno}")
    

@ventas.route("/registrarSalidas", methods=["POST"])
@login_required
@requiere_rol("admin", "venta")
def registrar_salidas():
    form_salida = formVenta.SalidaForm(request.form)

    # obtener ultimo turno del usuario
    turnoLocalizado = Turnos.query.filter_by(id_usuario=current_user.id).order_by(Turnos.id.desc()).first()

    if not turnoLocalizado:
        flash("No cuentas con un turno abierto")
        return redirect(url_for("ventas.turnos"))
    elif turnoLocalizado.estatus != 'En turno':
        flash("El turno ya se cerro")
        return redirect(url_for("ventas.turnos"))
    
    if form_salida and form_salida.validate():
        # Verificar si hay turnos abiertos
        if not turnoLocalizado:
            flash("No cuentas con un turno abierto")
            return redirect(url_for("ventas.modulo_venta") + f"?turno_id={turnoLocalizado.id}")
        elif turnoLocalizado.estatus != 'En turno':
            flash("El turno ya se cerro")
            return redirect(url_for("ventas.modulo_venta") + f"?turno_id={turnoLocalizado.id}")
        
        # Registrar salida
        salida = Salidas(id_turno=turnoLocalizado.id, fecha=datetime.datetime.now(), justificacion=form_salida.justificacion.data, cantidad=form_salida.cantidad.data)
        db.session.add(salida)
        db.session.commit()

    return redirect(url_for("ventas.modulo_venta") + f"?turno_id={turnoLocalizado.id}")


