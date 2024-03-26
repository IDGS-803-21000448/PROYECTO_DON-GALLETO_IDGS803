from flask import render_template
from . import galletas
from controllers.controller_login import requiere_rol
from flask_login import login_required

@galletas.route("/costoGalleta", methods=["GET"])
@login_required
@requiere_rol("admin")
def costo_galleta():
    return render_template("moduloGalletas/costoGalleta.html")