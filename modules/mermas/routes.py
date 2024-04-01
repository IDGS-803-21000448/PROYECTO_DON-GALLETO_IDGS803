import json

from flask import render_template, request, flash, redirect, url_for

from controllers import controller_mermas
from controllers.controller_materia_prima import actualizar_cantidades_tipo
from models import MermaMateriaPrima, db, MemraGalleta, MateriaPrima, CostoGalleta, Receta
from . import mermas
from formularios.formsMerma import MermaMateriaPrimaForm, tipoMermaForm
from controllers.controller_login import requiere_rol
from flask_login import login_required


# /mermas

@mermas.route("/merma_galletas", methods=["GET"])
@login_required
@requiere_rol("admin")
def merma_galletas():
    form = tipoMermaForm()
    originalForm = MermaMateriaPrimaForm()
    mermas = MemraGalleta.query.filter_by(estatus=1).all()
    originalForm.tipo_merma.data = "galletas"
    form.tipo_merma.data = "galletas"
    recetas = Receta.query.filter_by(estatus=1).all()
    materiasPrimas = []

    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                           formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)


@mermas.route("/merma_materia_prima", methods=["GET"])
@login_required
@requiere_rol("admin")
def merma_materia_prima():
    form = tipoMermaForm()
    originalForm = MermaMateriaPrimaForm()
    mermas = MermaMateriaPrima.query.filter_by(estatus=1)
    originalForm.tipo_merma.data = "materiaPrima"
    form.tipo_merma.data = "materiaPrima"
    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
    recetas = Receta.query.filter_by(estatus=1).all()

    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                           formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)

@mermas.route("/moduloMermas", methods=["POST", "GET"])
@login_required
@requiere_rol("admin")
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
@login_required
@requiere_rol("admin")
def agregar_merma():
    form = MermaMateriaPrimaForm(request.form)
    if request.method == "POST" and form.validate():
        if form.id.data == 0:
            if form.tipo_merma.data == "materiaPrima":
                materia_prima = MateriaPrima.query.get_or_404(form.materia_prima_id.data)
                if materia_prima.cantidad_disponible < form.cantidad.data:
                    flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                    formTipo = tipoMermaForm()
                    mermas = MermaMateriaPrima.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Receta.query.filter_by(estatus=1).all()

                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

                materia_prima.cantidad_disponible -= form.cantidad.data
                db.session.commit()
                nueva_merma = MermaMateriaPrima(
                    materia_prima_id=form.materia_prima_id.data,
                    tipo=form.tipo.data,
                    cantidad=form.cantidad.data,
                    descripcion=form.descripcion.data,
                    fecha=form.fecha.data
                )
            else:

                receta = Receta.query.get_or_404(form.materia_prima_id.data)

                cantidad = convertirCantidadaPz(form.tipo.data, form.cantidad.data)

                if receta.Costo_Galleta.galletas_disponibles < cantidad:
                    flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                    formTipo = tipoMermaForm()
                    mermas = MemraGalleta.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Receta.query.filter_by(estatus=1).all()

                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

                receta.Costo_Galleta.galletas_disponibles -= cantidad

                db.session.commit()
                nueva_merma = MemraGalleta(
                        receta_id=form.materia_prima_id.data,
                        tipo=form.tipo.data,
                        cantidad=form.cantidad.data,
                        descripcion=form.descripcion.data,
                        fecha=form.fecha.data
                )
            db.session.add(nueva_merma)
        if form.id.data != 0:
            if form.tipo_merma.data == "materiaPrima":
                merma = MermaMateriaPrima.query.get_or_404(form.id.data)

                materia_prima = MateriaPrima.query.get_or_404(merma.materia_prima_id)
                materia_prima.cantidad_disponible += merma.cantidad
                db.session.commit()

                materia_prima = MateriaPrima.query.get_or_404(form.materia_prima_id.data)


                if materia_prima.cantidad < form.cantidad.data:
                    flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                    formTipo = tipoMermaForm()
                    mermas = MermaMateriaPrima.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Receta.query.filter_by(estatus=1).all()

                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

                materia_prima.cantidad_disponible -= form.cantidad.data
                db.session.commit()
                merma.materia_prima_id = form.materia_prima_id.data,
                merma.tipo = form.tipo.data,
                merma.cantidad = form.cantidad.data,
                merma.descripcion = form.descripcion.data,
                merma.fecha = form.fecha.data
            else:
                merma = MemraGalleta.query.get_or_404(form.id.data)

                cantidad = convertirCantidadaPz( merma.tipo,  merma.cantidad)
                receta = Receta.query.get_or_404(merma.receta_id)
                receta.Costo_Galleta.galletas_disponibles += cantidad
                db.session.commit()

                receta = Receta.query.get_or_404(form.materia_prima_id.data)

                cantidad = convertirCantidadaPz(form.tipo.data, form.cantidad.data)
                if receta.Costo_Galleta.galletas_disponibles < cantidad:
                    flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                    formTipo = tipoMermaForm()
                    mermas = MemraGalleta.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Receta.query.filter_by(estatus=1).all()

                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

                receta.Costo_Galleta.galletas_disponibles -= cantidad
                db.session.commit()
                merma.receta_id = form.materia_prima_id.data,
                merma.tipo = form.tipo.data,
                merma.cantidad = form.cantidad.data,
                merma.descripcion = form.descripcion.data,
                merma.fecha = form.fecha.data

        db.session.commit()
        actualizar_cantidades_tipo()
        flash("Merma agregada correctamente.", "success")
    elif not form.validate():
        formTipo = tipoMermaForm()
        mermas = MermaMateriaPrima.query.filter_by(estatus=1)
        materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
        recetas = Receta.query.filter_by(estatus=1).all()

        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                               formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

    tipo_merma = form.tipo_merma.data
    if tipo_merma == "materiaPrima":
        return redirect(url_for('mermas.merma_materia_prima'))
    else:
        return redirect(url_for('mermas.merma_galletas'))

@mermas.route("/seleccionar_merma", methods=["GET", "POST"])
@login_required
@requiere_rol("admin")
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
            recetas = Receta.query.filter_by(estatus=1).all()

        else:
            form = tipoMermaForm()
            mermas = MemraGalleta.query.filter_by(estatus=1)
            originalForm.tipo_merma.data = "galletas"
            recetas = Receta.query.filter_by(estatus=1).all()

            materiasPrimas = []
            merma = MemraGalleta.query.get_or_404(id)

        originalForm.id.data = merma.id
        originalForm.materia_prima_id.data = merma.materia_prima_id if tipo_merma == "materiaPrima" else merma.receta_id
        originalForm.tipo.data = merma.tipo
        originalForm.cantidad.data = merma.cantidad
        originalForm.descripcion.data = merma.descripcion
        originalForm.fecha.data = merma.fecha

        flash("Merma Seleccionada", "success")
        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                               formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)


@mermas.route("/eliminarMerma", methods=["POST"])
@login_required
@requiere_rol("admin")
def eliminar_merma():
    id = request.form.get('id')
    tipo_merma = request.form.get('tipoMerma')
    if tipo_merma == "materiaPrima":
        merma = MermaMateriaPrima.query.get_or_404(id)

        materia_prima = MateriaPrima.query.get_or_404(merma.materia_prima_id)
        materia_prima.cantidad_disponible += merma.cantidad
    else:
        merma = MemraGalleta.query.get_or_404(id)

        receta = Receta.query.get_or_404(merma.receta_id)
        cantidad = convertirCantidadaPz(merma.tipo.data, merma.cantidad.data)

        receta.Costo_Galleta.galletas_disponibles += cantidad


    db.session.commit()
    merma.estatus = 0
    db.session.commit()
    actualizar_cantidades_tipo()
    flash("El estatus de la merma ha sido actualizado a inactivo.", "success")
    return redirect(url_for('mermas.modulo_mermas'))


@mermas.route("/pruebaCaducidades", methods=["GET"])
@login_required
@requiere_rol("admin")
def pruebaCaducidades():
    resultado = controller_mermas.verificarCaducidades()
    return json.dumps(resultado)



def convertirCantidadaPz(tipo, cantidad):
    if tipo == "pz":
        return cantidad
    elif tipo == "kg":
        conv = cantidad/100
        cant = conv/30
        return round(cant)
    elif tipo == "g":
        cant = cantidad / 30
        return round(cant)
    elif tipo == "pkg":
        cant = 30 * cantidad
        return cant


