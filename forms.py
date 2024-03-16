from wtforms import Form
from wtforms import StringField, EmailField, IntegerField
from wtforms import validators


class UsersForm(Form):
    nombre=StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingresa un nombre valido')
    ])
    apaterno=StringField('apaterno', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un apellido paterno valido')
    ])
    amaterno=StringField('amaterno', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un apellido materno valido')
    ])
    edad = IntegerField('edad', [
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 1, max=20, message = "Ingrese Una edad Valido")
    ])
    correo = EmailField('correo', [
        validators.Email(message='Ingrese un correo valido')
    ])