from . import alertas

from flask import render_template, request, redirect, url_for

from models import db, Alerta
from formularios import formAlerta
from flask_login import login_required
from controllers.controller_login import requiere_token

@alertas.route('/alertas', methods=['GET', 'POST'])
@login_required
@requiere_token
def alertas_main():
    form_alerta = formAlerta.FormAlerta(request.form)
    listado_alertas = []

    if request.method == 'POST' and form_alerta.validate():
        filtro = form_alerta.filtroAlerta.data

        if filtro == 'todas':
            listado_alertas = Alerta.query.all()
        elif filtro == 'cumplidas':
            listado_alertas = Alerta.query.filter_by(estatus=1).all()
        elif filtro == 'incumplidas':
            listado_alertas = Alerta.query.filter_by(estatus=0).all()
    else:
        listado_alertas = Alerta.query.all()

    return render_template("moduloAlertas/alertas.html", alertas=listado_alertas, form=form_alerta)


@alertas.route('/actualizar_alerta', methods=['POST'])
@login_required
@requiere_token
def actualizar_alerta():
    alerta_id = request.form.get('alerta_id')  
    alerta = Alerta.query.get(alerta_id)  

    if alerta:
        nuevo_estado = 0 if alerta.estatus == 1 else 1  
        alerta.estatus = nuevo_estado  
        db.session.commit()  

    return redirect(url_for('alertas.alertas_main'))  