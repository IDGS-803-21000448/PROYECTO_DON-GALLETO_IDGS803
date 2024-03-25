from flask import render_template, request, flash, redirect, url_for
from . import login
from formularios.formLogin import LoginForm
import flask_login as fl
from models import db, User


@login.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        user = request.form['usuario']
        password = request.form['contrasena']
        user = User.query.filter_by(email=user).first()
        if user and user.contrasena == password:
            fl.login_user(user)
            flash('Has iniciado sesión', 'success')
            return redirect(url_for('index'))

    return render_template("moduloLogin/login.html")


@login.route("/logout", methods=["GET", "POST"])
def logout():
    fl.logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login'))