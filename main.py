from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import DevelopmentConfig
from models import db
from modules import (galletas, index, proveedores, usuarios, recetas, dashboard, inventarios, alertas, produccion,
                     mermas, ventas, compras, login)
from models import Alerta, User, MateriaPrima, MermaMateriaPrima, Produccion, Receta, RecetaDetalle


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Alerta, db.session))
admin.add_view(ModelView(MateriaPrima, db.session))
admin.add_view(ModelView(Produccion, db.session))
admin.add_view(ModelView(Receta, db.session))
admin.add_view(ModelView(MermaMateriaPrima, db.session))
admin.add_view(ModelView(RecetaDetalle, db.session))


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

    app.run(debug=True, port=8080)