from flask import render_template, redirect, url_for
from flask_login import login_required
from controllers.controller_login import requiere_rol, requiere_token
from flask_login import current_user
from controllers import controller_mermas, controller_costo, controller_materia_prima, controller_alertas
from models import Alerta
from . import index

@index.route('/index', methods=["GET"])
@login_required
@requiere_token
def index():
    print(f"USUARIO: {current_user}")
    controller_mermas.verificarCaducidades()
    controller_mermas.verificarCaducidadesGalletas()
    controller_alertas.verificarCantidades()
    controller_alertas.verificarCantidadesGalletas()
    return redirect(url_for('dashboard.dashboard'))