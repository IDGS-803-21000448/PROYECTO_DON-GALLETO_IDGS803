from flask import Flask, render_template
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db
from modules import (galletas, index, proveedores, usuarios, recetas, dashboard, inventarios, alertas, produccion,
                     mermas, ventas, compras, login)


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


app.register_blueprint(index.index)
app.register_blueprint(galletas.galletas)
app.register_blueprint(proveedores.proveedores)
app.register_blueprint(usuarios.usuarios)
app.register_blueprint(recetas.recetas)
app.register_blueprint(dashboard.dashboard)
app.register_blueprint(inventarios.inventarios)
app.register_blueprint(alertas.alertas)
app.register_blueprint(produccion.produccion)
app.register_blueprint(mermas.mermas)
app.register_blueprint(ventas.ventas)
app.register_blueprint(compras.compras)
app.register_blueprint(login.login)

# Manejo de Errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

# Iniciar la aplicación
if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=False, port=8080)