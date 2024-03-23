from flask import render_template
from . import proveedores

@proveedores.route("/crudProveedores", methods=["GET"])
def crud_proveedores():
    return render_template("moduloProveedores/crudProveedores.html")