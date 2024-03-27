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


# @usuarios.route("/agregarUsuario", methods=["GET", "POST"])
# @login_required
# @requiere_rol("admin")
# def agregar_usuarios():
#     form_usuarios = formUsuario.UsersForm(request.form)
#     if request.method == "POST" and form_usuarios.validate():
#         # Verificar si las contraseñas coinciden
#         contrasena = form_usuarios.contrasena.data
#         confirmar_contrasena = form_usuarios.confirmar_contrasena.data
#         if contrasena != confirmar_contrasena:
#             flash("Las contraseñas no coinciden. Inténtalo de nuevo.", "error")
#             listado_usuarios = User.query.all()
#             return render_template("moduloUsuarios/crudUsuarios.html", form=form_usuarios, users=listado_usuarios)

#         if form_usuarios.id.data != 0:
#             user = User.query.get_or_404(form_usuarios.id.data)
#             user.nombre = form_usuarios.nombre.data
#             user.puesto = form_usuarios.puesto.data
#             user.rol = form_usuarios.rol.data
#             user.estatus = 'Activo'
#             user.usuario = form_usuarios.usuario.data
#             user.contrasena = form_usuarios.contrasena.data
#         else:
#             controller_usuarios.agregarUsuario(form_usuarios)
#             #db.session.add(nuevo_proveedor)
#         db.session.commit()
#         flash('Usuario agregado correctamente', 'success')
#         return redirect(url_for('usuarios.crud_usuarios'))

#     # Agregar un retorno para manejar otros casos
#     listado_usuarios = User.query.filter_by(estatus='Activo').all()
#     return render_template('moduloUsuarios/crudUsuarios.html', form=form_usuarios, users=listado_usuarios)


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


# @usuarios.route("/modificarUsuario", methods=["GET", "POST"])
# @login_required
# @requiere_rol("admin")
# def modificar_usuarios():
#     form_usuarios = formUsuario.UsersForm(request.form)

#     # Obtener el ID del usuario
#     id = request.args.get('id')

#     if id:
#         # Intentar obtener el usuario de la base de datos
#         user1 = User.query.filter_by(id=id, estatus='Activo').first()

#         if user1:
#             if request.method == "GET":
#                 # Poblar el formulario con los datos del usuario
#                 form_usuarios = formUsuario.UsersForm(obj=user1)
#                 # Asegurarse de que el campo confirmar_contrasena tenga los mismos datos que contrasena
#                 form_usuarios.confirmar_contrasena.data = user1.contrasena
#             elif request.method == "POST":
#                 # Solo llenar los campos del formulario sin modificar el usuario en la base de datos
#                 form_usuarios.populate_obj(user1)
#                 flash("Usuario modificado temporalmente", "info")
#         else:
#             # Manejar el caso en que el usuario no se encuentre en la base de datos
#             flash("Usuario no encontrado en la base de datos", "error")
#             return redirect(url_for("crud_usuarios"))
#     else:
#         # Manejar el caso en que no se proporcione un ID de usuario
#         flash("ID de usuario no proporcionado", "error")
#         return redirect(url_for("crud_usuarios"))

#     # Obtener el listado de usuarios activos
#     listado_usuarios = User.query.filter_by(estatus='Activo').all()

#     # Renderizar el template con el formulario y el listado de usuarios
#     return render_template("moduloUsuarios/modificarUsuario.html", form=form_usuarios, users=listado_usuarios)


# @usuarios.route("/confirmarModificacion", methods=["POST"])
# @login_required
# @requiere_rol("admin")
# def confirmar_modificacion():
#     form_usuarios = formUsuario.UsersFormModificar(request.form)

#     id = request.form.get('id')
#     user1 = User.query.filter_by(id=id, estatus='Activo').first()

#     if request.method == "POST":
#         try:
#             # Actualizar los datos del usuario con los del formulario
#             form_usuarios.populate_obj(user1)
            
#             # Modificar el usuario en la base de datos
#             controller_usuarios.modificarUsuario(form_usuarios, id)
            
#             # Confirmar los cambios en la base de datos
#             #db.session.commit()
            
#             # Redireccionar y mostrar mensaje de éxito
#             flash("Usuario modificado correctamente", "success")
#             return redirect(url_for("crud_usuarios"))
        
#         except Exception as e:
#             # Manejar el caso en que ocurra un error al modificar el usuario
#             db.session.rollback()
#             flash(f"Error al modificar usuario: {str(e)}", "error")
#             return redirect(url_for("usuarios.crud_usuarios"))

#     # Si la validación del formulario falla o no se envía una solicitud POST,
#     # redireccionar de vuelta a la página de administración de usuarios
#     return redirect(url_for("usuarios.crud_usuarios"))


# @usuarios.route("/confirmarEliminacion", methods=["GET", "POST"])
# @login_required
# @requiere_rol("admin")
# def confirmarEliminacion():
#     id = request.args.get('id')
#     if id:
#         user = User.query.filter_by(id=id, estatus='Activo').first()
#         if user:
#             return render_template("moduloUsuarios/confirmarBorradoUsuario.html", usuario_id=id)
#         else:
#             flash('Usuario no encontrado en la base de datos o ya está inactivo', 'error')
#     else:
#         flash('ID de usuario no proporcionado', 'error')

#     listado_usuarios = User.query.filter_by(estatus='Activo').all()
#     return render_template("moduloUsuarios/crudUsuarios.html", users=listado_usuarios)


# @usuarios.route("/borrarUsuario", methods=["GET", "POST"])
# @login_required
# @requiere_rol("admin")
# def borrar_usuario():
#     id = request.args['id']  # Obtener directamente el ID del usuario de la URL
#     if id:
#         user = User.query.filter_by(id=id, estatus='Activo').first()
#         if user:
#             # Cambiar el estado del usuario a 'Inactivo' en lugar de eliminarlo físicamente
#             user.estatus = 'Inactivo'
#             db.session.commit()
#             flash('Usuario marcado como inactivo correctamente', 'success')
#             return redirect(url_for("crud_usuarios"))  # Redirigir a la página de listado de usuarios
#         else:
#             # Manejar el caso en que el usuario no existe o ya está inactivo
#             flash('Usuario no encontrado en la base de datos o ya está inactivo', 'error')
#     else:
#         flash('ID de usuario no proporcionado', 'error')

#     listado_usuarios = User.query.filter_by(estatus='Activo').all()
#     return render_template("moduloUsuarios/crudUsuarios.html", users=listado_usuarios)