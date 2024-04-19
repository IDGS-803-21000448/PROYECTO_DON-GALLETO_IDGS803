from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import DevelopmentConfig
from models import db
from modules import (galletas, index, proveedores, usuarios, recetas, dashboard, inventarios, alertas, produccion,
                    mermas, ventas, compras, login, materiaPrima,solicitudProduccion, stock)
from models import *
import flask_login as fl
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
CORS(app, resources={r"/*": {"origins": "127.0.0.1:8080"}})
app.config['SECRET_KEY'] = 'llavesecreta1234'

login_manager = fl.LoginManager()
login_manager.init_app(app)

admin = Admin(app)
# Lista de modelos
modelos = [Tipo_Materia, MateriaPrima, Receta, RecetaDetalle, MermaMateriaPrima, Produccion, User, Alerta, MemraGalleta, Proveedor, Venta, DetalleVenta, CostoGalleta]

# Agregar cada modelo como vista de administrador
for modelo in modelos:
    admin.add_view(ModelView(modelo, db.session))


app.register_blueprint(index.index)
app.register_blueprint(galletas.galletas)
app.register_blueprint(proveedores.proveedores)
app.register_blueprint(usuarios.usuarios)
app.register_blueprint(recetas.recetas)
app.register_blueprint(dashboard.dashboard)
app.register_blueprint(inventarios.inventarios)
app.register_blueprint(alertas.alertas)
app.register_blueprint(produccion.produccion, name='produccion_blueprint')
app.register_blueprint(mermas.mermas)
app.register_blueprint(ventas.ventas)
app.register_blueprint(compras.compras)
app.register_blueprint(login.login)
app.register_blueprint(materiaPrima.materia_prima)
app.register_blueprint(solicitudProduccion.solicitud_produccion)
app.register_blueprint(stock.stock)

# Manejo de Errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(e):
    return render_template('errorScreen.html', error=e), 500

@app.errorhandler(500)
def page_not_found(e):
    return render_template('errorScreen.html'),500

@app.errorhandler(AttributeError)
def handle_attribute_error(e):
    return render_template('errorScreen.html', error=e), 500

@app.errorhandler(UnboundLocalError)
def handle_attribute_error(e):
    return render_template('errorScreen.html', error=e), 500

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

# Iniciar la aplicación
if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8080)