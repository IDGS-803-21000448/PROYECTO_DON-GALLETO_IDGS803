from flask import render_template
from flask_login import login_required
from controllers.controller_login import requiere_rol, requiere_token
from flask_login import current_user
from controllers import controller_mermas
from models import Alerta
from . import index

@index.route('/index', methods=["GET"])
@login_required
@requiere_token
def index():
    print(f"USUARIO: {current_user}")
    controller_mermas.verificarCaducidades()
    alertas = Alerta.query.filter_by(estatus = 0).all()
    return render_template("index.html", countAlertas = len(alertas))