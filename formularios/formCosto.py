from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class CalculoCompraForm(FlaskForm):
    precio_mano_obra = FloatField('Precio por Mano de Obra', validators=[
        DataRequired(message='El campo es requerido'),
        NumberRange(min=0, message='El precio no puede ser negativo')
    ])