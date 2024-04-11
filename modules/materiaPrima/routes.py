from controllers.controller_materia_prima import actualizar_cantidades_tipo
from formularios import formMateriaPrima
from . import materia_prima
from flask import render_template, request, flash, redirect, url_for
import models
from models import db, Tipo_Materia
from controllers.controller_login import requiere_rol
from flask_login import login_required
from controllers.controller_login import requiere_token

@materia_prima.route("/moduloMateriaPrima", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario")
def modulo_materia_prima():
    form = formMateriaPrima.MateriaPrimaForm()
    listado_materias = Tipo_Materia.query.filter_by(estatus=1).all()
    return render_template("moduloMateria/moduloMateria.html", form=form,
                           materias_primas=listado_materias)


@materia_prima.route("/agregarMateriaPrima", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario")
def agregar_materia():
    form = formMateriaPrima.MateriaPrimaForm(request.form)
    listado_materias = Tipo_Materia.query.filter_by(estatus=1).all()
    if form.validate():
        if form.id.data == 0:
            nuevaMateria= models.Tipo_Materia(
                    nombre = form.nombre.data,
                    cantidad_disponible = form.cantidad.data,
                    tipo = form.tipo.data
            )
            db.session.add(nuevaMateria)
        else:
            materia = Tipo_Materia.query.get_or_404(form.id.data )
            materia.nombre = form.nombre.data
            materia.cantidad_disponible = form.cantidad.data
            materia.tipo = form.tipo.data

        db.session.commit()
        actualizar_cantidades_tipo()
        return redirect(url_for('materiaPrima.modulo_materia_prima'))

    return render_template("moduloMateria/moduloMateria.html", form=form,
                           materias_primas=listado_materias)


@materia_prima.route('/seleccionarMateria', methods=['GET', 'POST'])
@login_required
@requiere_token
@requiere_rol("admin", "inventario")
def seleccionar_materia():
    id = request.form['id']
    originalForm = formMateriaPrima.MateriaPrimaForm()
    materias_primas = Tipo_Materia.query.filter_by(estatus=1).all()
    if request.method == 'POST':
        materia = Tipo_Materia.query.get_or_404(id)
        originalForm.id.data = materia.id
        originalForm.nombre.data = materia.nombre
        originalForm.tipo.data = materia.tipo
        originalForm.cantidad.data = materia.cantidad_disponible
        flash('Materia prima seleccionado correctamente', 'success')
    return render_template('moduloMateria/moduloMateria.html',
                           form=originalForm, materias_primas=materias_primas)

@materia_prima.route('/eliminarMateria', methods=['POST'])
@login_required
@requiere_token
@requiere_rol("admin", "inventario")
def eliminar_materia():
    id = request.form['id']
    materia = Tipo_Materia.query.get_or_404(id)
    if materia.cantidad_disponible > 0:
        flash("No se puede eliminar una materia prima con inventario activo")
        return redirect(url_for('materiaPrima.modulo_materia_prima'))
    materia.estatus = 0
    db.session.commit()
    flash('Materia Prima eliminada correctamente', 'success')
    return redirect(url_for('materiaPrima.modulo_materia_prima'))