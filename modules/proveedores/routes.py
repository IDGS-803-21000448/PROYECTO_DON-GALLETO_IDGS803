from flask import render_template
from . import proveedores
from controllers.controller_login import requiere_rol
from flask_login import login_required

@proveedores.route("/crudProveedores", methods=["GET"])
@login_required
@requiere_rol("admin")
def crud_proveedores():
    return render_template("moduloProveedores/crudProveedores.html")