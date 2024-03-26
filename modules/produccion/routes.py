from flask import render_template

from . import produccion
from controllers.controller_login import requiere_rol
from flask_login import login_required

@produccion.route("/produccion", methods=["GET"])
@login_required
@requiere_rol("admin")
def produccion_main():
    return render_template("moduloProduccion/produccion.html")

@produccion.route("/solicitudProduccion", methods=["GET"])
@login_required
@requiere_rol("admin")
def solicitud_produccion():
    return render_template("moduloProduccion/solicitudProduccion.html")