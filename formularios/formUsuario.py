from wtforms import Form
from wtforms import *
from wtforms import validators
from wtforms.widgets import HiddenInput


class UsersForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    nombre=StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=40, message='Ingresa un nombre valido')
    ])
    puesto=StringField('Puesto', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=20, message='Ingresa un apellido paterno valido')
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
        #validators.DataRequired(message='El campo es requerido'),
        validators.length(min= 4, max=15, message='Ingresa una contraseña valida')
    ])
    confirmar_contrasena = PasswordField('Confirmar contraseña', [
        #validators.DataRequired(message='El campo es requerido'),
        validators.length(min= 4, max=15, message='Ambas contraseñas deben de coincidir.')
    ])
    
class UsersFormModificar(Form):
    id = IntegerField('')
    nombre=StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=40, message='Ingresa un nombre valido')
    ])
    puesto=StringField('Puesto', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=20, message='Ingresa un apellido paterno valido')
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
       # validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa una contraseña valida')
    ])
    confirmar_contrasena = PasswordField('Confirmar contraseña', [
      #  validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ambas contraseñas deben de coincidir.')
    ])