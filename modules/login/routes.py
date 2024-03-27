from flask import render_template, request, flash, redirect, url_for
from . import login as login_bp  # Cambia el nombre al importar para evitar conflictos
from formularios.formLogin import LoginForm
import flask_login as fl
from flask_login import current_user
from models import db, User

@login_bp.route("/login", methods=["GET", "POST"])
def login_view():  # Cambia el nombre de la función para evitar conflictos
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        user = User.query.filter_by(usuario=usuario).first()  # Asegúrate de que este campo coincida con tu modelo
        if user and user.contrasena == contrasena:
            res = fl.login_user(user, force=True)
            flash('Has iniciado sesión', 'success')
            return redirect(url_for('index.index'))  # Asegúrate de que 'index' sea el endpoint correcto
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    else:
        flash('Error en el formulario', 'error')

    return render_template("moduloLogin/login.html", form=form)

@login_bp.route("/logout", methods=["GET", "POST"])
def logout():
    fl.logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login.login_view'))  # Asegúrate de que el nombre del endpoint sea correcto
