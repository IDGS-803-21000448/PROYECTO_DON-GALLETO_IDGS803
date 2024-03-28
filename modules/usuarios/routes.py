from flask import render_template, request, redirect, url_for, flash
from models import db, User
from controllers import controller_usuarios
from . import usuarios
from controllers.controller_login import requiere_rol
from flask_login import login_required
from formularios import formUsuario
from formularios.formUsuario import UsersForm
from flask import request

@usuarios.route("/crudUsuarios", methods=["GET"])
@login_required
@requiere_rol("admin")
def crud_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)

    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    return render_template("moduloUsuarios/crudUsuarios.html", form=form_usuarios, users=listado_usuarios)




@usuarios.route("/agregarUsuario", methods=["GET", "POST"])
@login_required
@requiere_rol("admin")
def agregar_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)
    if request.method == "POST" and form_usuarios.validate():
        # Verificar si las contraseñas coinciden
        contrasena = form_usuarios.contrasena.data
        confirmar_contrasena = form_usuarios.confirmar_contrasena.data

        # Verificar si ambos campos de contraseña están vacíos
        if not contrasena and not confirmar_contrasena:
            if form_usuarios.id.data != 0:
                user = User.query.get_or_404(form_usuarios.id.data)
                user.nombre = form_usuarios.nombre.data
                user.puesto = form_usuarios.puesto.data
                user.rol = form_usuarios.rol.data
                user.estatus = 'Activo'
                user.usuario = form_usuarios.usuario.data
            else:
                controller_usuarios.agregarUsuario(form_usuarios)
        else:
            # Si al menos uno de los campos de contraseña no está vacío, actualiza la contraseña
            if contrasena == confirmar_contrasena:
                if form_usuarios.id.data != 0:
                    user = User.query.get_or_404(form_usuarios.id.data)
                    user.nombre = form_usuarios.nombre.data
                    user.puesto = form_usuarios.puesto.data
                    user.rol = form_usuarios.rol.data
                    user.estatus = 'Activo'
                    user.usuario = form_usuarios.usuario.data
                    user.contrasena = contrasena
                else:
                    controller_usuarios.agregarUsuario(form_usuarios)
            else:
                flash("Las contraseñas no coinciden. Inténtalo de nuevo.", "error")
                listado_usuarios = User.query.all()
                return render_template("moduloUsuarios/crudUsuarios.html", form=form_usuarios, users=listado_usuarios)

        db.session.commit()
        flash('Usuario agregado correctamente', 'success')
        return redirect(url_for('usuarios.crud_usuarios'))

    # Agregar un retorno para manejar otros casos
    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    return render_template('moduloUsuarios/crudUsuarios.html', form=form_usuarios, users=listado_usuarios)




@usuarios.route("/seleccionarUsuario", methods=["GET", "POST"])
@login_required
@requiere_rol("admin")
def seleccionar_usuario():
    id = request.form['id']  # Usar corchetes para acceder al valor del campo 'id' en el formulario
    originalForm = formUsuario.UsersForm()
    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    if request.method == 'POST':
        user = User.query.get_or_404(id)
        originalForm.id.data = user.id
        originalForm.nombre.data = user.nombre
        originalForm.puesto.data = user.puesto
        originalForm.rol.data = user.rol
        originalForm.usuario.data = user.usuario
        originalForm.contrasena.data = user.contrasena
        flash("Usuario modificado temporalmente", "info")
    return render_template('moduloUsuarios/crudUsuarios.html', form=originalForm, users=listado_usuarios)


@usuarios.route("/eliminarUsuario", methods=["POST"])
@login_required
@requiere_rol("admin")
def eliminar_usuarios():
    id = request.form['id']
    usuario = User.query.get_or_404(id)
    usuario.estatus = 'Inactivo'
    db.session.commit()
    flash("Usuario eliminado", "info")
    return redirect(url_for("usuarios.crud_usuarios"))
