from flask import render_template
from . import galletas

@galletas.route("/costoGalleta", methods=["GET"])
def costo_galleta():
    return render_template("moduloGalletas/costoGalleta.html")