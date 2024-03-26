from flask import render_template
from . import compras
from controllers.controller_login import requiere_rol
from flask_login import login_required

@compras.route("/moduloCompras", methods=["GET"])
@login_required
@requiere_rol("admin")
def modulo_compras():
    return render_template("moduloCompras/moduloCompras.html")