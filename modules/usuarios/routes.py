from flask import render_template, request, redirect, url_for, flash
from models import db, User
from controllers import controller_usuarios
from . import usuarios
from controllers.controller_login import requiere_rol, requiere_token, es_contrasena_segura, encriptar_contrasena
from flask_login import login_required
from formularios import formUsuario
from formularios.formUsuario import UsersForm
from flask import request

@usuarios.route("/crudUsuarios", methods=["GET"])
@login_required
@requiere_token
@requiere_rol("admin")
def crud_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)

    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    return render_template("moduloUsuarios/crudUsuarios.html", form=form_usuarios, users=listado_usuarios)



@usuarios.route("/agregarUsuario", methods=["GET", "POST"])
@login_required
@requiere_token
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
                crypted = encriptar_contrasena(contrasena)
                user.contrasena = crypted
            else:
                crypted = encriptar_contrasena(contrasena)
                form_usuarios.contrasena.data = crypted
                controller_usuarios.agregarUsuario(form_usuarios)
        else:
            safePass = es_contrasena_segura(contrasena)
            print(safePass)
            if not safePass[0]:
                if safePass[1] == 0:
                    flash("La contraseña es una de las contraseñas inseguras", "warning")
                elif safePass[1] == 1:
                    flash("La contraseña debe tener al menos un número", "warning")
                elif safePass[1] == 2:
                    flash("La contraseña debe tener al menos una mayúscula", "warning")
                elif safePass[1] == 3:
                    flash("La contraseña debe tener al menos un carácter especial", "warning")
                listado_usuarios = User.query.all()
                return render_template("moduloUsuarios/crudUsuarios.html", form=form_usuarios, users=listado_usuarios)

            # Si al menos uno de los campos de contraseña no está vacío, actualiza la contraseña
            if contrasena == confirmar_contrasena:
                if form_usuarios.id.data != 0:
                    user = User.query.get_or_404(form_usuarios.id.data)
                    user.nombre = form_usuarios.nombre.data
                    user.puesto = form_usuarios.puesto.data
                    user.rol = form_usuarios.rol.data
                    user.estatus = 'Activo'
                    user.usuario = form_usuarios.usuario.data
                    crypted = encriptar_contrasena(contrasena)
                    user.contrasena = crypted
                else:
                    crypted = encriptar_contrasena(contrasena)
                    form_usuarios.contrasena.data = crypted
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
@requiere_token
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
@requiere_token
@requiere_rol("admin")
def eliminar_usuarios():
    id = request.form['id']
    usuario = User.query.get_or_404(id)
    usuario.estatus = 'Inactivo'
    db.session.commit()
    flash("Usuario eliminado", "info")
    return redirect(url_for("usuarios.crud_usuarios"))
