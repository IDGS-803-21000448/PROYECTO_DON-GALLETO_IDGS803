from wtforms import Form, StringField, IntegerField
from wtforms import *
from wtforms import validators
from wtforms.widgets import HiddenInput

class ProveedorForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    nombre=StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='Ingresa un nombre valido')
    ])
    direccion=StringField('Dirección', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='Ingresa una dirección valida')
    ])
    telefono=StringField('Telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un telefono valido')
    ])
    nombre_vendedor=StringField('Nombre del Vendedor', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=15, message='Ingresa un nombre valido')
    ])