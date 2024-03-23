from . import recetas

from flask import render_template, request
from formularios import formsReceta


@recetas.route("/vistaRecetas", methods=["GET"])
def vista_reectas():
    return render_template("moduloRecetas/vistaRecetas.html")

@recetas.route("/crudRecetas", methods=["GET"])
def crud_recetas():
    return render_template("moduloRecetas/crudRecetas.html")

@recetas.route("/detalleReceta", methods=["GET"])
def detalle_recetas():
    formReceta = formsReceta.RecetaForm(request.form)
    formDetalle = formsReceta.RecetaDetalleForm(request.form)
    return render_template("moduloRecetas/detalleReceta.html", formReceta = formReceta, formDetalle = formDetalle)