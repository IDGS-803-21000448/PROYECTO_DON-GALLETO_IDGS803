from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, TextAreaField, DateField, SearchField, FloatField, SelectField, FileField
from wtforms import validators
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RecetaForm(Form):
    nombre = StringField('Nombre receta', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=30, message='Ingresa un nombre valido')
    ])
    descripcion = TextAreaField('Pasos de receta', [
        validators.DataRequired(message='El campo es requerido')
    ])
    num_galletas = IntegerField('Numero de Galletas', [
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 20, max=100, message = "Ingrese una cantidad valida")
    ])
    fecha = DateField('Fecha de Registro', [
        validators.DataRequired(message='El campo es requerido'),
    ], format='%Y-%m-%d')
    cantidad = FloatField('Cantidad', [
        validators.number_range(min = 0.5, max=10.0, message = "Ingrese una cantidad valida")
    ])
    unidad_medida = SelectField('Unidad de Medida', [
        validators.DataRequired(message='El campo es requerido')
    ],choices=[('g', 'g'),('kg', 'kg'), ('ml', 'ml'), ('l', 'l'), ('pz', 'pz')])
    porcentaje_merma = FloatField('Porcentaje de Merma', [
        validators.number_range(min = 10.0, max=100.0, message = "Ingrese un porcentaje valido")
    ])
    ingrediente = SelectField('Ingrediente', [
    ])
    imagen = FileField('Imagen de la receta', validators=[FileAllowed(['png'], 'Solo se permiten archivos PNG')])
    ingredientes = StringField('ingredientes_array', [validators.DataRequired(message='El campo es requerido')])