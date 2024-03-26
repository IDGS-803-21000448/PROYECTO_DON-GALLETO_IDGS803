from flask import render_template
from flask_login import login_required
from controllers.controller_login import requiere_rol

from controllers import controller_mermas
from . import index

@index.route('/index', methods=["GET"])
@login_required
@requiere_rol("Administrador", "venta", )
def index():
    controller_mermas.verificarCaducidades()
    return render_template("index.html")