from wtforms import Form, PasswordField, StringField
from wtforms.validators import DataRequired, length

class LoginForm(Form):
    usuario = StringField('Usuario', validators=[DataRequired(message='El campo es requerido')])
    contrasena = PasswordField('Contraseña', validators=[DataRequired(message='El campo es requerido')])