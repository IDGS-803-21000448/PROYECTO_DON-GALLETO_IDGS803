from flask import render_template
from flask import render_template, request, jsonify, url_for, redirect, flash
from models import db, Receta, Produccion, RecetaDetalle, MateriaPrima, MermaMateriaPrima, CostoGalleta
from . import produccion
from controllers.controller_login import requiere_rol
from flask_login import login_required
from datetime import datetime
from sqlalchemy import asc

@produccion.route("/produccion", methods=["GET"])
@login_required
@requiere_rol("admin")
def vista_produccion():
    recetas = Receta.query.filter_by(estatus=1).all()
    solicitudes = Produccion.query.filter_by(estatus='solicitud').all()
    solicitudes_en_proceso = Produccion.query.filter_by(estatus='proceso').all()
    solicitudes_canceladas = Produccion.query.filter_by(estatus='cancelada').all()
    solicitudes_postergadas = Produccion.query.filter_by(estatus='postergada').all()
    
    return render_template("moduloProduccion/produccion.html", recetas=recetas, solicitudes=solicitudes, solicitudes_en_proceso=solicitudes_en_proceso, 
                           solicitudes_canceladas=solicitudes_canceladas, solicitudes_postergadas=solicitudes_postergadas)


@produccion.route('/solicitarProduccion', methods=['POST'])
@login_required
@requiere_rol('admin')
def solicitar_produccion():
    # Se recupera el id de la solicitud y la receta
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']
    
    # Actualizar el estatus de la solicitud a 'proceso'
    solicitud = Produccion.query.get(id_solicitud)
    solicitud.estatus = 'proceso'
    
    # Recuperar los detalles de la receta
    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
    
    receta = Receta.query.get(receta_id)
        

    # Actualizar las cantidades de materia prima
    for detalle in detalles_receta:
        
        
        cantidad_necesaria = detalle.cantidad_necesaria
        unidad_origen = detalle.unidad_medida

        # Recuperar las materias primas disponibles ordenadas por fecha de caducidad ascendente
        materias_primas_disponibles = MateriaPrima.query.filter_by(id_tipo_materia=detalle.tipo_materia_id)\
                                                        .order_by(asc(MateriaPrima.fecha_caducidad)).all()

        # Convertir la cantidad necesaria a la unidad de medida de la primera materia prima disponible
        cantidad_restante = convertir_unidades(cantidad_necesaria, unidad_origen, materias_primas_disponibles[0].tipo)

        # Recorrer las materias primas disponibles hasta encontrar suficiente cantidad
        for materia_prima in materias_primas_disponibles:
            cantidad_disponible = convertir_unidades(materia_prima.cantidad_disponible,
                                                     materia_prima.tipo, materia_prima.tipo)

            # Si la cantidad disponible es suficiente, actualizar y salir del bucle
            if cantidad_disponible >= cantidad_restante:
                materia_prima.cantidad_disponible -= cantidad_restante
                break
            else:
                # Si no es suficiente, consumir toda la cantidad disponible y actualizar cantidad restante
                cantidad_restante -= cantidad_disponible
                materia_prima.cantidad_disponible = 0

        # Manejar caso donde no hay suficiente materia prima
        if cantidad_restante > 0:
            #flash(f'No hay suficiente cantidad de materia prima para el detalle de receta {detalle.id}.', 'error')
            continue

    # Actualizar stock de las galletas
    

    # Realizar el commit de todas las actualizaciones de la materia prima
    try:
        db.session.commit()
        flash('La solicitud de producción se ha procesado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al procesar la solicitud de producción. Inténtelo de nuevo más tarde.', 'error')
        #current_app.logger.error(f'Error al procesar la solicitud de producción: {str(e)}')

    return redirect(url_for("produccion_blueprint.vista_produccion"))
    


def convertir_unidades(cantidad, unidad_origen, unidad_destino):
    print(f"Convirtiendo {cantidad} {unidad_origen} a {unidad_destino}")
    conversiones = {
        ('g', 'kg'): lambda x: x / 1000,
        ('kg', 'g'): lambda x: x * 1000,
        ('ml', 'l'): lambda x: x / 1000,
        ('l', 'ml'): lambda x: x * 1000,
    }
    
    if unidad_origen == unidad_destino:
        return cantidad

    if (unidad_origen, unidad_destino) in conversiones:
        resultado = conversiones[(unidad_origen, unidad_destino)](cantidad)
        print(f"Resultado: {resultado}")
        return resultado
    else:
        print("Las unidades de medida no son compatibles")




@produccion.route("/postergarProduccion", methods=["POST"])
@login_required
@requiere_rol("admin")
def postergar_produccion():
    id_solicitud = request.form['solicitud_id']

    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'postergada'
    
    db.session.commit()  # Aquí se realiza el commit en el objeto de sesión db.session
    flash('La solicitud de producción se ha postergado correctamente.', 'info')
    
    return redirect(url_for("produccion_blueprint.vista_produccion"))


@produccion.route("/terminarProduccion", methods=["POST"])
@login_required
@requiere_rol("admin")
def terminar_produccion():
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']
    
    # Actualizar el estatus de la solicitud a 'proceso'
    solicitud = Produccion.query.get(id_solicitud)
    solicitud.estatus = 'terminada'
    solicitud.fecha_producido = datetime.now()
    
    # Recuperar los detalles de la receta
    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
    
    receta = Receta.query.get(receta_id)
    
    costo_galleta = CostoGalleta.query.filter_by(precio = receta.id_precio).first()
    for detalle in detalles_receta:
        if not detalle.merma_porcentaje or detalle.merma_porcentaje == 0:
                print("no hay porcentaje de merma")
        else:
            porcentaje = detalle.merma_porcentaje / 100
            
            merma_porcentaje = (detalle.cantidad_necesaria * porcentaje)
            
            nueva_merma = MermaMateriaPrima(
                materia_prima_id=detalle.tipo_materia_id,
                cantidad = merma_porcentaje,
                descripcion = f'Merma producida por {detalle.merma_porcentaje}% de la receta con id {receta_id}',
                tipo = detalle.unidad_medida, # investigar qué dato va en esta variable
                fecha = datetime.now(),
                estatus = 1
            )
            db.session.add(nueva_merma)
    # Actualizar stock de las galletas
    costo_galleta.galletas_disponibles += receta.num_galletas

    # Realizar el commit de todas las actualizaciones de la materia prima
    try:
        db.session.commit()
        flash('La solicitud de producción se ha terminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al terminar la solicitud de producción. Inténtelo de nuevo más tarde.', 'error')
        #current_app.logger.error(f'Error al procesar la solicitud de producción: {str(e)}')

    return redirect(url_for("produccion_blueprint.vista_produccion"))

from sqlalchemy import asc

@produccion.route("/cancelarProduccion", methods=["POST"])
@requiere_rol("admin")
def cancelar_produccion():
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']

    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'cancelada'
    
    try:
        # Obtener los detalles de la solicitud
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
        
        # Regresar la materia prima a la receta
        for detalle in detalles_receta:
            materia_prima = MateriaPrima.query.filter_by(id_tipo_materia=detalle.tipo_materia_id).first()
            if materia_prima is not None:
                # Convertir la cantidad necesaria a la unidad de medida de la materia prima
                cantidad_necesaria = convertir_unidades(detalle.cantidad_necesaria, detalle.unidad_medida, materia_prima.tipo)
                materia_prima.cantidad_disponible += cantidad_necesaria
                db.session.commit()
        
        db.session.commit()
        flash('La solicitud de producción se ha cancelado correctamente. Se ha regresado la materia prima a la receta.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error al regresar la materia prima a la receta. Inténtelo de nuevo más tarde.', 'error')
        #current_app.logger.error(f'Error al regresar la materia prima a la receta: {str(e)}')

    return redirect(url_for("produccion_blueprint.vista_produccion"))



@produccion.route("/cancelarSolicitud", methods=["POST"])
@requiere_rol("admin")
def cancelar_solicitud():
    id_solicitud = request.form['solicitud_id']

    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'cancelada'
    
    db.session.commit()
    flash('La solicitud de producción se ha cancelado correctamente.', 'info')
    
    return redirect(url_for("produccion_blueprint.vista_produccion"))
