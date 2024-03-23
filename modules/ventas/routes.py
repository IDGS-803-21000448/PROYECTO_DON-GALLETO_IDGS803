from flask import render_template
from . import ventas

@ventas.route("/moduloVenta", methods=["GET"])
def modulo_venta():
    return render_template("moduloVentas/moduloVenta.html")