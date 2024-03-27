from wtforms import Form, StringField, IntegerField
from wtforms import *
from wtforms import validators
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput

class CompraForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    proveedor_id = IntegerField('ID de Materia Prima', validators=[DataRequired()])
    cantidad = FloatField('Cantidad', render_kw={"readonly": True})
    tipo = SelectField('Unidad de Medida', [
                        validators.DataRequired(message='El campo es requerido')
                            ],choices=[('g', 'g'),('kg', 'kg'), ('ml', 'ml'), ('l', 'l')])
    precio_compra = FloatField('Precio_Compra', render_kw={"readonly": True})
    fecha = StringField('Fecha Compra', [
        DataRequired(message='El campo es requerido')
    ])
    lote = StringField('Lote Merma', [
        DataRequired(message='El campo es requerido')
    ])
