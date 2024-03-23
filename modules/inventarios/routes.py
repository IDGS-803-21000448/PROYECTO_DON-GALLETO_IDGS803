from flask import render_template
from . import inventarios

@inventarios.route("/inventarioMaterias", methods=["GET"])
def inventario_materias():
    return render_template("moduloInventarios/inventarioMaterias.html")

@inventarios.route("/inventarioTerminado", methods=["GET"])
def inventario_terminado():
    return render_template("moduloInventarios/inventarioTerminado.html")