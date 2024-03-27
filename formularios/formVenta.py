from wtforms import Form, StringField, IntegerField, validators, SelectField, DateField

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
