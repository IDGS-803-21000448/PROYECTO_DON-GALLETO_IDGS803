from flask import render_template, request, flash, redirect, url_for, make_response
from . import login as login_bp  # Cambia el nombre al importar para evitar conflictos
from formularios.formLogin import LoginForm
import flask_login as fl
from flask_login import current_user
from models import db, User
from controllers.controller_login import generate_jwt_token

@login_bp.route("/login", methods=["GET", "POST"])
def login_view():  # Cambia el nombre de la función para evitar conflictos
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        user = User.query.filter_by(usuario=usuario).first()  # Asegúrate de que este campo coincida con tu modelo
        if user and user.contrasena == contrasena:
    # Usuario autenticado correctamente
            res = fl.login_user(user, force=True)

            token = generate_jwt_token(user.id)
            print(f"TOKEN: {token}")
            if token is None:
                # Manejar el caso de error, por ejemplo, enviando una respuesta de error
                flash('Error al generar el token de autenticación', 'error')
                return redirect(url_for('login.login_view'))

            # Si todo está bien, proceder como antes
            response = make_response(redirect(url_for('index.index')))
            response.set_cookie('auth_token', token)
            return response
    else:
        flash('Error en el formulario', 'error')

    return render_template("moduloLogin/login.html", form=form)

@login_bp.route("/logout", methods=["GET", "POST"])
def logout():
    fl.logout_user()
    response = make_response(redirect(url_for('login.login_view')))
    response.set_cookie('auth_token', '')
    flash('Has cerrado sesión', 'success')
    return response  # Asegúrate de que el nombre del endpoint sea correcto
