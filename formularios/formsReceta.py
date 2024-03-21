from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, TextAreaField, DateField, SearchField, FloatField, SelectField
from wtforms import validators



class RecetaForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingresa un nombre valido')
    ])
    descripcion = TextAreaField('Descripcion', [
        validators.DataRequired(message='El campo es requerido')
    ])
    num_galletas = IntegerField('Numero de Galletas', [
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 20, max=100, message = "Ingrese una cantidad valida")
    ])
    fecha = DateField('Fecha de Registro', [
        validators.DataRequired(message='El campo es requerido'),
    ], format='%Y-%m-%d')
    ingredientes = StringField('ingredientes_array', [validators.DataRequired(message='El campo es requerido')])

class RecetaDetalleForm(Form):
    cantidad = FloatField('Cantidad', [
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 0.5, max=10.0, message = "Ingrese una cantidad valida")
    ])
    unidad_medida = SelectField('Unidad de Medida', [
        validators.DataRequired(message='El campo es requerido')
    ],choices=[('g', 'g'),('kg', 'kg'), ('ml', 'ml'), ('l', 'l')])
    porcentaje_merma = FloatField('Porcentaje de Merma', [
        validators.number_range(min = 10.0, max=100.0, message = "Ingrese un porcentaje valido")
    ])
    ingrediente = SelectField('Ingrediente', [
        validators.DataRequired(message='El campo es requerido')
    ])