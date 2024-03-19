from wtforms import Form
from wtforms import *
from wtforms import validators


class UsersForm(Form):
    id = IntegerField('id')
    nombre=StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un nombre valido')
    ])
    puesto=StringField('Puesto', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un apellido paterno valido')
    ])
    rol = SelectField('Rol', choices=[
        ('admin', 'Administrador'), ('venta', 'Ventas'), ('produccion', 'Producción'), ('inventario', 'Inventario')
        ], validators=[validators.DataRequired(message='El campo es requerido.')])
    # estatus = SelectField('Estatus', choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], validators=[validators.DataRequired(message='El campo es requerido.')])

    usuario = StringField('Usuario', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un usuario valido')
    ])
    contrasena = PasswordField('Contraseña', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa una contraseña valida')
    ])