from wtforms import Form
from wtforms import *
from wtforms import validators

class FormAlerta(Form):
    filtroAlerta = SelectField('Filtrar alertas', choices=[
            ('todas', 'Todas las alertas'), ('cumplidas', 'Alertas cumplidas'), ('incumplidas', 'Alertas sin cumplir')], validators=[validators.DataRequired(message='El campo es requerido.')])
