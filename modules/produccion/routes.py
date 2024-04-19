from flask import render_template
from flask import render_template, request, jsonify, url_for, redirect, flash
from models import db, Receta, Produccion, RecetaDetalle, MateriaPrima, MermaMateriaPrima, CostoGalleta, Tipo_Materia
from . import produccion
from controllers.controller_login import requiere_rol, requiere_token
from flask_login import login_required, current_user
from datetime import datetime, date
from sqlalchemy import asc
from controllers.controller_materia_prima import actualizar_cantidades_tipo
from controllers.controller_login import requiere_token

@produccion.route("/produccion", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
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
@requiere_token
@requiere_rol('admin', "produccion")
def solicitar_produccion():
    # Se recupera el id de la solicitud y la receta
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']
    
    # Actualizar el estatus de la solicitud a 'proceso'
    solicitud = Produccion.query.get(id_solicitud)
    solicitud.estatus = 'proceso'
    solicitud.empleadoProduccion = current_user.nombre

    # Recuperar los detalles de la receta
    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
    
    receta = Receta.query.get(receta_id)

    # Actualizar las cantidades de materia prima
    for detalle in detalles_receta:
        # Bandera para verificar si se encontraron suficientes insumos para este detalle
        insumos_suficientes = False
        
        cantidad_necesaria = detalle.cantidad_necesaria
        unidad_origen = detalle.unidad_medida

        # Recuperar las materias primas disponibles ordenadas por fecha de caducidad ascendente
        materias_primas_disponibles = MateriaPrima.query.filter_by(id_tipo_materia=detalle.tipo_materia_id)\
                                                        .order_by(asc(MateriaPrima.fecha_caducidad)).all()

        # Convertir la cantidad necesaria a la unidad de medida de la primera materia prima disponible
        cantidad_restante = convertir_unidades(cantidad_necesaria, unidad_origen, materias_primas_disponibles[0].tipo)
        ids_materias = []
        # Si hay un porcentaje de merma, calcularlo


        # Recorrer las materias primas disponibles hasta encontrar suficiente cantidad
        for materia_prima in materias_primas_disponibles:
            cantidad_disponible = convertir_unidades(materia_prima.cantidad_disponible,
                                                     materia_prima.tipo, materia_prima.tipo)
            ids_materias.append(materia_prima.id)
            # Si la cantidad disponible es suficiente, actualizar y salir del bucle
            if cantidad_disponible >= cantidad_restante:
                materia_prima.cantidad_disponible -= cantidad_restante
                insumos_suficientes = True  # Actualizar la bandera

                break
            else:
                # Si no es suficiente, consumir toda la cantidad disponible y actualizar cantidad restante
                cantidad_restante -= cantidad_disponible
                materia_prima.cantidad_disponible = 0


        # Si no hay suficientes insumos para algún detalle de receta, mostrar mensaje de error y redireccionar
        if not insumos_suficientes:
            flash(f'No hay suficiente cantidad de materia prima para el detalle de receta {detalle.id}.', 'error')
            return redirect(url_for("produccion_blueprint.vista_produccion"))


        # Si hay suficientes insumos, procesar el porcentaje de merma
        merma_porcentaje = 0
        if detalle.merma_porcentaje and detalle.merma_porcentaje != 0:
            porcentaje = detalle.merma_porcentaje / 100
            merma_porcentaje = detalle.cantidad_necesaria * porcentaje
            merma_porcentaje = merma_porcentaje/len(ids_materias)

        if merma_porcentaje != 0:
            for mmateria_id in ids_materias:
                    nueva_merma = MermaMateriaPrima(
                        materia_prima_id=mmateria_id,
                        cantidad=merma_porcentaje,
                        descripcion=f'Merma producida por {detalle.merma_porcentaje}% por producción de la receta de {receta.nombre}',
                        tipo=detalle.unidad_medida,  # investigar qué dato va en esta variable
                        fecha=datetime.now(),
                        estatus=1
                    )
                    db.session.add(nueva_merma)
            
        # Actualizar la cantidad disponible de la materia prima
        tipo_materia = Tipo_Materia.query.get(detalle.tipo_materia_id)
        cantidad_a_restar = convertir_unidades(detalle.cantidad_necesaria, detalle.unidad_medida, tipo_materia.tipo)
        tipo_materia.cantidad_disponible -= cantidad_a_restar

    # Si se completó la iteración sin problemas, entonces todos los detalles de receta tienen suficientes insumos
    # Procesar la solicitud completa
    try:
        db.session.commit()
        actualizar_cantidades_tipo()
        flash('La solicitud de producción se ha procesado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        actualizar_cantidades_tipo()
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
        ('kg', 'pz'): lambda x: (x / 1000)  / 50,
        ('g', 'pz'): lambda x: x /50,
        ('pz', 'g'): lambda x: x * 50,
        ('pz', 'kg'): lambda x: x * 0.050,
        
        
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
@requiere_token
@requiere_rol("admin", "produccion")
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
@requiere_token
@requiere_rol("admin", "produccion")
def terminar_produccion():
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']
    
    # Actualizar el estatus de la solicitud a 'proceso'
    solicitud = Produccion.query.get(id_solicitud)
    solicitud.estatus = 'terminada'
    solicitud.fecha_producido = datetime.now()
    solicitud.lote = "prod-"+date.today().strftime('%d/%m/%Y')+'-'+solicitud.receta.nombre


    # Recuperar los detalles de la receta
    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
    
    receta = Receta.query.get(receta_id)
    
    costo_galleta = CostoGalleta.query.filter_by(id = receta.id_precio).first()
    # for detalle in detalles_receta:
    #     if not detalle.merma_porcentaje or detalle.merma_porcentaje == 0:
    #             print("no hay porcentaje de merma")
    #     else:
    #         porcentaje = detalle.merma_porcentaje / 100
            
    #         merma_porcentaje = (detalle.cantidad_necesaria * porcentaje)
            
    #         nueva_merma = MermaMateriaPrima(
    #             materia_prima_id=detalle.tipo_materia_id,
    #             cantidad = merma_porcentaje,
    #             descripcion = f'Merma producida por {detalle.merma_porcentaje}% de la receta con id {receta_id}',
    #             tipo = detalle.unidad_medida, # investigar qué dato va en esta variable
    #             fecha = datetime.now(),
    #             estatus = 1
    #         )
    #         db.session.add(nueva_merma)
        
    #     tipo_materia = Tipo_Materia.query.get(detalle.tipo_materia_id)
    #     cantidad_a_restar = convertir_unidades(detalle.cantidad_necesaria, detalle.unidad_medida, tipo_materia.tipo)
    #     tipo_materia.cantidad_disponible -= cantidad_a_restar
        
        
    # Actualizar stock de las galletas
    costo_galleta.galletas_disponibles += receta.num_galletas
    solicitud.galletas_disponibles = receta.num_galletas

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
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def cancelar_produccion():
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']

    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'cancelada'
    
    try:
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
        
        for detalle in detalles_receta:
            # Ordenar las materias primas por fecha de caducidad ascendente
            materias_primas = MateriaPrima.query.filter_by(id_tipo_materia=detalle.tipo_materia_id)\
                                                .order_by(MateriaPrima.fecha_caducidad.asc()).all()

            cantidad_a_devolver = convertir_unidades(detalle.cantidad_necesaria, detalle.unidad_medida, materias_primas[0].tipo) if materias_primas else 0

            for materia_prima in materias_primas:
                if cantidad_a_devolver <= 0:
                    break  # Ya se ha devuelto toda la cantidad necesaria

                # Si el lote actual puede aceptar toda la cantidad a devolver, hazlo y termina el proceso
                materia_prima.cantidad_disponible += cantidad_a_devolver
                cantidad_a_devolver = 0  # Ajusta según necesidad real

                db.session.add(materia_prima)  # Asegura que los cambios se preparan para el commit

        db.session.commit()  # Realiza un único commit después de actualizar todas las materias primas
        actualizar_cantidades_tipo()
        flash('La solicitud de producción se ha cancelado correctamente. Se ha regresado la materia prima al inventario.', 'info')
    except Exception as e:
        db.session.rollback()
        actualizar_cantidades_tipo()
        flash(f'Error al regresar la materia prima al inventario. Inténtelo de nuevo más tarde. {e}', 'error')

    return redirect(url_for("produccion_blueprint.vista_produccion"))


@produccion.route("/agregarMerma", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def agregar_merma():
    id_solicitud = request.form['solicitud_id']
    receta_id = request.form['receta_id']
    
    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'merma'
    
    
    # Recuperar los detalles de la receta
    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
    try:
        for detalle in detalles_receta:
            materias_primas = MateriaPrima.query.filter_by(id_tipo_materia=detalle.tipo_materia_id)\
                                                    .order_by(MateriaPrima.fecha_caducidad.asc()).all()
                
            #cantidad_a_merma = convertir_unidades(detalle.cantidad_necesaria, detalle.unidad_medida, materias_primas[0].tipo) if materias_primas else 0

            cantidad_a_merma = detalle.cantidad_necesaria
            
            tipo_materia = Tipo_Materia.query.get(detalle.tipo_materia_id)
            materiaref = MateriaPrima.query.filter_by(id_tipo_materia = tipo_materia.id).all()
            nueva_merma = MermaMateriaPrima(
                materia_prima_id=materiaref[0].id,
                cantidad = cantidad_a_merma,
                descripcion = f' {tipo_materia.nombre} enviado a merma por la solicitud de la receta con id {receta_id}',
                tipo = detalle.unidad_medida, # investigar qué dato va en esta variable
                fecha = datetime.now(),
                estatus = 1
            )
            db.session.add(nueva_merma)
    
        db.session.commit()  # Realiza un único commit después de actualizar todas las materias primas
        actualizar_cantidades_tipo()
        flash('La solicitud de producción se ha enviado a merma correctamente.', 'info')
    except Exception as e:
        db.session.rollback()
        actualizar_cantidades_tipo()
        flash(f'Error al mandar a merma la materia prima al inventario. Inténtelo de nuevo más tarde. {e}', 'error')

    return redirect(url_for("produccion_blueprint.vista_produccion"))
    
    

@produccion.route("/cancelarSolicitud", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def cancelar_solicitud():
    id_solicitud = request.form['solicitud_id']
    
    print(f"Solicitud a cancelar: {id_solicitud}")

    solicitud = Produccion.query.get(id_solicitud)
    
    solicitud.fecha_cancelado = datetime.now()
    solicitud.estatus = 'cancelada'
    
    db.session.commit()
    flash('La solicitud de producción se ha cancelado correctamente.', 'info')
    
    return redirect(url_for("produccion_blueprint.vista_produccion"))
