from datetime import datetime
from controllers import controller_costo
from . import recetas
from models import Receta, MateriaPrima, RecetaDetalle, Tipo_Materia, CostoGalleta, Alerta
from flask import render_template, request, jsonify, url_for, redirect, flash
from formularios import formsReceta
from controllers.controller_login import requiere_rol
from flask_login import login_required
from controllers.controller_login import requiere_token

from werkzeug.utils import secure_filename
import base64
from models import db
import json


@recetas.route("/vistaRecetas", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def vista_recetas():
    recetas = Receta.query.filter_by(estatus=1).all()
    return render_template("moduloRecetas/vistaRecetas.html", recetas=recetas)

@recetas.route("/crudRecetas", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def crud_recetas():
    return render_template("moduloRecetas/crudRecetas.html")

@recetas.route('/nuevaReceta', methods=['GET', 'POST'])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def nueva_receta():
    formReceta = formsReceta.RecetaForm(request.form)
    #formDetalle = formsReceta.RecetaDetalleForm()

    # Obtén la lista de ingredientes desde la tabla Tipo_Materia
    materias_primas = Tipo_Materia.query.all()

    if request.method == 'POST' and formReceta.validate():
        return redirect(url_for('recetas.detalle_recetas'))

    return render_template('moduloRecetas/nuevaReceta.html', formReceta=formReceta, materias_primas=materias_primas)

@recetas.route("/guardarReceta", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def guardar_receta():
    if request.method == "POST":
        # Obtener los datos del formulario de la receta
        nombre = request.form['nombre']
        num_galletas = request.form['num_galletas']
        fecha = request.form['fecha']
        # Obtener la imagen (en base64 o como prefieras manejarla)
        imagen = request.files['imagen']
        descripcion = request.form['descripcion']
        # Obtener los ingredientes
        ingredientesRaw = request.form['ingredientes']
        ingredientesJson = json.loads(ingredientesRaw)

        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)

            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

        # Aquí puedes realizar la lógica para guardar la receta en la base de datos
        # Por ejemplo:
        nueva_receta = Receta(nombre=nombre, num_galletas=num_galletas, create_date=fecha, imagen=imagen_base64, descripcion=descripcion)
        nuevo_costo_galleta = CostoGalleta(
                precio=0,
                galletas_disponibles=0,
                mano_obra=0,
                fecha_utlima_actualizacion=datetime.now()
            )
        
        
        db.session.add(nuevo_costo_galleta)
        db.session.add(nueva_receta)
        db.session.commit()

        # Obtener el ID del nuevo costo de galleta
        id_precio = nuevo_costo_galleta.id
        last_receta = Receta.query.order_by(Receta.id.desc()).first()
        last_receta.id_precio = id_precio
        db.session.commit()

        # Obtener el detalle de la receta guardada
        lastDetalles = RecetaDetalle.query.filter_by(receta_id=last_receta.id).all()

        #verificar si lastDetalles tiene elementos, si tiene datos realizar lo siguiente
        if lastDetalles:
            # Verificar si en el ingredientesJson no hay un id de ingrediente registrado en el lastDetalles, si es asi debe eliminarlo de la base de datos donde el id de receta y el id de materia prima coincidan
            for detalle in lastDetalles:
                if not any(ingrediente['id'] == detalle.tipo_materia_id for ingrediente in ingredientesJson):
                    db.session.delete(detalle)
                    db.session.commit()        

        # Crear los detalles de la receta
        for ingrediente in ingredientesJson:
            detalle = RecetaDetalle(
                receta_id=last_receta.id,
                tipo_materia_id=ingrediente['ingrediente_id'],
                cantidad_necesaria=ingrediente['cantidad'],
                unidad_medida=ingrediente['unidad_medida'],
                merma_porcentaje=ingrediente['porcentaje_merma']
            )
            # Verificar si la receta ya tiene detalles
            if lastDetalles:                
                # Verificar si el detalle ya existe en la base de datos
                existe = next((x for x in lastDetalles if x.tipo_materia_id == ingrediente['id']), None)

                # Si el detalle ya existe solo modificar datos en la base de datos donde el id de ingrediente y el id de receta coincidan
                if existe:
                    existe.cantidad_necesaria = ingrediente['cantidad']
                    existe.unidad_medida = ingrediente['unidaddemedida']
                    existe.merma_porcentaje = ingrediente['mermaporcentaje']
                    db.session.commit()
                # Si el detalle no existe, agregarlo a la base de datos
                else:
                    db.session.add(detalle)                    
            else:
                db.session.add(detalle)
                db.session.commit()

        # Llamar a actualizar_costos_por_id solo si se está insertando una nueva receta
        controller_costo.actualizar_costos_por_id(last_receta.id)

        # Redirigir a la página de vista de recetas después de guardar la receta
        return redirect(url_for('recetas.vista_recetas'))

    return render_template("404.html"), 404

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png','jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recetas.route("/detalleReceta", methods=["GET", "POST"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def detalle_recetas():
    formReceta = formsReceta.RecetaForm(request.form)
    #formDetalle = formsReceta.RecetaDetalleForm(request.form)

    materias_primas = Tipo_Materia.query.all()
    
    # Verificar si se envió el formulario y se presionó el botón "Limpiar Campos"
    if request.method == "POST" and request.form.get("limpiar_campos"):
        formReceta.nombre.data = ''
        formReceta.num_galletas.data = ''
        formReceta.fecha.data = None
        formReceta.descripcion.data = ''
        return render_template("moduloRecetas/detalleReceta.html", receta=None, formReceta=formReceta, ingredientes=[], materias_primas=materias_primas)
    
    # Resto de tu lógica para manejar el formulario cuando no se presiona "Limpiar Campos"
    if request.method == "POST":
        receta_id = request.form.get("receta_id")
        receta = Receta.query.filter_by(id=receta_id).first()
        formReceta.nombre.data = receta.nombre
        formReceta.num_galletas.data = receta.num_galletas
        formReceta.fecha.data = receta.create_date
        formReceta.descripcion.data = receta.descripcion
        formReceta.imagen.data = receta.imagen

        ingredientesReceta = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
        
        ingredientes = []

        for ingrediente in ingredientesReceta:
            materia_prima = Tipo_Materia.query.filter_by(id=ingrediente.tipo_materia_id).first()

            ingredientes.append({
                'ingrediente_id': materia_prima.id,
                'ingrediente': materia_prima.nombre,
                'cantidad': ingrediente.cantidad_necesaria,
                'unidad_medida': ingrediente.unidad_medida,
                'porcentaje_merma': float(ingrediente.merma_porcentaje)
            })

        formReceta.ingredientes.data = json.dumps(ingredientes) # Serializa los ingredientes

        # Pasa la receta y los formularios a la plantilla HTML para mostrarlos
        return render_template("moduloRecetas/detalleReceta.html", receta=receta, formReceta=formReceta, materias_primas=materias_primas, ingredientes=ingredientes)
    
    return render_template("404.html"), 404

@recetas.route("/editarReceta", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def editar_receta():
    if request.method == "POST":
        if 'guardar_receta_btn' in request.form:
            # Obtener los datos del formulario de la receta
            receta_id = request.form['receta_id']
            nombre = request.form['nombre']
            num_galletas = request.form['num_galletas']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']
            ingredientesRaw = request.form['ingredientes']
            ingredientesJson = json.loads(ingredientesRaw)

            # Verificar si se seleccionó una nueva imagen
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen and allowed_file(imagen.filename):
                    filename = secure_filename(imagen.filename)
                    imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

                    # Actualizar la receta con la nueva imagen
                    receta = Receta.query.get(receta_id)
                    receta.nombre = nombre
                    receta.num_galletas = num_galletas
                    receta.create_date = fecha
                    receta.imagen = imagen_base64
                    receta.descripcion = descripcion

                    db.session.commit()

                    # Redirigir a la página de vista de recetas después de guardar la receta
                    return redirect(url_for('recetas.vista_recetas'))

            # Si no se seleccionó una nueva imagen, actualizar solo los otros campos
            receta = Receta.query.get(receta_id)
            receta.nombre = nombre
            receta.num_galletas = num_galletas
            receta.create_date = fecha
            receta.descripcion = descripcion
            nuevaAlerta = Alerta(
            nombre="Modificación de receta",
            descripcion="Se hizo una modificación de receta, los precios podrían haber cambiado.",
            estatus=0
            )      
            db.session.add(nuevaAlerta)
            db.session.commit()

            #last_receta = Receta.query.order_by(Receta.id.desc()).first()

            # Obtener el detalle de la receta guardada
            #lastDetalles = RecetaDetalle.query.filter_by(receta_id=last_receta.id).all()

            lastDetalles = RecetaDetalle.query.filter_by(receta_id=receta_id).all()
            #verificar si lastDetalles tiene elementos, si tiene datos realizar lo siguiente
            if lastDetalles:
                # Verificar si en el ingredientesJson no hay un id de ingrediente registrado en el lastDetalles, si es asi debe eliminarlo de la base de datos donde el id de receta y el id de materia prima coincidan
                for detalle in lastDetalles:
                    if not any(int(ingrediente['ingrediente_id']) == int(detalle.tipo_materia_id) for ingrediente in ingredientesJson):
                            db.session.delete(detalle)
                            db.session.commit()        

            # Crear los detalles de la receta
            for ingrediente in ingredientesJson:
                detalle = RecetaDetalle(
                    receta_id=receta_id,
                    tipo_materia_id=ingrediente['ingrediente_id'],
                    cantidad_necesaria=ingrediente['cantidad'],
                    unidad_medida=ingrediente['unidad_medida'],
                    merma_porcentaje=ingrediente['porcentaje_merma']
                )
                # Verificar si la receta ya tiene detalles
                if lastDetalles:                
                    # Verificar si el detalle ya existe en la base de datos
                    existe = next((x for x in lastDetalles if x.tipo_materia_id == ingrediente['ingrediente_id']), None)

                    # Si el detalle ya existe solo modificar datos en la base de datos donde el id de ingrediente y el id de receta coincidan
                    if existe:
                        existe.cantidad_necesaria = ingrediente['cantidad']
                        existe.unidad_medida = ingrediente['unidad_medida']
                        existe.merma_porcentaje = ingrediente['porcentaje_merma']
                        db.session.commit()      
                    # Si el detalle no existe, agregarlo a la base de datos
                    else:
                        db.session.add(detalle)     
                        db.session.commit()
                else:
                    db.session.add(detalle)
                    db.session.commit()
        return redirect(url_for('recetas.vista_recetas'))
    return render_template("404.html"), 404

@recetas.route("/eliminarReceta", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "produccion")
def eliminar_receta():
    if request.method == "POST":
        print(request.form)
        id = request.form['id'] 
        receta = Receta.query.get(id)  
        if receta:
            receta.estatus = 0 
            db.session.commit() 
            flash('Receta eliminada exitosamente', 'success')
            return redirect(url_for('recetas.vista_recetas'))
        else:
            flash('Receta no encontrada', 'error')
            return redirect(url_for('recetas.vista_recetas'))

    return render_template("404.html"), 404
