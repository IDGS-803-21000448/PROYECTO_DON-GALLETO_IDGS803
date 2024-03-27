from wtforms import Form, IntegerField, FloatField, SelectField, validators, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput


class MateriaPrimaForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    nombre = StringField('Lote Merma', [
        DataRequired(message='El campo es requerido')
    ])
    cantidad = FloatField('Cantidad')
    tipo = SelectField('Unidad de Medida', [
                        validators.DataRequired(message='El campo es requerido')
                            ],choices=[('g', 'g'),('kg', 'kg'), ('ml', 'ml'), ('l', 'l')])