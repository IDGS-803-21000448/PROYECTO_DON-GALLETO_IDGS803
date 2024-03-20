from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import CSRFProtect
import json
from config import DevelopmentConfig
from models import db, User
from controllers import controller_mermas
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
    # caducidades = controller.verificarCaducidades()
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
        listado_usuarios = User.query.filter_by(estatus='Activo').all()
        return render_template("crudUsuarios.html", form=form_usuarios, users=listado_usuarios)
    else:
        listado_usuarios = User.query.filter_by(estatus='Activo').all()
        return render_template("crudUsuarios.html", form=form_usuarios, users=listado_usuarios)
    
@app.route("/modificarUsuario", methods=["GET", "POST"])
def modificar_usuarios():
    form_usuarios = formUsuario.UsersForm(request.form)
    
    # Obtener el ID del usuario
    id = request.args.get('id')
    
    if id:
        # Intentar obtener el usuario de la base de datos
        user1 = User.query.filter_by(id=id, estatus='Activo').first()
        
        if user1:
            if request.method == "GET":
                # Poblar el formulario con los datos del usuario
                form_usuarios = formUsuario.UsersForm(obj=user1)
                # Asegurarse de que el campo confirmar_contrasena tenga los mismos datos que contrasena
                form_usuarios.confirmar_contrasena.data = user1.contrasena
            elif request.method == "POST":
                # Solo llenar los campos del formulario sin modificar el usuario en la base de datos
                form_usuarios.populate_obj(user1)
                flash("Usuario modificado temporalmente", "info")
        else:
            # Manejar el caso en que el usuario no se encuentre en la base de datos
            flash("Usuario no encontrado en la base de datos", "error")
            return redirect(url_for("crud_usuarios"))
    else:
        # Manejar el caso en que no se proporcione un ID de usuario
        flash("ID de usuario no proporcionado", "error")
        return redirect(url_for("crud_usuarios"))
    
    # Obtener el listado de usuarios activos
    listado_usuarios = User.query.filter_by(estatus='Activo').all()
    
    # Renderizar el template con el formulario y el listado de usuarios
    return render_template("modificarUsuario.html", form=form_usuarios, users=listado_usuarios)

@app.route("/confirmarModificacion", methods=["POST"])
def confirmar_modificacion():
    form_usuarios = formUsuario.UsersForm(request.form)

    id = request.form.get('id')
    user1 = User.query.filter_by(id=id, estatus='Activo').first()

    if request.method == "POST" and form_usuarios.validate():
        try:
            # Actualizar los datos del usuario con los del formulario
            form_usuarios.populate_obj(user1)
            
            # Modificar el usuario en la base de datos
            controller_usuarios.modificarUsuario(form_usuarios, id)
            
            # Confirmar los cambios en la base de datos
            db.session.commit()
            
            # Redireccionar y mostrar mensaje de éxito
            flash("Usuario modificado correctamente", "success")
            return redirect(url_for("crud_usuarios"))
        
        except Exception as e:
            # Manejar el caso en que ocurra un error al modificar el usuario
            db.session.rollback()
            flash(f"Error al modificar usuario: {str(e)}", "error")
            return redirect(url_for("crud_usuarios"))

    # Si la validación del formulario falla o no se envía una solicitud POST,
    # redireccionar de vuelta a la página de administración de usuarios
    return redirect(url_for("crud_usuarios"))


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
    resultado = controller_mermas.verificarCaducidades()
    return json.dumps(resultado)

@app.route('/moduloMermas')
def crud_mermas():
    return render_template('crudMermas.html')


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8080)