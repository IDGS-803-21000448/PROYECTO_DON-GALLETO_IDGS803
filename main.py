from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
import json
import controller
from config import DevelopmentConfig
from models import db
from controller import *
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
#-------------------------------
 
@app.route("/index",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/costoGalleta", methods=["GET"])
def costo_galleta():
    return render_template("costoGalleta.html")

@app.route("/crudProveedores", methods=["GET"])
def crud_proveedores():
    return render_template("crudProveedores.html")

@app.route("/crudRecetas", methods=["GET"])
def crud_recetas():
    return render_template("moduloRecetas/crudRecetas.html")

@app.route("/detalleReceta", methods=["GET"])
def detalle_recetas():
    formReceta = forms.RecetaForm(request.form)
    formDetalle = forms.RecetaDetalleForm(request.form)
    return render_template("moduloRecetas/detalleReceta.html", formReceta = formReceta, formDetalle = formDetalle)

@app.route("/crudUsuarios", methods=["GET"])
def crud_usuarios():
    return render_template("crudUsuarios.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/inventarioMaterias", methods=["GET"])
def inventario_materias():
    return render_template("inventarioMaterias.html")

@app.route("/inventarioTerminado", methods=["GET"])
def inventario_terminado():
    return render_template("inventarioTerminado.html")

@app.route("/layout", methods=["GET"])
def layout():
    return render_template("layout.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/moduloCompras", methods=["GET"])
def modulo_compras():
    return render_template("moduloCompras.html")

@app.route("/moduloVenta", methods=["GET"])
def modulo_venta():
    return render_template("moduloVenta.html")

@app.route("/produccion", methods=["GET"])
def produccion():
    return render_template("produccion.html")

@app.route("/solicitudProduccion", methods=["GET"])
def solicitud_produccion():
    return render_template("solicitudProduccion.html")

@app.route("/pruebaCaducidades", methods=["GET"])
def pruebaCaducidades():
    resultado = controller.verificarCaducidades()
    return json.dumps(resultado)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=8080)
