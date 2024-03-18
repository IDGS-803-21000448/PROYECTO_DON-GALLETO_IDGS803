from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db
import formUsuario

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
    return render_template("crudRecetas.html")

@app.route("/crudUsuarios", methods=["GET"])
def crud_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)
    return render_template("crudUsuarios.html", form = form_usuarios)

@app.route("/agregarUsuario", methods=["GET", "POST"])
def agregar_usuarios():
    
    return render_template("agregarUsuario.html")

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




if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    app.run()
