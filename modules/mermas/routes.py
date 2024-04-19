import json

from flask import render_template, request, flash, redirect, url_for
from controllers.controller_login import requiere_token

from controllers import controller_mermas
from controllers.controller_materia_prima import actualizar_cantidades_tipo
from models import MermaMateriaPrima, db, MemraGalleta, MateriaPrima, CostoGalleta, Receta, Produccion
from . import mermas
from formularios.formsMerma import MermaMateriaPrimaForm, tipoMermaForm
from controllers.controller_login import requiere_rol
from flask_login import login_required


# /mermas

@mermas.route("/merma_galletas", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
def merma_galletas():
    form = tipoMermaForm()
    originalForm = MermaMateriaPrimaForm()
    mermas = MemraGalleta.query.filter_by(estatus=1).all()
    originalForm.tipo_merma.data = "galletas"
    form.tipo_merma.data = "galletas"
    recetas = Produccion.query.filter_by(estatus='terminada').all()
    materiasPrimas = []

    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                           formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)


@mermas.route("/merma_materia_prima", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
def merma_materia_prima():
    form = tipoMermaForm()
    originalForm = MermaMateriaPrimaForm()
    mermas = MermaMateriaPrima.query.filter_by(estatus=1)
    originalForm.tipo_merma.data = "materiaPrima"
    form.tipo_merma.data = "materiaPrima"
    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
    recetas = Produccion.query.filter_by(estatus='terminada').all()

    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                           formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)

@mermas.route("/moduloMermas", methods=["POST", "GET"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
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


@mermas.route("/mermas/agregarMerma", methods=["GET", "POST"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
def agregar_nueva_merma():
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
                    recetas = Produccion.query.filter_by(estatus='terminada').all()

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

                receta = Produccion.query.get_or_404(form.materia_prima_id.data)
                form.cantidad.data = int(form.cantidad.data)
                cantidad = convertirCantidadaPz(form.tipo.data, form.cantidad.data)

                if receta.galletas_disponibles < cantidad:
                    flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                    formTipo = tipoMermaForm()
                    formTipo.tipo_merma.data = "galletas"
                    mermas = MemraGalleta.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Produccion.query.filter_by(estatus='terminada').all()

                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

                receta.galletas_disponibles -= cantidad
                receta.receta.Costo_Galleta.galletas_disponibles -= cantidad



                db.session.commit()
                nueva_merma = MemraGalleta(
                        produccion_id=form.materia_prima_id.data,
                        tipo=form.tipo.data,
                        cantidad=form.cantidad.data,
                        descripcion=form.descripcion.data,
                        fecha=form.fecha.data
                )
            db.session.add(nueva_merma)
        if form.id.data != 0:
            if form.tipo_merma.data == "materiaPrima":
                merma = MermaMateriaPrima.query.get_or_404(form.id.data)
                if not ("% por producción de la receta de" in merma.descripcion or "enviado a merma por la solicitud de la receta" in merma.descripcion):
                    materia_prima = MateriaPrima.query.get_or_404(merma.materia_prima_id)
                    materia_prima.cantidad_disponible += merma.cantidad

                    if merma.materia_prima_id == form.materia_prima_id.data:
                        db.session.commit()

                    materia_prima = MateriaPrima.query.get_or_404(form.materia_prima_id.data)


                    if materia_prima.cantidad_disponible < form.cantidad.data:
                        materia_prima = MateriaPrima.query.get_or_404(merma.materia_prima_id)
                        materia_prima.cantidad_disponible -= merma.cantidad
                        if merma.materia_prima_id == form.materia_prima_id.data:
                            db.session.commit()
                        flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                        formTipo = tipoMermaForm()
                        mermas = MermaMateriaPrima.query.filter_by(estatus=1)
                        materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                        recetas = Produccion.query.filter_by(estatus='terminada').all()
                        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                              formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)
                    else:
                        db.session.commit()

                    materia_prima.cantidad_disponible -= form.cantidad.data
                    db.session.commit()
                    merma.materia_prima_id = form.materia_prima_id.data,
                    merma.tipo = form.tipo.data,
                    merma.cantidad = form.cantidad.data,
                    merma.descripcion = form.descripcion.data,
                    merma.fecha = form.fecha.data
                else:
                    flash("No se puede editar una merma generada en producción", "danger")
                    formTipo = tipoMermaForm()
                    mermas = MermaMateriaPrima.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Produccion.query.filter_by(estatus='terminada').all()
                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)
            else:
                merma = MemraGalleta.query.get_or_404(form.id.data)

                cantidad = convertirCantidadaPz( merma.tipo,  merma.cantidad)
                receta = Produccion.query.get_or_404(merma.produccion_id)
                receta.galletas_disponibles += merma.cantidad
                receta.receta.Costo_Galleta.galletas_disponibles += merma.cantidad
                if merma.produccion_id == form.materia_prima_id.data:
                    db.session.commit()
                receta = Produccion.query.get_or_404(form.materia_prima_id.data)

                form.cantidad.data = int(form.cantidad.data)
                cantidad = convertirCantidadaPz(form.tipo.data, form.cantidad.data)
                if receta.galletas_disponibles < cantidad:
                    flash("No se puede agregar una merma mayor a la cantidad existente.", "danger")
                    receta = Produccion.query.get_or_404(merma.produccion_id)
                    receta.galletas_disponibles -= merma.cantidad
                    receta.receta.Costo_Galleta.galletas_disponibles -= merma.cantidad
                    if merma.produccion_id == form.materia_prima_id.data:
                        db.session.commit()
                    formTipo = tipoMermaForm()
                    formTipo.tipo_merma.data = "galletas"
                    mermas = MemraGalleta.query.filter_by(estatus=1)
                    materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
                    recetas = Produccion.query.filter_by(estatus='terminada').all()

                    return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                                           formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)
                else:
                    db.session.commit()

                receta.galletas_disponibles -= cantidad
                db.session.commit()
                merma.produccion_id = form.materia_prima_id.data,
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
        recetas = Produccion.query.filter_by(estatus='terminada').all()

        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=form,
                               formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)

    tipo_merma = form.tipo_merma.data
    if tipo_merma == "materiaPrima":
        return redirect(url_for('mermas.merma_materia_prima'))
    else:
        return redirect(url_for('mermas.merma_galletas'))

@mermas.route("/seleccionar_merma", methods=["GET", "POST"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
def seleccionar_merma():
    id = request.form.get('id')
    tipo_merma = request.form.get('tipo_merma')
    originalForm = MermaMateriaPrimaForm()
    if request.method == "POST":
        if tipo_merma == "materiaPrima":
            merma = MermaMateriaPrima.query.get_or_404(id)
            materia = MateriaPrima.query.get_or_404(merma.materia_prima_id)
            nombre = materia.tipo_materia.nombre
            form = tipoMermaForm()
            mermas = MermaMateriaPrima.query.filter_by(estatus=1)
            originalForm.tipo_merma.data = "materiaPrima"
            materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
            recetas = Produccion.query.filter_by(estatus='terminada').all()

        else:
            form = tipoMermaForm()
            mermas = MemraGalleta.query.filter_by(estatus=1)
            originalForm.tipo_merma.data = "galletas"
            form.tipo_merma.data = "galletas"
            recetas = Produccion.query.filter_by(estatus='terminada').all()

            materiasPrimas = []
            merma = MemraGalleta.query.get_or_404(id)

            produccion = Produccion.query.get_or_404(merma.produccion_id)
            nombre = produccion.receta.nombre

        originalForm.id.data = merma.id
        originalForm.materia_prima_id.data = merma.materia_prima_id if tipo_merma == "materiaPrima" else merma.produccion_id
        originalForm.tipo.data = merma.tipo
        originalForm.cantidad.data = merma.cantidad
        originalForm.descripcion.data = merma.descripcion
        originalForm.fecha.data = merma.fecha
        originalForm.nombre.data = nombre

        flash("Merma Seleccionada", "success")
        return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                               formTipo=form, materiasPrimas=materiasPrimas, recetas=recetas)


@mermas.route("/eliminarMerma", methods=["POST"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
def eliminar_merma():
    id = request.form.get('id')
    tipo_merma = request.form.get('tipoMerma')
    if tipo_merma == "materiaPrima":
        merma = MermaMateriaPrima.query.get_or_404(id)
        if not ("% por producción de la receta de" in merma.descripcion or "enviado a merma por la solicitud de la receta" in merma.descripcion):
            materia_prima = MateriaPrima.query.get_or_404(merma.materia_prima_id)
            materia_prima.cantidad_disponible += merma.cantidad
        else:
            flash("No se puede eliminar una merma generada en producción", "danger")
            formTipo = tipoMermaForm()
            originalForm = MermaMateriaPrimaForm()
            mermas = MermaMateriaPrima.query.filter_by(estatus=1)
            materiasPrimas = controller_mermas.getMateriasPrimasSinMerma()
            recetas = Produccion.query.filter_by(estatus='terminada').all()
            return render_template('moduloMermas/crudMermas.html', mermas=mermas, form=originalForm,
                                   formTipo=formTipo, materiasPrimas=materiasPrimas, recetas=recetas)
    else:
        merma = MemraGalleta.query.get_or_404(id)

        receta = Produccion.query.get_or_404(merma.produccion_id)
        cantidad = convertirCantidadaPz(merma.tipo, merma.cantidad)

        receta.galletas_disponibles += cantidad
        receta.receta.Costo_Galleta.galletas_disponibles += cantidad




    db.session.commit()
    merma.estatus = 0
    db.session.commit()
    actualizar_cantidades_tipo()
    flash("El estatus de la merma ha sido actualizado a inactivo.", "success")
    return redirect(url_for('mermas.modulo_mermas'))


@mermas.route("/pruebaCaducidades", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin", "inventario", "produccion")
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


