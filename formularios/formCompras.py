from wtforms import Form, StringField, IntegerField
from wtforms import *
from wtforms import validators
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput

class CompraForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    proveedor_id = IntegerField('ID de Proveedopr', validators=[DataRequired()])
    id_tipo_materia = IntegerField('ID de Materia Prima', validators=[DataRequired()])
    nombre = StringField('Nombre Producto', render_kw={"readonly": True})
    nombre_proveedor = StringField('Nombre Proveedor', render_kw={"readonly": True})

    cantidad = FloatField('Cantidad')
    tipo = SelectField('Unidad de Medida', [
                        validators.DataRequired(message='El campo es requerido')
                            ],choices=[('g', 'g'),('kg', 'kg'), ('ml', 'ml'), ('l', 'l'), ('pz', 'pz')])
    precio_compra = FloatField('Precio_Compra')
    fecha = StringField('Fecha Compra', [
        DataRequired(message='El campo es requerido')
    ])
    fecha_caducidad = StringField('Fecha Caducidad', [
        DataRequired(message='El campo es requerido')
    ])
    lote = StringField('Lote Merma', [
        DataRequired(message='El campo es requerido')
    ])
