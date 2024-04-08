from wtforms import Form, IntegerField, FloatField, SelectField, validators, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput


class MateriaPrimaForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    nombre = StringField('Nombre Materia Prima', [
        DataRequired(message='El campo es requerido')
    ])
    cantidad = FloatField('Cantidad', default=0, render_kw={"readonly": True})
    tipo = SelectField('Unidad de Medida', [
                        validators.DataRequired(message='El campo es requerido')
                            ],choices=[('g', 'g'),('kg', 'kg'), ('ml', 'ml'), ('l', 'l')])