from flask import render_template

from formularios import formCompras
from . import compras
from flask import render_template, request, flash, redirect, url_for
import models
from models import db
from controllers.controller_login import requiere_rol
from flask_login import login_required

@compras.route("/moduloCompras", methods=["GET"])
#@login_required
#@requiere_rol("admin")
def modulo_compras():
    form_compras = formCompras.CompraForm()
    tipo_materias = models.Tipo_Materia.query.filter_by(estatus=1).all()
    proveedores =  models.Proveedor.query.filter_by(estatus=1).all()
    listado_compras = models.MateriaPrima.query.filter_by(estatus=1).all()
    return render_template("moduloCompras/moduloCompras.html", form=form_compras,
                           materias_primas=tipo_materias, proveedores = proveedores, compras = listado_compras)


@compras.route("/agregarCompra", methods=["POST"])
def agregar_compra():
    form_compras = formCompras.CompraForm(request.form)
    proveedores = models.Proveedor.query.filter_by(estatus=1).all()
    listado_compras = models.MateriaPrima.query.filter_by(estatus=1).all()
    if form_compras.validate():
        if form_compras.id.data == 0:
            nueva_compra= models.MateriaPrima(
                id_proveedor = form_compras.proveedor_id.data,
                id_tipo_materia = form_compras.id_tipo_materia.data,
                cantidad_compra = form_compras.cantidad.data,
                cantidad_disponible=form_compras.cantidad.data,
                tipo = form_compras.tipo.data,
                precio_compra = form_compras.precio_compra.data,
                create_date = form_compras.fecha.data,
                fecha_caducidad = form_compras.fecha_caducidad.data,
                lote = form_compras.lote.data,
            )

            materia = models.Tipo_Materia.query.get_or_404(form_compras.id_tipo_materia.data)
            materia.cantidad_disponible = materia.cantidad_disponible + form_compras.cantidad.data if materia.tipo == form_compras.tipo.data \
                                            else materia.cantidad_disponible + convertirCantidades(materia.tipo, form_compras.tipo.data, form_compras.cantidad.data)

            db.session.add(nueva_compra)
        else:

            compra = models.MateriaPrima.query.get_or_404(form_compras.id.data)
            if compra.cantidad_disponible != compra.cantidad_compra:
                if compra.cantidad_disponible != form_compras.cantidad.data:
                    flash('No puedes Modificar cantidades de un lote ya utilizado en producción', 'error')
                    return render_template("moduloCompras/moduloCompras.html", form=form_compras,
                                           materias_primas=listado_compras, proveedores=proveedores)

            if compra.id_tipo_materia == form_compras.id_tipo_materia.data:
                materia = models.Tipo_Materia.query.get_or_404(form_compras.id_tipo_materia.data)
                materia.cantidad_disponible -= convertirCantidades(materia.tipo, compra.tipo,
                                                                           compra.cantidad_disponible)

                materia.cantidad_disponible = materia.cantidad_disponible + form_compras.cantidad.data if materia.tipo == form_compras.tipo.data \
                    else materia.cantidad_disponible + convertirCantidades(materia.tipo, form_compras.tipo.data,
                                                                           form_compras.cantidad.data)
                db.session.commit()
            else:

                materia = models.Tipo_Materia.query.get_or_404(compra.id_tipo_materia)
                materia.cantidad_disponible -= convertirCantidades(materia.tipo, compra.tipo,
                                                                           compra.cantidad_disponible)
                db.session.commit()
                nuevaMateria = models.Tipo_Materia.query.get_or_404(form_compras.id_tipo_materia.data)
                nuevaMateria.cantidad_disponible = nuevaMateria.cantidad_disponible + form_compras.cantidad.data if nuevaMateria.tipo == form_compras.tipo.data \
                    else nuevaMateria.cantidad_disponible + convertirCantidades(nuevaMateria.tipo, form_compras.tipo.data,
                                                                           form_compras.cantidad.data)
                db.session.commit()

            compra.id_proveedor = form_compras.proveedor_id.data
            compra.id_tipo_materia = form_compras.id_tipo_materia.data
            compra.cantidad_disponible = form_compras.cantidad.data
            compra.cantidad_compra = form_compras.cantidad.data
            compra.tipo = form_compras.tipo.data
            compra.precio_compra = form_compras.precio_compra.data
            compra.create_date = form_compras.fecha.data
            compra.fecha_caducidad = form_compras.fecha_caducidad.data
            compra.lote = form_compras.lote.data
        db.session.commit()
        return redirect(url_for('compras.modulo_compras'))

    return render_template("moduloCompras/moduloCompras.html", form=form_compras,
                           materias_primas=listado_compras, proveedores = proveedores)


@compras.route('/seleccionarCompra', methods=['GET', 'POST'])
def seleccionar_compra():
    id = request.form['id']
    form_compras = formCompras.CompraForm()
    proveedores = models.Proveedor.query.filter_by(estatus=1).all()
    listado_compras = models.MateriaPrima.query.filter_by(estatus=1).all()
    if request.method == 'POST':
        compra = models.MateriaPrima.query.get_or_404(id)
        form_compras.id.data = compra.id
        form_compras.nombre.data = compra.tipo_materia.nombre
        form_compras.nombre_proveedor.data = compra.proveedor.nombre
        form_compras.proveedor_id.data = compra.id_proveedor
        form_compras.id_tipo_materia.data = compra.id_tipo_materia
        form_compras.cantidad.data = compra.cantidad_disponible
        form_compras.tipo.data = compra.tipo
        form_compras.precio_compra.data = compra.precio_compra
        form_compras.fecha.data = compra.create_date
        form_compras.fecha_caducidad.data = compra.fecha_caducidad
        form_compras.lote.data = compra.lote
        flash('Compra seleccionada correctamente', 'success')

    return render_template("moduloCompras/moduloCompras.html", form=form_compras,
                           materias_primas=listado_compras, proveedores=proveedores)

@compras.route('/eliminarCompra', methods=['POST'])
def eliminar_compra():
    id = request.form['id']
    compra = models.MateriaPrima.query.get_or_404(id)
    materia = models.Tipo_Materia.query.get_or_404(compra.id_tipo_materia)

    materia.cantidad_disponible -= convertirCantidades(materia.tipo, compra.tipo,
                                                       compra.cantidad_disponible)
    compra.estatus = 0
    db.session.commit()
    flash('Materia Prima eliminada correctamente', 'success')
    return redirect(url_for('compras.modulo_compras'))


def convertirCantidades(tipo1, tipo2, cantidad):
    if (tipo1 == "g" or tipo1 == "ml") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad * 1000
    elif (tipo1 == "kg" or tipo1 == "l") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 1000

    return cantidad