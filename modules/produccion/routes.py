from flask import render_template

from . import produccion

@produccion.route("/produccion", methods=["GET"])
def produccion():
    return render_template("moduloProduccion/produccion.html")

@produccion.route("/solicitudProduccion", methods=["GET"])
def solicitud_produccion():
    return render_template("moduloProduccion/solicitudProduccion.html")