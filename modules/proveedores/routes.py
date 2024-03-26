from flask import render_template, request, redirect, url_for, flash
from models import db, Proveedor
from controllers import controller_proveedores
from . import proveedores
from formularios import formProveedores
from formularios.formProveedores import ProveedorForm
from flask import request

@proveedores.route("/crudProveedores", methods=["GET"])
def crud_proveedores():
    form_proveedores = formProveedores.ProveedorForm(request.form)
    
    listado_proveedor = Proveedor.query.filter_by(estatus = 1).all()
    return render_template("moduloProveedores/crudProveedores.html", formProveedor=form_proveedores, proveedores = listado_proveedor)


# @proveedores.route("/agregarProveedor", methods=["GET", "POST"])
# def agregar_proveedor():
#     form_proveedor = formProveedores.ProveedorForm(request.form)
#     if request.method == "POST" and form_proveedor.validate():
#         controller_proveedores.agregar_proveedor(form_proveedor)
#         form_proveedor = formProveedores.ProveedorForm()
#         listado_proveedor = Proveedor.query.filter_by(estatus = 1).all()
#         flash("Proveedoredor agregado correctamente", "success")
#         return render_template("moduloProveedores/crudProveedores.html", formProveedor=form_proveedor, proveedores=listado_proveedor)
#     else:
#         # Aquí no se debería volver a crear el objeto form_proveedor
#         flash("Error al agregar proveedor", "error")
#         listado_proveedor = Proveedor.query.all()
#         return render_template("moduloProveedores/crudProveedores.html", formProveedor=form_proveedor, proveedores=listado_proveedor)


@proveedores.route('/agregarProveedor', methods=['GET','POST'])
def agregar_proveedor():
    form_proveedor = formProveedores.ProveedorForm(request.form)
    
    if request.method == 'POST' and form_proveedor.validate():
        nuevo_proveedor = Proveedor(
            nombre = form_proveedor.nombre.data,
            direccion = form_proveedor.direccion.data,
            telefono = form_proveedor.telefono.data,
            nombre_vendedor = form_proveedor.nombre_vendedor.data,
            estatus = 1
        )  
        if form_proveedor.id.data != 0:
            proveedor = Proveedor.query.get_or_404(form_proveedor.id.data)
            proveedor.nombre = form_proveedor.nombre.data
            proveedor.direccion = form_proveedor.direccion.data
            proveedor.telefono = form_proveedor.telefono.data
            proveedor.nombre_vendedor = form_proveedor.nombre_vendedor.data
        else:
            controller_proveedores.agregar_proveedor(form_proveedor)
            #db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('Proveedor agregado correctamente', 'success')
        return redirect(url_for('proveedores.crud_proveedores'))

    # Agregar un retorno para manejar otros casos
    listado_proveedor = Proveedor.query.filter_by(estatus = 1).all()

    return render_template('moduloProveedores/crudProveedores.html', formProveedor=form_proveedor, proveedores=listado_proveedor)



@proveedores.route('/seleccionarProveedor', methods=['GET', 'POST'])
def seleccionar_proveedor():
    id = request.form['id']  # Usar corchetes para acceder al valor del campo 'id' en el formulario
    originalForm = ProveedorForm()
    listado_proveedor = Proveedor.query.filter_by(estatus=1).all()
    if request.method == 'POST':
        proveedor = Proveedor.query.get_or_404(id)
        originalForm.id.data = proveedor.id
        originalForm.nombre.data = proveedor.nombre
        originalForm.direccion.data = proveedor.direccion
        originalForm.telefono.data = proveedor.telefono
        originalForm.nombre_vendedor.data = proveedor.nombre_vendedor
        flash('Proveedor seleccionado correctamente', 'success')
    return render_template('moduloProveedores/crudProveedores.html', formProveedor=originalForm, proveedores=listado_proveedor)

@proveedores.route('/eliminarProveedor', methods=['POST'])
def eliminar_proveedor():
    id = request.form['id']
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.estatus = 0
    db.session.commit()
    flash('Proveedor eliminado correctamente', 'success')
    return redirect(url_for('proveedores.crud_proveedores'))