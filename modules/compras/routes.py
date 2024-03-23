from flask import render_template
from . import compras

@compras.route("/moduloCompras", methods=["GET"])
def modulo_compras():
    return render_template("moduloCompras/moduloCompras.html")