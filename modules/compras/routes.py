from flask import render_template
from . import compras
from flask import render_template, request, flash, redirect, url_for
import models
from models import db
from controllers.controller_login import requiere_rol
from flask_login import login_required

@compras.route("/moduloCompras", methods=["GET"])
@login_required
@requiere_rol("admin")
def modulo_compras():
    form_compras = formCompras.CompraForm()
    proveedores =  models.Proveedor.query.filter_by(estatus=1).all()
    listado_compras = models.MateriaPrima.query.filter_by(estatus=1).all()
    return render_template("moduloCompras/moduloCompras.html", form=form_compras,
                           materias_primas=listado_compras, proveedores = proveedores)


@compras.route("/agregarCompra", methods=["POST"])
def agregar_compra():
    form_compras = formCompras.CompraForm(request.form)
    proveedores = models.Proveedor.query.filter_by(estatus=1).all()
    listado_compras = models.MateriaPrima.query.filter_by(estatus=1).all()
    if form_compras.validate():
        if form_compras.id.data == 0:
            nueva_compra= models.MateriaPrima(


            )
        db.add()


    return render_template("moduloCompras/moduloCompras.html", form=form_compras,
                           materias_primas=listado_compras, proveedores = proveedores)