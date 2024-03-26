from flask import render_template
from . import inventarios
from controllers.controller_login import requiere_rol
from flask_login import login_required

@inventarios.route("/inventarioMaterias", methods=["GET"])
@login_required
@requiere_rol("admin")
def inventario_materias():
    return render_template("moduloInventarios/inventarioMaterias.html")

@inventarios.route("/inventarioTerminado", methods=["GET"])
@login_required
@requiere_rol("admin")
def inventario_terminado():
    return render_template("moduloInventarios/inventarioTerminado.html")