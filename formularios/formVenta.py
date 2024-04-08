from wtforms import Form, StringField, IntegerField, validators, SelectField, DateField, FloatField, TextAreaField
from wtforms.widgets import HiddenInput

class VentaForm(Form):
    id = IntegerField('')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un nombre válido')
    ])
    tipo_venta = SelectField('Tipo de venta', choices=[
        ('pieza', 'Por pieza'),
        ('gramos', 'Por gramos'),
        ('paquete', 'Por paquete')
    ], validators=[
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un tipo de venta válido')
    ])
    paquete = SelectField('Paquete', choices=[
        ('0', 'Seleccione un paquete'),
        ('1', '700g'),
        ('2', '1Kg')
    ])
    sabor = SelectField('Sabor de galleta', validators=[
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un sabor válido')
    ])
    cantidad = IntegerField('Cantidad', [
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 1, max=100, message = "Ingrese una cantidad valida")
    ])
    fecha = DateField('Fecha de Registro', [
        validators.DataRequired(message='El campo es requerido'),
    ], format='%Y-%m-%d')

class FiltroVentaForm(Form):
    fecha = DateField('FechaVenta', format='%Y-%m-%d')
    mes = SelectField('Mes', choices=[
        ('1', 'Enero'),
        ('2', 'Febrero'),
        ('3', 'Marzo'),
        ('4', 'Abril'),
        ('5', 'Mayo'),
        ('6', 'Junio'),
        ('7', 'Julio'),
        ('8', 'Agosto'),
        ('9', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre')
    ])
    anio = IntegerField('Anio', [
        validators.number_range(min = 2019, max=2023, message = "Ingrese un anio valido")
    ])

class TurnoForm(Form):
    montoInicial = FloatField('Monto inicial', validators=[
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 1000.0, message = "Ingrese un monto valido")
    ])

class SalidaForm(Form):
    cantidad = FloatField('Monto inicial', validators=[
        validators.DataRequired(message='El campo es requerido'),
        validators.number_range(min = 10.0, message = "Ingrese un monto valido")
    ])
    justificacion = TextAreaField('Justificación', validators=[validators.DataRequired(message='El campo es requerido')])


class CerrarTurnoForm(Form):
    idTurno = IntegerField('idTurno', widget=HiddenInput(), default=0)

# Prueba venta por paquete de diferentes sabores
class MultisaborForm(Form):
    saborPaquete = SelectField('Sabores', validators=[
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un sabor válido')
    ])
    saboresSelected = StringField('saboresSelected', widget=HiddenInput())