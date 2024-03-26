from . import recetas
from models import Receta, MateriaPrima, RecetaDetalle
from flask import render_template, request, jsonify
from formularios import formsReceta
import json


@recetas.route("/vistaRecetas", methods=["GET"])
def vista_recetas():
    recetas = Receta.query.all()
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
        ingrediente_nombre = request.form['ingrediente']
        cantidad = request.form['cantidad']
        unidad_medida = request.form['unidad_medida']
        porcentaje_merma = request.form['porcentaje_merma']

        # Verificar que los campos no estén vacíos
        if ingrediente_nombre and cantidad and unidad_medida and porcentaje_merma:
            # Agregar los datos al arreglo ingredientes_data
            ingredientes_data = {
                'ingrediente': ingrediente_nombre,
                'cantidad': cantidad,
                'unidad_medida': unidad_medida,
                'porcentaje_merma': porcentaje_merma
            }

            # Devolver los datos actualizados como respuesta JSON
            return jsonify({'success': True, 'ingredientes_data': ingredientes_data})

    # Si no se pudo agregar o validar los datos, se renderiza la plantilla con el formulario vacío
    return render_template('moduloRecetas/nuevaReceta.html', formReceta=formReceta, materias_primas=materias_primas)


# @recetas.route("/detalleReceta", methods=["GET"])
# def detalle_recetas():
#     formReceta = formsReceta.RecetaForm(request.form)
#     formDetalle = formsReceta.RecetaDetalleForm(request.form)
#     return render_template("moduloRecetas/detalleReceta.html", formReceta = formReceta, formDetalle = formDetalle)

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

        formReceta.ingredientes.data = json.dumps(ingredientes) # Almacena los datos de ingredientes

        # Pasa la receta y los formularios a la plantilla HTML para mostrarlos
        return render_template("moduloRecetas/detalleReceta.html", receta=receta, formReceta=formReceta, ingredientes=ingredientes, materias_primas=materias_primas)
    
    return render_template("404.html"), 404

