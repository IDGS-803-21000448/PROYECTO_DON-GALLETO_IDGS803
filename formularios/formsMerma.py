from wtforms import Form, IntegerField, StringField, FloatField, TextAreaField, DateTimeField, SelectField, \
    DateTimeLocalField
from wtforms.validators import DataRequired, length, number_range
from wtforms.widgets import HiddenInput


class MermaMateriaPrimaForm(Form):
    id = IntegerField('id', widget=HiddenInput(), default=0)
    materia_prima_id = IntegerField('ID de Materia Prima', validators=[DataRequired(message='El campo es requerido')])
    nombre = StringField('Nombre Producto', render_kw={"readonly": True})
    cantidad = FloatField('Cantidad',  validators=[DataRequired(message='El campo es requerido'), number_range(min = 0.1, message="Ingrese una longitud valida")])
    descripcion = TextAreaField('Descripción', validators=[DataRequired(message='El campo es requerido')])
    fecha = StringField('Fecha Registro', [
        DataRequired(message='El campo es requerido')
    ])
    tipo_merma = SelectField(
        'Tipo de merma',
        choices=[('materiaPrima', 'Materia Prima'), ('galletas', 'Galletas')],
        default='materiaPrima',
        validators=[DataRequired(message='El campo es requerido.')]
    )
    tipo = SelectField('Unidad de Medida', [
        DataRequired(message='El campo es requerido')
    ], choices=[('g', 'g'), ('kg', 'kg'), ('ml', 'ml'), ('l', 'l'), ('pz', 'pz'), ("pkg", "pkg")], render_kw={"readonly": True})


class tipoMermaForm(Form):
    tipo_merma = SelectField('Tipo de merma', choices=[
        ('materiaPrima', 'Materia Prima'), ('galletas', 'Galletas')],
                             validators=[DataRequired(message='El campo es requerido.')])
