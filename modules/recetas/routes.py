from . import recetas
from models import Receta, MateriaPrima, RecetaDetalle
from flask import render_template, request, jsonify, url_for, redirect, flash
from formularios import formsReceta

from werkzeug.utils import secure_filename
import base64
from models import db
import json


@recetas.route("/vistaRecetas", methods=["GET"])
def vista_recetas():
    recetas = Receta.query.filter_by(estatus=1).all()
    return render_template("moduloRecetas/vistaRecetas.html", recetas=recetas)

@recetas.route("/crudRecetas", methods=["GET"])
def crud_recetas():
    return render_template("moduloRecetas/crudRecetas.html")

@recetas.route('/nuevaReceta', methods=['GET', 'POST'])
def nueva_receta():
    formReceta = formsReceta.RecetaForm(request.form)
    #formDetalle = formsReceta.RecetaDetalleForm()

    # Obtén la lista de ingredientes desde la tabla MateriaPrima
    materias_primas = MateriaPrima.query.all()

    if request.method == 'POST' and formReceta.validate():
        return redirect(url_for('recetas.detalle_recetas'))

    return render_template('moduloRecetas/nuevaReceta.html', formReceta=formReceta, materias_primas=materias_primas)

@recetas.route("/guardarReceta", methods=["POST"])
def guardar_receta():
    if request.method == "POST":
        # Obtener los datos del formulario de la receta
        nombre = request.form['nombre']
        num_galletas = request.form['num_galletas']
        fecha = request.form['fecha']
        # Obtener la imagen (en base64 o como prefieras manejarla)
        imagen = request.files['imagen']
        descripcion = request.form['descripcion']

        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)

            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

        # Aquí puedes realizar la lógica para guardar la receta en la base de datos
        # Por ejemplo:
        nueva_receta = Receta(nombre=nombre, num_galletas=num_galletas, create_date=fecha, imagen=imagen_base64, descripcion=descripcion)
        db.session.add(nueva_receta)
        db.session.commit()

        # Redirigir a la página de vista de recetas después de guardar la receta
        return redirect(url_for('recetas.vista_recetas'))

    return render_template("404.html"), 404

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recetas.route("/detalleReceta", methods=["GET", "POST"])
def detalle_recetas():
    formReceta = formsReceta.RecetaForm(request.form)
    #formDetalle = formsReceta.RecetaDetalleForm(request.form)

    materias_primas = MateriaPrima.query.all()
    print(materias_primas)
    
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
            materia_prima = MateriaPrima.query.filter_by(id=ingrediente.materia_prima_id).first()

            ingredientes.append({
                'ingrediente_id': materia_prima.id,
                'ingrediente': materia_prima.nombre,
                'cantidad': ingrediente.cantidad_necesaria,
                'unidad_medida': ingrediente.unidad_medida,
                'porcentaje_merma': float(ingrediente.merma_porcentaje)
            })

        print(ingredientes)
        formReceta.ingredientes.data = json.dumps(ingredientes) # Serializa los ingredientes

        # Pasa la receta y los formularios a la plantilla HTML para mostrarlos
        return render_template("moduloRecetas/detalleReceta.html", receta=receta, formReceta=formReceta, materias_primas=materias_primas, ingredientes=ingredientes)
    
    return render_template("404.html"), 404

@recetas.route("/editarReceta", methods=["POST"])
def editar_receta():
    if request.method == "POST":
        if 'guardar_receta_btn' in request.form:
            # Obtener los datos del formulario de la receta
            receta_id = request.form['receta_id']
            nombre = request.form['nombre']
            num_galletas = request.form['num_galletas']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']

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
            db.session.commit()
        return redirect(url_for('recetas.vista_recetas'))
    return render_template("404.html"), 404

@recetas.route("/eliminarReceta", methods=["POST"])
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
