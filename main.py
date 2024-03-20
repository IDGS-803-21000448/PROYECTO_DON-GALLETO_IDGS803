from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import CSRFProtect
import json
import controller
from config import DevelopmentConfig
from models import db, User
from controller import *
from controllers import controller_usuarios
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

    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    return render_template("crudUsuarios.html", form=form_usuarios, users=listado_usuarios)

@app.route("/agregarUsuario", methods=["GET", "POST"])
def agregar_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)
    if request.method == "POST" and form_usuarios.validate():
        # Verificar si las contraseñas coinciden
        contrasena = form_usuarios.contrasena.data
        confirmar_contrasena = form_usuarios.confirmar_contrasena.data
        if contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden. Inténtalo de nuevo.", "error")
            listado_usuarios = User.query.all()
            return render_template("crudUsuarios.html", form=form_usuarios, users=listado_usuarios)

        controller_usuarios.agregarUsuario(form_usuarios)
        form_usuarios = formUsuario.UsersForm()
        listado_usuarios = User.query.all()
        return render_template("crudUsuarios.html", form=form_usuarios, users=listado_usuarios)
    else:
        listado_usuarios = User.query.all()
        return render_template("crudUsuarios.html", form=form_usuarios, users=listado_usuarios)
    
@app.route("/modificarUsuario", methods=["GET", "POST"])
def modificar_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)
    idFuncional = []
    if request.method == "GET":
        id = request.args.get('id')
        idFuncional.append(id)
        print(id,"aqui2")
        if id:
            user1 = db.session.query(User).filter(User.id == id).first()
            if user1:
                form_usuarios.id.data = id
                form_usuarios.nombre.data = user1.nombre
                form_usuarios.puesto.data = user1.puesto
                form_usuarios.rol.data = user1.rol
                # form_usuarios.estatus.data = user1.estatus
                form_usuarios.usuario.data = user1.usuario
                form_usuarios.contrasena.data = user1.contrasena
            else:
                # Manejar el caso en que el usuario no existe
                return "Usuario no encontrado"
        else:
            # Manejar el caso en que no se proporciona un ID de usuario
            return "ID de usuario no proporcionado"
    if request.method == "POST":
        #id = form_usuarios.id.data
        #id = idFuncional2
        id = idFuncional[1]
        print(id,"aqui")
        user1 = db.session.query(User).filter(User.id == id).first()
        if user1:
            user1.nombre = form_usuarios.nombre.data
            user1.puesto = form_usuarios.puesto.data
            user1.rol = form_usuarios.rol.data
            # user1.estatus = form_usuarios.estatus.data
            user1.usuario = form_usuarios.usuario.data
            user1.contrasena = form_usuarios.contrasena.data
            db.session.add(user1)
            db.session.commit()
            return redirect(url_for("crud_usuarios"))  # Redirecciona a la vista de usuarios
        else:
            # Manejar el caso en que el usuario no existe
            return "Usuario no encontrado en la base de datos"
    listado_usuarios = User.query.all()
    return render_template("modificarUsuario.html", form=form_usuarios, users=listado_usuarios)


@app.route("/confirmarEliminacion", methods=["GET", "POST"])
def confirmarEliminacion():
    id = request.args.get('id')
    if id:
        user = User.query.filter_by(id=id, estatus='Activo').first()
        if user:
            return render_template("confirmarBorradoUsuario.html", usuario_id=id)
        else:
            flash('Usuario no encontrado en la base de datos o ya está inactivo', 'error')
    else:
        flash('ID de usuario no proporcionado', 'error')

    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    return render_template("crudUsuarios.html", users=listado_usuarios)

@app.route("/borrarUsuario", methods=["GET", "POST"])
def borrar_usuario():
    id = request.args['id']  # Obtener directamente el ID del usuario de la URL
    if id:
        user = User.query.filter_by(id=id, estatus='Activo').first()
        if user:
            # Cambiar el estado del usuario a 'Inactivo' en lugar de eliminarlo físicamente
            user.estatus = 'Inactivo'
            db.session.commit()
            flash('Usuario marcado como inactivo correctamente', 'success')
            return redirect(url_for("crud_usuarios"))  # Redirigir a la página de listado de usuarios
        else:
            # Manejar el caso en que el usuario no existe o ya está inactivo
            flash('Usuario no encontrado en la base de datos o ya está inactivo', 'error')
    else:
        flash('ID de usuario no proporcionado', 'error')

    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    return render_template("crudUsuarios.html", users=listado_usuarios)

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
