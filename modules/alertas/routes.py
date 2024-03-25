from . import alertas

from flask import render_template, request, redirect, url_for

from models import db, Alerta
from formularios import formAlerta

@alertas.route('/alertas', methods=['GET', 'POST'])
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
def actualizar_alerta():
    alerta_id = request.form.get('alerta_id')  # Obtener el ID de la alerta
    alerta = Alerta.query.get(alerta_id)  # Obtener la alerta de la base de datos

    if alerta:
        nuevo_estado = 0 if alerta.estatus == 1 else 1  # Cambiar el estado
        alerta.estatus = nuevo_estado  # Actualizar el estado en la base de datos
        db.session.commit()  # Guardar los cambios

    return redirect(url_for('alertas.alertas_main'))  # Redireccionar a la página de alertas