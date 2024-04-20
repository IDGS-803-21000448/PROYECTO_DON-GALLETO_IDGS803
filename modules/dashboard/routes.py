from flask import render_template, session
from sqlalchemy import func

from . import dashboard
from flask_login import login_required, current_user
from controllers.controller_login import requiere_token
from models import LogLogin, Alerta, CostoGalleta, Receta, RecetaDetalle, MateriaPrima, MemraGalleta, db, Produccion, \
    DetalleVenta, Proveedor, Venta, Salidas, Turnos, Tipo_Materia
import json
from datetime import datetime, timedelta
from sqlalchemy import func

from collections import OrderedDict
from sqlalchemy.orm import sessionmaker

receta_mayor_ganancia = None
costo_menor = float('inf')

@dashboard.route("/dashboard", methods=["GET"])
@login_required
@requiere_token
def dashboard():
    # obtener logs de inicio de sesión correctos del usuario
    logs = LogLogin.query.filter_by(id_user=current_user.id, estatus='correcto').order_by(LogLogin.id.desc()).limit(2).all()
    mermas_mayor = obtenerMayorMerma()
    merma_porcentaje = obtenerMermaPorcentaje()
    costos_galletas = obtenerCostos()
    datos_presentaciones = obtenerPresentación()
    galletas_vendias = obtenerGalletasMasVendidas()
    proveedores_por_lote = obtener_proveedores_por_lote()
    ventas_salidas = ventas_salidas_por_semana()
    # obtener el segundo ultimo log de inicio de sesion correcto del usuario
    if len(logs) > 1:
        # regresar lastSession en formato dd/mm/yyyy hh:mm:ss
        lastSession = logs[1].fecha.strftime("%d/%m/%Y %H:%M:%S")
    else:
        lastSession = None
    alertas = Alerta.query.filter_by(estatus = 0).all()
    session['countAlertas'] = len(alertas)
    return render_template("moduloDashboard/dashboard.html", lastSession=lastSession, costos_galletas=costos_galletas, menor_costo=receta_mayor_ganancia, merma_mayor=mermas_mayor, merma_porcentaje = merma_porcentaje, datos_presentaciones = datos_presentaciones, galletas_vendias = galletas_vendias, proveedores_por_lote = proveedores_por_lote, ventas_salidas = ventas_salidas)


def obtenerPresentación():
    result = db.session.query(
        DetalleVenta.tipo_venta,
        func.count('*').label('cant_vendida')
    ).group_by( DetalleVenta.tipo_venta)

    resultados_serializables = []
    for nombre, total_merma in result:
        resultados_serializables.append((nombre, total_merma))

    return resultados_serializables

def obtenerMayorMerma():
    result = db.session.query(
        Receta.nombre,
        func.sum(MemraGalleta.cantidad).label('total_merma')
    ).join(
        Produccion, MemraGalleta.produccion_id == Produccion.id
    ).join(
        Receta, Produccion.receta_id == Receta.id
    ).group_by(
        Receta.nombre
    ).order_by(
        func.sum(MemraGalleta.cantidad).desc()
    ).all()
    resultados_serializables = []
    for nombre, total_merma in result:

        resultados_serializables.append((nombre, total_merma))

    return resultados_serializables


def obtenerMermaPorcentaje():
    cantidad_producciones_subq = db.session.query(
        Receta.id.label('id_receta'),
        func.count('*').label('cantidad_producciones')
    ).join(
        Produccion, Produccion.receta_id == Receta.id
    ).group_by(
        Receta.id
    ).subquery()

    result = db.session.query(
        Receta.nombre,
        (func.sum(MemraGalleta.cantidad) * 100) / (
                    func.max(cantidad_producciones_subq.c.cantidad_producciones) * func.max(
                Receta.num_galletas)).label('porcentaje_merma')
    ).join(
        Produccion, MemraGalleta.produccion_id == Produccion.id
    ).join(
        Receta, Produccion.receta_id == Receta.id
    ).join(
        cantidad_producciones_subq, Receta.id == cantidad_producciones_subq.c.id_receta
    ).group_by(
        Receta.nombre
    ).all()

    resultados_serializables = []
    for nombre, total_merma in result:
        resultados_serializables.append((nombre, total_merma))

    return resultados_serializables

def obtenerCostos():
    global receta_mayor_ganancia, costo_menor
    # Lista para almacenar los costos de recetas
    costos_recetas = []
    ganancia_mayor = 0

    # Obtenemos todas las recetas con estatus 1
    recetas = Receta.query.filter_by(estatus=1).all()

    # Vamos a recorrer todas las recetas
    for receta in recetas:
        # Obtener los detalles de la receta
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id).all()
        # Obtener los IDs de los ingredientes de la receta seleccionada
        ids_ingredientes = [detalle.tipo_materia_id for detalle in detalles_receta]
        # Obtener los costos de la receta y sus detalles
        costos = CostoGalleta.query.filter_by(id=receta.id).first()
        factor_ajuste_mano_obra = 0.5  # Factor de ajuste para la mano de obra

        # Inicializar variables
        suma_costos = 0
        cantidad_materias = 0
        costo_mano_obra = 0

        # Realizar la consulta de Materias Prima para cada ID de ingrediente
        for id_ingrediente in ids_ingredientes:
            # Obtener las materias primas que corresponden al ID de ingrediente
            materias = MateriaPrima.query.filter_by(id_tipo_materia=id_ingrediente, estatus=1).all()

            # Si las materias primas existen
            if materias:
                # Obtener el total de precio de la materia
                total_precio_materia = sum(m.precio_compra for m in materias)
                # Obtener el total de cantidades de la materia
                cantidad_materias += len(materias)

                # Puede haber varias compras de la misma materia
                for materia in materias:
                    # Obtenemos el detalle de receta de la receta que estamos iterando
                    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id, tipo_materia_id=id_ingrediente).first()
                    cantidad_materia = convertirCantidades(materia.tipo, detalles_receta.unidad_medida, detalles_receta.cantidad_necesaria)

                    # Calcular el precio por kilogramo/litro
                    precio_por_kg = total_precio_materia / cantidad_materia

                    # Aplicar el factor de ajuste a la mano de obra
                    if costos.mano_obra is None:
                        # Manejar el caso en que el valor de mano_obra sea None, por default será 100
                        mano_obra = costos.mano_obra = 100
                    else:
                        mano_obra = costos.mano_obra

                    # asignamos el factor de ajuste de la mano de obra
                    costo_mano_obra = mano_obra * factor_ajuste_mano_obra

                    # Calcular el costo de los ingredientes
                    costo_ingredientes = ((cantidad_materia * precio_por_kg) + costo_mano_obra) / materia.cantidad_compra

                    # Agregar el costo de la materia a la suma de costos
                    suma_costos += costo_ingredientes

        # Calcular el costo promedio de la receta
        costo_receta = round(suma_costos / cantidad_materias, 2)

        # Calcular la ganancia esperada por cada receta
        precio_pz = costos.precio
        galletas_por_receta = receta.num_galletas
        ganancia_esperada = precio_pz * galletas_por_receta
        ganancia = ganancia_esperada - costo_receta

        # Actualizar la receta de mayor ganancia si corresponde
        if ganancia > ganancia_mayor:
            receta_mayor_ganancia = receta.nombre
            ganancia_mayor = ganancia

        # Guardar el costo de la receta junto con su nombre en la lista
        costos_recetas.append((receta.id, receta.nombre, costo_receta, receta.num_galletas))

    return costos_recetas

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


def obtenerGalletasMasVendidas():
    recetas = Receta.query.filter_by(estatus=1).all()
    detalle_venta = DetalleVenta.query.all()

    galletas_mas_vendidas = {}

    for detalle in detalle_venta:
        if detalle.receta_id:
            receta_id = detalle.receta_id
            cantidad_galletas = detalle.cantidad_galletas
            receta_nombre = Receta.query.filter_by(id=receta_id).first().nombre

            if receta_id in galletas_mas_vendidas:
                galletas_mas_vendidas[receta_id]["cantidad"] += cantidad_galletas
            else:
                galletas_mas_vendidas[receta_id] = {
                    "nombre": receta_nombre,
                    "cantidad": cantidad_galletas
                }

    return galletas_mas_vendidas
    

def obtener_proveedores_por_lote():
    producciones = Produccion.query.filter_by(estatus='terminada').all()
    lista_proveedores_por_lote = []

    for produccion in producciones:
        proveedores_lote = set()  # Usamos un conjunto para evitar duplicados de proveedores en un mismo lote
        
        receta_detalles = RecetaDetalle.query.filter_by(receta_id=produccion.receta_id).all()
        
        for receta_detalle in receta_detalles:
            materia_prima = MateriaPrima.query.filter_by(id=receta_detalle.tipo_materia_id).first()
            
            if materia_prima:
                proveedor = Proveedor.query.filter_by(id=materia_prima.id_proveedor).first()
                
                if proveedor:
                    ingrediente = Tipo_Materia.query.filter_by(id=materia_prima.id_tipo_materia).first()
                    if ingrediente:
                        proveedores_lote.add((proveedor.nombre, ingrediente.nombre))  # Tupla (nombre_proveedor, nombre_ingrediente)
        
        lista_proveedores_por_lote.append({
            'id_produccion': produccion.id,
            'lote': produccion.lote,
            'proveedores': list(proveedores_lote)  # Convertir el conjunto a una lista para poder ser serializado
        })
    
    return lista_proveedores_por_lote

def ventas_salidas_por_semana():    
    # Obtener la fecha y hora actual
    current_datetime = datetime.now()

    # Establecer el primer día de la semana (0=Monday, 6=Sunday)
    first_week_day = 0  # Cambiar esto según sea necesario

    # Calcular el inicio de la semana basado en el día de inicio elegido
    days_to_start = (current_datetime.weekday() - first_week_day) % 7
    start_of_week = current_datetime - timedelta(days=days_to_start)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calcular el fin de la semana como seis días después del inicio
    end_of_week = start_of_week + timedelta(days=6)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Obtener los turnos de la semana actual
    turnos = Turnos.query.filter(Turnos.fecha.between(start_of_week, end_of_week)).all()

    # Diccionario ordenado para almacenar las ventas y salidas por día de la semana
    dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ventas_por_semana = {dia: {'total_final': 0, 'salidas_totales': 0, 'fondo_caja': 0, 'venta_total': 0} for dia in dias}

    # Verificar los turnos y agruparlos por día de la semana y sumar total_final y salidas_totales
    for turno in turnos:
        dia_semana = turno.fecha.strftime('%A')
        ventas_por_semana[dia_semana]['total_final'] += turno.total_final
        ventas_por_semana[dia_semana]['salidas_totales'] += turno.salidas_totales
        ventas_por_semana[dia_semana]['fondo_caja'] = turno.fondo_caja
        ventas_por_semana[dia_semana]['venta_total'] += turno.venta_total

    return ventas_por_semana

