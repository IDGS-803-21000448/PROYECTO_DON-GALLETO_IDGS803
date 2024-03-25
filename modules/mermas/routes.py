import json

from flask import render_template, request, flash, redirect, url_for

from controllers import controller_mermas
from models import MermaMateriaPrima, db, MemraGalleta, MateriaPrima
from . import mermas
from formularios.formsMerma import MermaMateriaPrimaForm, tipoMermaForm


# /mermas

@mermas.route("/merma_galletas", methods=["GET"])
def merma_galletas():
    form = tipoMermaForm()
    originalForm = MermaMateriaPrimaForm()
    mermas = MemraGalleta.query.filter_by(estatus=1)
    originalForm.tipo_merma.data = "galletas"
    form.tipo_merma.data = "galletas"
    recetas = []
    materiasPrimas = []

    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                           formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)


@mermas.route("/merma_materia_prima", methods=["GET"])
def merma_materia_prima():
    form = tipoMermaForm()
    originalForm = MermaMateriaPrimaForm()
    mermas = MermaMateriaPrima.query.filter_by(estatus=1)
    originalForm.tipo_merma.data = "materiaPrima"
    form.tipo_merma.data = "materiaPrima"
    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
    recetas = []

    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                           formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)

@mermas.route("/moduloMermas", methods=["POST", "GET"])
def modulo_mermas():
    form = tipoMermaForm(request.form)
    if request.method == "POST" and form.validate():
        tipo_merma = form.tipo_merma.data
        if tipo_merma == "materiaPrima":
            return redirect(url_for('mermas.merma_materia_prima'))
        else:
            return redirect(url_for('mermas.merma_galletas'))
    else:
        return redirect(url_for('mermas.merma_materia_prima'))


@mermas.route("/agregarMerma", methods=["GET", "POST"])
def agregar_merma():
    form = MermaMateriaPrimaForm(request.form)
    if request.method == "POST" and form.validate():

        if form.tipo_merma.data == "materiaPrima":
            nueva_merma = MermaMateriaPrima(
                materia_prima_id=form.materia_prima_id.data,
                tipo=form.tipo.data,
                cantidad=form.cantidad.data,
                descripcion=form.descripcion.data,
                fecha=form.fecha.data
            )
        else:
            nueva_merma = MemraGalleta(
                receta_id=form.materia_prima_id.data,
                tipo=form.tipo.data,
                cantidad=form.cantidad.data,
                descripcion=form.descripcion.data,
                fecha=form.fecha.data
            )
        if form.id.data != 0:
            merma = MermaMateriaPrima.query.get_or_404(form.id.data)
            merma.materia_prima_id = form.materia_prima_id.data,
            merma.tipo = form.tipo.data,
            merma.cantidad = form.cantidad.data,
            merma.descripcion = form.descripcion.data,
            merma.fecha = form.fecha.data
        else:
            db.session.add(nueva_merma)
        db.session.commit()
        flash("Merma agregada correctamente.", "success")
    elif not form.validate():
        formTipo = tipoMermaForm()
        mermas = MermaMateriaPrima.query.filter_by(estatus=1)
        materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
        recetas = []
        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                               formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

    tipo_merma = form.tipo_merma.data
    if tipo_merma == "materiaPrima":
        return redirect(url_for('mermas.merma_materia_prima'))
    else:
        return redirect(url_for('mermas.merma_galletas'))

@mermas.route("/seleccionar_merma", methods=["GET", "POST"])
def seleccionar_merma():
    id = request.form.get('id')
    tipo_merma = request.form.get('tipo_merma')
    originalForm = MermaMateriaPrimaForm()
    if request.method == "POST":
        if tipo_merma == "materiaPrima":
            merma = MermaMateriaPrima.query.get_or_404(id)
            form = tipoMermaForm()
            mermas = MermaMateriaPrima.query.filter_by(estatus=1)
            originalForm.tipo_merma.data = "materiaPrima"
            materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
            recetas = []
        else:
            form = tipoMermaForm()
            mermas = MemraGalleta.query.filter_by(estatus=1)
            originalForm.tipo_merma.data = "galletas"
            recetas = []
            materiasPrimas = []
            merma = MemraGalleta.query.get_or_404(id)

        originalForm.id.data = merma.id
        originalForm.materia_prima_id.data = merma.materia_prima_id
        originalForm.tipo.data = merma.tipo
        originalForm.cantidad.data = merma.cantidad
        originalForm.descripcion.data = merma.descripcion
        originalForm.fecha.data = merma.fecha

        flash("Merma Seleccionada", "success")
        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                               formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)


@mermas.route("/eliminarMerma", methods=["POST"])
def eliminar_merma():
    id = request.form.get('id')
    merma = MermaMateriaPrima.query.get_or_404(id)
    merma.estatus = 0
    db.session.commit()
    flash("El estatus de la merma ha sido actualizado a inactivo.", "success")
    return redirect(url_for('mermas.modulo_mermas'))


@mermas.route("/pruebaCaducidades", methods=["GET"])
def pruebaCaducidades():
    resultado = controller_mermas.verificarCaducidades()
    return json.dumps(resultado)
