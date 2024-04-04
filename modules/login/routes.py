from flask import render_template, request, flash, redirect, url_for, make_response
from . import login as login_bp  # Cambia el nombre al importar para evitar conflictos
from formularios.formLogin import LoginForm
import flask_login as fl
from flask_login import current_user
from models import db, User, LogLogin
from controllers.controller_login import generate_jwt_token, verificar_contrasena
import datetime


@login_bp.route("/login", methods=["GET", "POST"])
def login_view():  # Cambia el nombre de la función para evitar conflictos
    form = LoginForm(request.form)

    if request.method == "POST":
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        if not usuario:
            flash('El campo usuario es requerido', 'error')
            return render_template("moduloLogin/login.html", form=form)
        
        if not request.form['contrasena']:
            flash('El campo contraseña es requerido', 'error')
            return render_template("moduloLogin/login.html", form=form)

        try:
            user = User.query.filter_by(usuario=usuario).first()
        except Exception as e:
            flash('Error al iniciar sesion', 'error')
            return render_template("moduloLogin/login.html", form=form)

        if not user:
            flash('El usuario no se puede identificar, vuelve a intentarlo', 'error')
            return render_template("moduloLogin/login.html", form=form)

        # obtener los logs de inicio de sesion del usuario
        logs = LogLogin.query.filter_by(id_user=user.id).order_by(LogLogin.id.desc()).limit(5).all()

        # verificar si los ultimos 3 intentos de inicio de sesion del usuario son correctos, si hay 3 o mas incorrectos, bloquear el usuario por 5 minutos
        incorrectos = 0
        for log in logs:
            if log.estatus == 'incorrecto':
                incorrectos += 1
            else:
                break
        # verificar si hay 3 o mas intentos incorrectos y si el campo fecha no han pasado 5 minutos desde su registro
        if incorrectos >= 3 and log.fecha + datetime.timedelta(minutes=5) > datetime.datetime.now():
            flash('Su usuario ha sido bloqueado temporalmente por 5 minutos debido a 3 intentos incorrectos', 'error')
            return render_template("moduloLogin/login.html", form=form)

        # Insertar log de inicio de sesion en base de datos con estatus 'pendiente'
        log = LogLogin(log='Hay un intento de inicio de sesión', ip=request.remote_addr, direccion=request.headers.get('X-Forwarded-For', request.remote_addr), id_user=user.id, estatus='pendiente')
        db.session.add(log)
        db.session.commit()

        validPass = verificar_contrasena(contrasena, user.contrasena)
        if user and validPass:
            # Usuario autenticado correctamente
            res = fl.login_user(user, force=True)

            token = generate_jwt_token(user.id)
            print(f"TOKEN: {token}")
            if token is None:
                # Manejar el caso de error, por ejemplo, enviando una respuesta de error
                flash('Error al generar el token de autenticación', 'error')
                return render_template("moduloLogin/login.html", form=form)

            # Si todo está bien, proceder como antes
            response = make_response(redirect(url_for('index.index')))
            #enviar token al localstorage de la web
            response.set_cookie('auth_token', token, samesite='None', secure=True, httponly=True)
            print(f"------------------ REDIRECCIONANDO ------------------")
            # actualizar el estatus del log a 'correcto'
            log.estatus = 'correcto'
            db.session.commit()

            return response    
        else:
            # actualizar el estatus del log a 'incorrecto'
            log.estatus = 'incorrecto'
            db.session.commit()
            flash('Usuario o contraseña incorrectos. Verifiquelo y vuelva a intentarlo', 'error')    

    return render_template("moduloLogin/login.html", form=form)

@login_bp.route("/logout", methods=["GET"])
def logout():
    fl.logout_user()
    response = make_response(redirect(url_for('login.login_view')))
    response.set_cookie('auth_token', '')
    flash('Has cerrado sesión', 'success')
    return response  # Asegúrate de que el nombre del endpoint sea correcto

@login_bp.route("/")
def login():
    return redirect(url_for('login.login_view'))
